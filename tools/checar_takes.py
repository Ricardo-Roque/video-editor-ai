"""Check generated takes against the script: transcribe each take locally and compare to the expected line.

Usage:
  python tools/checar_takes.py --config "Criativo 01/takes_config.json" --from T07 --to T30 [--model medium]

Reports word similarity, whether speech runs to the very end (possible cut-off) and saves
word timestamps to <take>.words.json next to each video (used later for captions and trimming).
"""
import argparse
import difflib
import json
import pathlib
import re
import subprocess
import sys
import unicodedata

import numpy as np
from faster_whisper import WhisperModel

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lote_takes import ROOT, parse_rows  # noqa: E402


def norm(s: str) -> list[str]:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", s)


def load_audio(path: pathlib.Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--from", dest="start", required=True)
    ap.add_argument("--to", dest="end", required=True)
    ap.add_argument("--model", default="medium")
    args = ap.parse_args()

    cfg_path = ROOT / args.config
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    base = cfg_path.parent
    num = lambda t: int(re.match(r"T(\d+)", t).group(1))
    rows = [r for r in parse_rows(base / cfg["script"]) if num(args.start) <= num(r[0]) <= num(args.end)]

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    for take, _, expected in rows:
        video = base / cfg["out_dir"] / f'{take}{cfg.get("out_suffix", "")}.mp4'
        if not video.exists():
            print(f"{take}: MISSING")
            continue
        audio = load_audio(video)
        dur = len(audio) / 16000
        segs, _ = model.transcribe(audio, language=cfg.get("language", "fr"), beam_size=5, word_timestamps=True)
        words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in s.words]
        got = " ".join(w["w"] for w in words)
        sim = difflib.SequenceMatcher(None, norm(expected), norm(got)).ratio()
        last_end = words[-1]["e"] if words else 0
        flag = []
        if sim < 0.85:
            flag.append("TEXT MISMATCH")
        if dur - last_end < 0.15:
            flag.append("POSSIBLE CUT-OFF")
        video.with_suffix(".words.json").write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{take}: sim={sim:.2f} speech={words[0]['s'] if words else 0:.1f}-{last_end:.1f}s of {dur:.1f}s "
              f"{' '.join(flag) or 'OK'}")
        if flag:
            print(f"   expected: {expected}\n   got:      {got}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
