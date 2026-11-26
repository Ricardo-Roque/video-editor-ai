"""Render a take as a sequence of illustrations with camera moves (zoom + pan), punch shakes and pop-in
labels, keeping the take's own audio. Made for the illustrated narrated format (Criativo 20): the voice comes
from a generated take, the picture is built locally. The result goes into montar.py like any take.

Usage:
  python -I -X utf8 tools/ilustrar_take.py "Criativo 20/ilustracao/T01.json"

Spec (paths relative to the creative folder, i.e. the parent of the spec's folder; times in seconds of the
untrimmed take, so they match <take>.words.json):
  {
    "audio": "takes/T01_360p_v1.mp4",
    "out": "takes/T01_ilus_v1.mp4",
    "font": "../assets/fonts/Montserrat-ExtraBold.ttf",
    "segments": [
      {"start": 0, "image": "imagens/cenas/H1_v1.png",
       "keys": [[0, 1.0, 384, 688], [1.36, 1.5, 430, 720]],      # [t, zoom, cx, cy] in source pixels, eased
       "shake": [1.36, 0.3, 10],                                    # [t, duration, amplitude in source px]
       "overlays": [
         {"type": "badge", "text": "1", "x": 95, "y": 420, "r": 34, "t": 2.6},
         {"type": "label", "text": "ÉTAPE ?", "x": 380, "y": 470, "size": 64, "t": 4.9, "pointer": true},
         {"type": "text", "text": "15", "x": 210, "y": 440, "size": 150, "color": [40, 40, 40], "t": 0.5}
       ]}
    ]
  }
A segment lasts until the next one starts (the last one until the end of the audio). Overlays pop in at t
(scale 1.35 -> 1 in 0.15 s) and stay until the segment ends.
"""
import json
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS, UP = 1080, 1920, 30, 2  # images are upscaled UP x before cropping so zooms stay sharp
RED, WHITE = (178, 18, 24), (255, 255, 255)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout
    return float(out)


def ease(a):
    return a * a * (3 - 2 * a)


def camera(keys, t):
    if t <= keys[0][0]:
        return keys[0][1:]
    for k0, k1 in zip(keys, keys[1:]):
        if k0[0] <= t <= k1[0]:
            a = ease((t - k0[0]) / (k1[0] - k0[0])) if k1[0] > k0[0] else 1.0
            return [x0 + (x1 - x0) * a for x0, x1 in zip(k0[1:], k1[1:])]
    return keys[-1][1:]


def draw_overlay(img, ov, scale, font_path):
    d = ImageDraw.Draw(img)
    x, y = ov["x"] * UP, ov["y"] * UP
    if ov["type"] == "badge":
        r = ov.get("r", 34) * UP * scale
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=WHITE, width=int(5 * UP * scale))
        f = ImageFont.truetype(font_path, int(r * 1.15))
        d.text((x, y + r * 0.04), ov["text"], font=f, fill=WHITE, anchor="mm")
    elif ov["type"] == "label":
        f = ImageFont.truetype(font_path, int(ov.get("size", 60) * UP * scale))
        l, t, r_, b = d.textbbox((x, y), ov["text"], font=f, anchor="mm")
        pad = 22 * UP * scale
        box = [l - pad, t - pad * 0.8, r_ + pad, b + pad * 0.8]
        d.rounded_rectangle(box, radius=int(14 * UP * scale), fill=RED)
        if ov.get("pointer"):
            s = 22 * UP * scale
            d.polygon([(x - s, box[3] - 1), (x + s, box[3] - 1), (x, box[3] + s * 1.2)], fill=RED)
        d.text((x, y), ov["text"], font=f, fill=WHITE, anchor="mm")
    elif ov["type"] == "text":  # plain text, e.g. a number on a phone screen
        f = ImageFont.truetype(font_path, int(ov.get("size", 60) * UP * scale))
        d.text((x, y), ov["text"], font=f, fill=tuple(ov.get("color", RED)), anchor="mm")


def main():
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base = spec_path.parent.parent
    audio = base / spec["audio"]
    out = base / spec["out"]
    font_path = str(base / spec.get("font", "../assets/fonts/Montserrat-ExtraBold.ttf"))
    total = duration(audio)
    segs = spec["segments"]
    imgs = {}
    for s in segs:
        if s["image"] not in imgs:
            im = Image.open(base / s["image"]).convert("RGB")
            imgs[s["image"]] = im.resize((im.width * UP, im.height * UP), Image.LANCZOS)

    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", str(audio), "-map", "0:v", "-map", "1:a",
                           "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], stdin=subprocess.PIPE)
    rnd = random.Random(39)
    for n in range(math.ceil(total * FPS)):
        t = n / FPS
        seg = [s for s in segs if s["start"] <= t][-1]
        src = imgs[seg["image"]]
        z, cx, cy = camera(seg["keys"], t)
        sh = seg.get("shake")
        if sh and sh[0] <= t < sh[0] + sh[1]:
            k = 1 - (t - sh[0]) / sh[1]
            cx += rnd.uniform(-1, 1) * sh[2] * k
            cy += rnd.uniform(-1, 1) * sh[2] * k
        live = [o for o in seg.get("overlays", []) if o["t"] <= t]
        if live:
            src = src.copy()
            for o in live:
                a = min(1.0, (t - o["t"]) / 0.15)
                draw_overlay(src, o, 1.35 - 0.35 * ease(a), font_path)
        cw = src.width / z
        ch = cw * H / W
        if ch > src.height:
            ch = src.height
            cw = ch * W / H
        x0 = min(max(cx * UP - cw / 2, 0), src.width - cw)
        y0 = min(max(cy * UP - ch / 2, 0), src.height - ch)
        frame = src.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        ff.stdin.write(frame.tobytes())
    ff.stdin.close()
    ff.wait()
    print(out)


if __name__ == "__main__":
    main()
