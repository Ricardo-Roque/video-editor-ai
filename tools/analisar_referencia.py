"""Step 1 of a new creative: break down a reference video so it can be analysed (hook / body / CTA / scenes).

Usage:
  python tools/analisar_referencia.py --video "Vídeo Bruto/<file>.mp4" --out "Criativo NN/referencia" [--language en]

Writes into --out:
  info.txt            resolution, fps, duration
  cortes.txt          detected scene cuts (hard cuts at 0.25, soft at 0.08)
  transcript.txt/json transcript with segment and word timestamps (faster-whisper "small")
  sheet_*.jpg         contact sheets, one frame every 3 s (8x3 per sheet)
  hook.jpg            first 18 s at 2 fps (the hook is where detail matters most)
  frame_XXs.jpg       one full-size frame per detected hard cut
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel


def ff(*args):
    return subprocess.run(["ffmpeg", "-hide_banner", *args], capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def scene_cuts(video: str, threshold: float) -> list[float]:
    log = ff("-i", video, "-vf", f"select='gt(scene\\,{threshold})',showinfo", "-fps_mode", "vfr", "-f", "null", "-").stderr
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", log)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--language", default=None, help="spoken language code (en, fr, pt...); auto-detect if omitted")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    video = args.video

    info = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                           "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "compact", video],
                          capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    (out / "info.txt").write_text(info, encoding="utf-8")
    print(info)

    hard, soft = scene_cuts(video, 0.25), scene_cuts(video, 0.08)
    (out / "cortes.txt").write_text(
        "hard (0.25): " + " ".join(f"{t:.2f}" for t in hard) + "\n"
        "soft (0.08): " + " ".join(f"{t:.2f}" for t in soft) + "\n", encoding="utf-8")
    print(f"hard cuts: {len(hard)}  soft cuts: {len(soft)}")

    ff("-y", "-v", "error", "-i", video, "-vf", "fps=1/3,scale=180:-1,tile=8x3", str(out / "sheet_%02d.jpg"))
    ff("-y", "-v", "error", "-i", video, "-t", "18", "-vf", "fps=2,scale=240:-1,tile=9x4", "-frames:v", "1",
       str(out / "hook.jpg"))
    for t in [0.5] + [c + 0.3 for c in hard]:
        ff("-y", "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", str(out / f"frame_{t:06.2f}s.jpg"))

    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
