"""Step 1 of a new creative: break down a reference video so it can be analysed (hook / body / CTA / scenes / variables).

Usage:
  python tools/analisar_referencia.py --video "Vídeo Bruto/<file>.mp4" --out "Criativo NN/referencia" [--language en]

Writes into --out:
  info.txt            resolution, fps, duration
  cortes.txt          detected scene cuts (hard cuts at 0.25, soft at 0.08)
  transcript.txt/json transcript with segment and word timestamps (faster-whisper "small")
  sheet_*.jpg         contact sheets, one frame per second with timestamps (6x4 per sheet)
  hook.jpg            first 18 s at 2 fps (the hook is where detail matters most)
  hook_3s.jpg         first 3 s at 4 fps (one frame every 0.25 s), with timestamps
  frame_XXs.jpg       one full-size frame per detected hard cut
  evidencias.md       measured evidence: cut rhythm, words in the first 3 s, speaking pace,
                      pauses, loudness and the level of any music bed under the voice

Automatic cut detection undercounts fast edits: treat cortes.txt as candidates and confirm them on the frames.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT = "assets/fonts/Montserrat-ExtraBold.ttf"  # relative to ROOT: ffmpeg filters choke on "C:" in paths
STAMP = f"drawtext=fontfile={FONT}:text='%{{pts\\:hms}}':x=4:y=4:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6"


def ff(*args):
    return subprocess.run(["ffmpeg", "-hide_banner", *args], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=ROOT)


def scene_cuts(video: str, threshold: float) -> list[float]:
    log = ff("-i", video, "-vf", f"select='gt(scene\\,{threshold})',showinfo", "-fps_mode", "vfr", "-f", "null", "-").stderr
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", log)]


def duration_of(video: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()
    return float(out or 0)


def loudness(video: str) -> str:
    log = ff("-i", video, "-af", "loudnorm=print_format=summary", "-f", "null", "-").stderr
    m = re.search(r"Input Integrated:\s*(-?[0-9.]+|-inf)", log)
    return f"{m.group(1)} LUFS" if m else "não medido"


def fmt(x: float) -> str:
    return f"{x:.2f}".replace(".", ",")


def db(x: np.ndarray) -> float:
    if x.size == 0:
        return float("nan")
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def cut_rhythm(cuts: list[float], dur: float) -> list[str]:
    """Shot count and mean shot length in the hook (0-3 s), the body and the last 20 %."""
    bounds = [0.0] + [c for c in cuts if 0 < c < dur] + [dur]
    shots = [(a, b) for a, b in zip(bounds, bounds[1:]) if b - a > 0.05]
    lines = [f"- Planos detectados: {len(shots)}; duração média do plano: {fmt(dur / max(len(shots), 1))} s."]
    zones = [("Hook (0–3 s)", 0.0, min(3.0, dur)), ("Corpo", min(3.0, dur), dur * 0.8), ("Final (últimos 20%)", dur * 0.8, dur)]
    for name, a, b in zones:
        if b <= a:
            continue
        inside = [c for c in cuts if a <= c < b]
        n = len(inside) + 1
        lines.append(f"- {name}: {len(inside)} cortes em {fmt(b - a)} s, plano médio de {fmt((b - a) / n)} s.")
    return lines


def speech_stats(segments: list[dict], audio: np.ndarray, sr: int) -> list[str]:
    words = [w for s in segments for w in s["words"]]
    if not words:
        return ["- Sem fala detectada."]
    lines = []
    first3 = [w["w"].strip() for w in words if w["s"] < 3.0]
    lines.append(f"- Palavras nos 3 primeiros segundos: {len(first3)} (\"{' '.join(first3)}\").")
    lines.append(f"- Primeira palavra em {fmt(words[0]['s'])} s.")
    span = words[-1]["e"] - words[0]["s"]
    lines.append(f"- Total: {len(words)} palavras em {fmt(span)} s de fala, {fmt(len(words) / max(span, 0.01))} palavras/s.")
    stop, comma = [], []
    for w, nxt in zip(words, words[1:]):
        gap = max(0.0, nxt["s"] - w["e"])
        t = w["w"].strip()
        if t.endswith((".", "!", "?")):
            stop.append(gap)
        elif t.endswith(","):
            comma.append(gap)
    if stop:
        lines.append(f"- Pausa média depois de ponto: {fmt(float(np.mean(stop)))} s ({len(stop)} pontos).")
    if comma:
        lines.append(f"- Pausa média depois de vírgula: {fmt(float(np.mean(comma)))} s ({len(comma)} vírgulas).")

    # Music bed: level in the gaps between words (>= 0.3 s) against the level while the voice speaks.
    mask = np.zeros(audio.size, dtype=bool)
    for w in words:
        mask[int(w["s"] * sr):int(w["e"] * sr)] = True
    gaps = np.zeros(audio.size, dtype=bool)
    edges = [(0.0, words[0]["s"])] + [(a["e"], b["s"]) for a, b in zip(words, words[1:])] + [(words[-1]["e"], audio.size / sr)]
    for a, b in edges:
        if b - a >= 0.3:
            gaps[int((a + 0.05) * sr):int((b - 0.05) * sr)] = True
    gap_s = gaps.sum() / sr
    voice_db, gap_db = db(audio[mask]), db(audio[gaps])
    if gap_s < 1.0:
        lines.append("- Fundo sob a voz: pouca pausa para medir (menos de 1 s sem fala).")
    else:
        diff = gap_db - voice_db
        if diff > -12:
            label = "fundo alto (música ou ambiente forte)"
        elif diff > -30:
            label = "fundo audível (provável trilha ou ambiente)"
        else:
            label = "praticamente silêncio nas pausas (só voz)"
        lines.append(f"- Fundo sob a voz: pausas a {fmt(diff)} dB em relação à voz, medido em {fmt(gap_s)} s de pausa: {label}. Confirmar ouvindo.")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--language", default=None, help="spoken language code (en, fr, pt...); auto-detect if omitted")
    args = ap.parse_args()

    out = pathlib.Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    video = str(pathlib.Path(args.video).resolve())

    info = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                           "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "compact", video],
                          capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    (out / "info.txt").write_text(info, encoding="utf-8")
    print(info)
    dur = duration_of(video)

    hard, soft = scene_cuts(video, 0.25), scene_cuts(video, 0.08)
    (out / "cortes.txt").write_text(
        "hard (0.25): " + " ".join(f"{t:.2f}" for t in hard) + "\n"
        "soft (0.08): " + " ".join(f"{t:.2f}" for t in soft) + "\n", encoding="utf-8")
    print(f"hard cuts: {len(hard)}  soft cuts: {len(soft)}")

    ff("-y", "-v", "error", "-i", video, "-vf", f"fps=1,scale=180:-1,{STAMP},tile=6x4", str(out / "sheet_%02d.jpg"))
    ff("-y", "-v", "error", "-i", video, "-t", "18", "-vf", "fps=2,scale=240:-1,tile=9x4", "-frames:v", "1",
       str(out / "hook.jpg"))
    ff("-y", "-v", "error", "-i", video, "-t", "3", "-vf", f"fps=4,scale=240:-1,{STAMP},tile=6x2", "-frames:v", "1",
       str(out / "hook_3s.jpg"))
    for t in [0.5] + [c + 0.3 for c in hard]:
        ff("-y", "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", str(out / f"frame_{t:06.2f}s.jpg"))

    sr = 16000
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segs, meta = model.transcribe(audio, language=args.language, word_timestamps=True, vad_filter=True)
    data = {"language": meta.language, "segments": []}
    lines = []
    for s in segs:
        data["segments"].append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
                                 "words": [{"w": w.word, "s": round(w.start, 2), "e": round(w.end, 2)} for w in s.words]})
        lines.append(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}")
    (out / "transcript.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "transcript.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"language: {meta.language}, {len(lines)} segments -> {out}")

    ev = [
        "# Evidências medidas",
        "",
        f"Vídeo: `{args.video}`. Duração: {fmt(dur)} s. Idioma detectado: {meta.language}.",
        "Gerado por `tools/analisar_referencia.py`. Os números abaixo são medidos; a leitura deles vai na quebra.",
        "",
        "## Ritmo de cortes",
        "",
        "Detector automático: conta a menos em edição rápida. Conferir cada corte nas folhas (`sheet_*.jpg`, `hook_3s.jpg`).",
        "",
        *cut_rhythm(hard, dur),
        f"- Cortes suaves (0,08) para conferir: {len(soft)}.",
        "",
        "## Fala",
        "",
        *speech_stats(data["segments"], audio, sr),
        "",
        "## Som",
        "",
        f"- Volume integrado: {loudness(video)}.",
        "",
        "## Conferido no olho (preencher)",
        "",
        "- Lista de cortes confirmada (tempo, antes → depois, duração do plano):",
        "- Texto na tela: fonte, tamanho (% da altura do quadro), posição, cor que codifica sentido, atraso em relação à fala:",
        "- Trilha e efeitos sonoros:",
        "",
    ]
    (out / "evidencias.md").write_text("\n".join(ev), encoding="utf-8")
    print(f"evidence -> {out / 'evidencias.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
