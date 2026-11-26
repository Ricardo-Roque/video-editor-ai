"""Assemble the final video from approved takes: trim silences, upscale, word-by-word captions, overlays.

Usage:
  python -I -X utf8 tools/montar.py --config "Criativo 01/montagem.json" [--stage all|segments|captions|final]

Pipeline:
  1. Word timings per clip (faster-whisper, cached as <clip>.words.json), aligned to the script text
     so captions use the correct spelling.
  2. Each clip trimmed to its speech (+ small pads), scaled to 1080x1920 @30fps -> montagem/seg_NN.mp4
  3. Segments concatenated -> montagem/assembled.mp4
  4. Captions (ASS, 1-3 words, keyword highlighted) + image overlays + loudness normalisation -> output.
"""
import argparse
import difflib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lote_takes import ROOT, parse_rows  # noqa: E402

W, H, FPS = 1080, 1920, 30
PAD_IN, PAD_OUT = 0.10, 0.28
CAPTION_Y = 1420  # ~74% of height: low, but above the Reels/TikTok UI zone
HIGHLIGHT = "&H0000FFE5&"  # ASS BGR for #E5FF00 (yellow-lime)
STOPWORDS = set("""
a à au aux avec ce ces c cette d de des du elle en et il ils je j l la le les leur leurs lui m ma mais me même mes
mon n ne nous on ou où par pas pour qu que qui s sa se ses si son sur t ta te tes ton tu un une vos votre vous y
est sont a ont été être fait ça plus très tout tous toute bien comme dont là sous
the and or of to in on at is are was were be it this that your you my his her their with for not no just so
o os as um uma de do da dos das em no na nos nas e é que para por com seu sua não mais
el los las un una del en y es que para por con su sus no más
""".split())


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if p.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(map(str, cmd))}\n{p.stderr[-2000:]}")
    return p.stdout


def duration(path) -> float:
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]))


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c) and c.isalnum())


_model = None


def whisper_words(clip: pathlib.Path, language: str = "fr"):
    cache = clip.with_suffix(".words.json")
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    global _model
    import numpy as np
    from faster_whisper import WhisperModel
    if _model is None:
        _model = WhisperModel("medium", device="cpu", compute_type="int8")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(clip), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    segs, _ = _model.transcribe(audio, language=language, beam_size=5, word_timestamps=True,
                                condition_on_previous_text=False)
    words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in s.words]
    cache.write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")
    return words


def keep_intervals(clip: pathlib.Path, start: float, end: float, words=None, min_gap=0.35, keep_after=0.12,
                   keep_before=0.10, min_piece=0.40, word_margin=0.04):
    """Speech-only intervals inside [start, end]: pauses longer than min_gap are shortened (jump cuts).

    A pause is only cut when no heard word overlaps it (soft words such as "et" or a word's quiet tail can fall
    under the silence threshold), and never when it would leave a piece shorter than min_piece (stutter).
    """
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(clip), "-af", f"silencedetect=n=-38dB:d={min_gap}",
                          "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?[0-9.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
    if len(ends) < len(starts):
        ends.append(end + 1)
    spans = [(w["s"], w["e"]) for w in (words or []) if norm(w["w"])]
    cuts = []
    for ss, se in zip(starts, ends):
        a = start if ss <= start + 0.02 else ss + keep_after
        b = end if se >= end - 0.02 else se - keep_before
        a, b = max(a, start), min(b, end)
        if b - a <= 0.05:
            continue
        inner = a > start and b < end  # leading/trailing silence is always trimmed
        if inner and any(ws < b - word_margin and we > a + word_margin for ws, we in spans):
            continue
        cuts.append((a, b))
    # drop cuts that would create a tiny piece between two cuts or at the edges
    changed = True
    while changed:
        changed = False
        edges = [start] + [x for c in cuts for x in c] + [end]
        pieces = [(edges[i], edges[i + 1]) for i in range(0, len(edges), 2)]
        for i, (pa, pb) in enumerate(pieces):
            if pb - pa < min_piece and len(cuts) > 0:
                # remove the inner cut adjacent to this piece (prefer the one after it)
                j = i if i < len(cuts) and cuts[i][1] < end else i - 1
                if 0 <= j < len(cuts) and cuts[j][0] > start and cuts[j][1] < end:
                    cuts.pop(j)
                    changed = True
                    break
    keep, cur = [], start
    for a, b in cuts:
        if a > cur:
            keep.append((cur, a))
        cur = max(cur, b)
    if cur < end:
        keep.append((cur, end))
    return [(a, b) for a, b in keep if b - a > 0.06]


def remap(t: float, keep: list[tuple]) -> float:
    """Original clip time -> time inside the cut segment."""
    out = 0.0
    for a, b in keep:
        if t <= a:
            break
        out += min(t, b) - a
    return out


def align(script_text: str, heard: list[dict]) -> list[dict]:
    """Give every script word a start/end time using the whisper words (character-level alignment)."""
    tokens = script_text.replace("⚠", "").split()
    # Build character streams with an owner index so that splits/merges between the two
    # transcriptions ("s'y" vs "s 'y", "hémato-encéphalique" vs "hémato -encéphalique") still line up.
    s_chars, s_owner = [], []
    for i, t in enumerate(tokens):
        for c in norm(t):
            s_chars.append(c)
            s_owner.append(i)
    h_chars, h_owner = [], []
    for j, w in enumerate(heard):
        for c in norm(w["w"]):
            h_chars.append(c)
            h_owner.append(j)
    times = [[None, None] for _ in tokens]
    sm = difflib.SequenceMatcher(None, s_chars, h_chars, autojunk=False)
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            i, j = s_owner[a + k], h_owner[b + k]
            st, en = heard[j]["s"], heard[j]["e"]
            times[i][0] = st if times[i][0] is None else min(times[i][0], st)
            times[i][1] = en if times[i][1] is None else max(times[i][1], en)
    # Interpolate words that were not heard.
    known = [i for i, t in enumerate(times) if t[0] is not None]
    if not known:
        raise RuntimeError(f"could not align: {script_text[:60]}")
    for i, t in enumerate(times):
        if t[0] is None:
            prev = max((k for k in known if k < i), default=None)
            nxt = min((k for k in known if k > i), default=None)
            lo = times[prev][1] if prev is not None else times[nxt][0] - 0.3
            hi = times[nxt][0] if nxt is not None else times[prev][1] + 0.3
            t[0], t[1] = lo, hi
    out = []
    for tok, (st, en) in zip(tokens, times):
        out.append({"w": tok, "s": st, "e": max(en, st + 0.05)})
    for k in range(1, len(out)):  # keep monotonic
        out[k]["s"] = max(out[k]["s"], out[k - 1]["s"])
    return out


def group_words(words: list[dict]) -> list[list[dict]]:
    groups, cur = [], []
    for w in words:
        # Keep a line within ~18 characters so it fits the frame at this font size.
        if cur and sum(len(x["w"]) + 1 for x in cur) + len(w["w"]) > 18:
            groups.append(cur)
            cur = []
        cur.append(w)
        clean = re.sub(r"[^\w'’-]", "", w["w"])
        if re.search(r"[,.:;!?]$", w["w"]) or len(cur) == 3 or len(clean) >= 11:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def caption_text(group: list[dict]) -> str:
    clean = [re.sub(r"[,.:;!?…]+$", "", w["w"]) for w in group]
    scores = []
    for c in clean:
        n = norm(c)
        base = n.split("'")[-1]
        scores.append(-1 if (n in STOPWORDS or len(n) <= 2) else len(n))
    best = max(range(len(clean)), key=lambda i: scores[i])
    parts = []
    for i, c in enumerate(clean):
        c = c.replace("{", "").replace("}", "")
        parts.append(f"{{\\c{HIGHLIGHT}}}{c}{{\\c&H00FFFFFF&}}" if i == best and scores[i] > 0 else c)
    return " ".join(parts)


def ass_time(t: float) -> str:
    t = max(0.0, t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_ass(path: pathlib.Path, timeline: list[dict], font_name: str, total: float, cap_y: int = CAPTION_Y):
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
        "MarginR, MarginV, Encoding",
        f"Style: Cap,{font_name},92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,5,3,5,60,60,0,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    groups = []
    for clip in timeline:
        for g in group_words(clip["words"]):
            groups.append((clip["offset"] + g[0]["s"] - clip["trim_start"],
                           clip["offset"] + g[-1]["e"] - clip["trim_start"],
                           clip["offset"] + clip["dur"], g))
    for k, (st, en, clip_end, g) in enumerate(groups):
        nxt = groups[k + 1][0] if k + 1 < len(groups) else total
        end = min(max(en + 0.08, st + 0.30), nxt, clip_end)
        lines.append(f"Dialogue: 0,{ass_time(st)},{ass_time(end)},Cap,,0,0,0,,"
                     f"{{\\an5\\pos({W // 2},{cap_y})}}{caption_text(g)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def make_card(src: pathlib.Path, dst: pathlib.Path, width=430, aspect=4 / 3, radius=32):
    from PIL import Image, ImageDraw
    im = Image.open(src).convert("RGB")
    w, h = im.size
    target_h = int(w / aspect)
    if target_h <= h:
        top = (h - target_h) // 2
        im = im.crop((0, top, w, top + target_h))
    im = im.resize((width, int(width / aspect)), Image.LANCZOS)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), radius=radius, fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    out.save(dst)
    return out.size


EDGE_IN, EDGE_OUT = 0.08, 0.18


def speech_edges(clip: pathlib.Path, lo: float, hi: float, thr_db=-38.0, win=0.02, run_len=3):
    """First/last moment inside [lo, hi] where the voice is on (RMS over thr_db for run_len windows).

    Whisper often reports the first word at 0.0 s and silencedetect misses room tone with small peaks,
    so take starts/ends keep dead air; this measures the voice itself.
    """
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(clip), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    n = int(16000 * win)
    rms = np.array([np.sqrt(np.mean(a[i:i + n] ** 2)) + 1e-9 for i in range(0, len(a) - n, n)])
    on_mask = 20 * np.log10(rms) > thr_db
    t = np.arange(len(rms)) * win
    idx = [i for i in range(len(rms) - run_len + 1)
           if lo <= t[i] <= hi and on_mask[i:i + run_len].all()]
    if not idx:
        return lo, hi
    # The last syllable can run past whisper's word end: follow the voice while it continues without a gap.
    last = idx[-1] + run_len - 1
    max_gap, limit = int(0.15 / win), min(len(rms) - 1, int((hi + 0.5) / win))
    k = last + 1
    while k <= limit:
        nxt = next((j for j in range(k, min(limit, k + max_gap) + 1) if on_mask[j]), None)
        if nxt is None:
            break
        last, k = nxt, nxt + 1
    return float(t[idx[0]]), float(t[last] + win)


def make_full(src: pathlib.Path, dst: pathlib.Path):
    """Crop an image to 9:16 (centre) and scale it to the full frame."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h > W / H:
        nw = int(h * W / H)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w * H / W)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.resize((W, H), Image.LANCZOS).save(dst)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--stage", default="all", choices=["all", "segments", "captions", "final"])
    args = ap.parse_args()

    cfg_path = ROOT / args.config
    base = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    script = {t: text for t, _, text in parse_rows(base / cfg["script"])}
    work = base / cfg["work_dir"]
    work.mkdir(exist_ok=True)
    takes = base / cfg["takes_dir"]

    # 1. timings + trims
    timeline = []
    for idx, c in enumerate(cfg["clips"]):
        clip = takes / c["file"]
        if c.get("silent"):  # action take without speech: keep [start, end] as is, no captions
            a, b = c.get("start", 0.0), c.get("end", duration(clip))
            timeline.append({"idx": idx, "clip": clip, "words": [], "keep": [(a, b)], "trim_start": 0.0})
            print(f"{idx:02d} {c['file']:22} silent {a:.2f}-{b:.2f}s")
            continue
        text = c.get("text") or script[c["take"]]
        heard = whisper_words(clip, cfg.get("language", "fr"))
        words = align(text, heard)
        clip_dur = duration(clip)
        trim_start = max(0.0, words[0]["s"] - PAD_IN)
        trim_end = min(clip_dur, words[-1]["e"] + PAD_OUT)
        on, off = speech_edges(clip, trim_start, trim_end)  # tighter, measured start/end of the voice
        trim_start, trim_end = max(trim_start, on - EDGE_IN), min(clip_dur, off + EDGE_OUT)
        keep = keep_intervals(clip, trim_start, trim_end, words=heard)
        for w in words:  # move word times onto the cut segment's timeline
            w["s"], w["e"] = remap(w["s"], keep), remap(w["e"], keep)
        kept = sum(b - a for a, b in keep)
        timeline.append({"idx": idx, "clip": clip, "words": words, "keep": keep, "trim_start": 0.0})
        print(f"{idx:02d} {c['file']:22} {clip_dur:5.2f}s -> {kept:5.2f}s ({len(keep)} pieces)")

    # 2. segments
    seg_list = []
    for t in timeline:
        seg = work / f"seg_{t['idx']:02d}.mp4"
        seg_list.append(seg)
        if args.stage in ("all", "segments") or not seg.exists():
            parts, labels = [], []
            for k, (a, b) in enumerate(t["keep"]):
                d = b - a
                parts.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{k}]")
                parts.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,aresample=48000,"
                             f"afade=t=in:d=0.015,afade=t=out:st={max(0, d - 0.025):.3f}:d=0.025[a{k}]")
                labels.append(f"[v{k}][a{k}]")
            parts.append(f"{''.join(labels)}concat=n={len(labels)}:v=1:a=1[vc][ac]")
            parts.append(f"[vc]scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5:5:5:0,fps={FPS},format=yuv420p,setsar=1[vo]")
            run(["ffmpeg", "-y", "-v", "error", "-i", str(t["clip"]), "-filter_complex", ";".join(parts),
                 "-map", "[vo]", "-map", "[ac]",
                 "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                 "-ac", "2", str(seg)])
    offset = 0.0
    for t, seg in zip(timeline, seg_list):
        t["offset"] = offset
        t["dur"] = duration(seg)
        offset += t["dur"]
    total = offset
    print(f"total {total:.2f}s")

    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{s.name}'\n" for s in seg_list), encoding="utf-8")
    assembled = work / "assembled.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", concat.name, "-c", "copy", assembled.name],
        cwd=work)

    # 3. captions
    fonts = work / "fonts"
    fonts.mkdir(exist_ok=True)
    font_src = (base / cfg["font_file"]).resolve()
    shutil.copy(font_src, fonts / font_src.name)
    from PIL import ImageFont
    font_name = ImageFont.truetype(str(font_src), 10).getname()[0]
    cap_y = cfg.get("caption_y", CAPTION_Y)  # move captions up when something sits at the default height
    write_ass(work / "legendas.ass", timeline, font_name, total, cap_y)

    # 4. overlays + final render
    inputs = ["-i", assembled.name]
    chain, last = [], "0:v"
    for k, ov in enumerate(cfg.get("overlays", [])):
        if ov.get("mode") == "patch":  # fixed RGBA image at x,y over the whole video (e.g. sharp product label)
            card = work / f"card_{k}.png"
            shutil.copy(base / ov["image"], card)
            inputs += ["-loop", "1", "-i", card.name]
            # optional time range by clip: from the start of clip "from_clip" to the start of clip "to_clip"
            # (e.g. the question box of the Caixinha format, only during the hook)
            enable = ""
            if "from_clip" in ov or "to_clip" in ov:
                a = timeline[ov["from_clip"]]["offset"] if "from_clip" in ov else 0.0
                b = timeline[ov["to_clip"]]["offset"] if "to_clip" in ov else total
                enable = f":enable='between(t,{a:.2f},{b:.2f})'"
            chain.append(f"[{last}][{k + 1}:v]overlay={ov['x']}:{ov['y']}{enable}:shortest=1[v{k}]")
            last = f"v{k}"
            print(f"patch {ov['image']} at {ov['x']},{ov['y']}{enable}")
            continue
        t = timeline[ov["clip_index"]]
        ws = t["words"]
        first = next(w for w in ws if norm(w["w"]) == norm(ov["from_word"]))
        later = [w for w in ws if w["s"] > first["s"] and norm(w["w"]) == norm(ov["to_word"])]
        a = t["offset"] + first["s"] - t["trim_start"] - 0.05
        b = t["offset"] + (later[0]["s"] if later else ws[-1]["e"]) - t["trim_start"] - 0.05
        card = work / f"card_{k}.png"
        if ov.get("mode") == "full":  # full-screen B-roll image (cropped to 9:16)
            make_full(base / ov["image"], card)
            x, y = 0, 0
        else:
            cw, ch = make_card(base / ov["image"], card, width=ov.get("width", 430), aspect=ov.get("aspect", 4 / 3))
            # default: card over the torso, below her chin, just above the caption
            x, y = ov.get("x", (W - cw) // 2), ov.get("y", cap_y - 52 - ch)
        inputs += ["-loop", "1", "-i", card.name]
        chain.append(f"[{last}][{k + 1}:v]overlay={x}:{y}:enable='between(t,{a:.2f},{b:.2f})':shortest=1[v{k}]")
        last = f"v{k}"
        print(f"overlay {ov['image']}: {a:.2f}-{b:.2f}s")
    chain.append(f"[{last}]ass=legendas.ass:fontsdir=fonts[vout]")
    out = (base / cfg["output"]).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = work / "final.mp4"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(chain), "-map", "[vout]", "-map", "0:a",
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{total:.3f}",
         tmp_out.name], cwd=work)
    shutil.copy(tmp_out, out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
