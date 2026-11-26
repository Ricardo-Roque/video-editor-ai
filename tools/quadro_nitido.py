"""Replace the (AI-redrawn, often misspelled) board text in a take with the sharp text of its start image,
frame by frame, while hands, markers and hair that pass in front of the board stay from the take.

Usage:
  python -I -X utf8 tools/quadro_nitido.py --take "Criativo 11/takes/T05_360p_v2.mp4" \
      --image "Criativo 11/imagens/cenas/C5_v2.png" --region 0,55,360,305 \
      --out "Criativo 11/takes/T05_quadro_v1.mp4"

--region is x0,y0,x1,y1 in take pixels (360x640): the part of the board to replace.
How it works:
  1. Finds how the start image maps onto the take (the video model rescales/crops it slightly).
  2. Upscales the take to 1080x1920 and, inside the region, uses the sharp image (colour-matched to the frame)
     except where a skin/hair-coloured blob (plus a margin for the marker) covers the board.
  3. Copies the take's audio and its .words.json (so montar.py can use the output like a normal take).
The output is 1080x1920, so montar.py does not upscale it again.
"""
import argparse
import json
import pathlib
import shutil
import subprocess

import numpy as np
from PIL import Image, ImageFilter

OW, OH = 1080, 1920


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip().split(",")
    num, den = out[2].split("/")
    return int(out[0]), int(out[1]), out[2], float(num) / float(den)


def first_frame(path, w, h):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-frames:v", "1", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3)


def find_mapping(img, frame, w, h):
    """Scale (image height in take pixels) and crop offset that best match the frame's top band."""
    g = frame.mean(axis=2)[: int(h * 0.36)]
    best = None
    for H in range(h, int(h * 1.12), 2):
        W = round(img.width * H / img.height)
        if W < w:
            continue
        r = np.asarray(img.convert("L").resize((W, H), Image.LANCZOS), dtype=float)
        for dy in range(0, min(H - h, 30) + 1):
            for dx in range(0, min(W - w, 20) + 1):
                e = np.mean(np.abs(r[dy:dy + g.shape[0], dx:dx + w] - g))
                if best is None or e < best[0]:
                    best = (e, W, H, dx, dy)
    return best


def skin_mask(rgb):
    r, g, b = (rgb[..., i].astype(int) for i in range(3))
    skin = (r > 70) & (r > g + 10) & (g > b) & (r - b > 25) & (r < 250) & ~((r > 150) & (g < 90) & (b < 100))
    return skin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--take", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--region", required=True, help="x0,y0,x1,y1 in take pixels")
    ap.add_argument("--out", required=True)
    ap.add_argument("--margin", type=int, default=12, help="take pixels kept around hands/hair (covers the marker)")
    args = ap.parse_args()

    take, out = pathlib.Path(args.take), pathlib.Path(args.out)
    w, h, rate, fps = probe(take)
    img = Image.open(args.image).convert("RGB")
    f0 = first_frame(take, w, h)
    err, W, H, dx, dy = find_mapping(img, f0, w, h)
    print(f"mapping: image -> {W}x{H}, crop {dx},{dy} (err {err:.1f})")

    k = OW / w
    sharp = img.resize((round(W * k), round(H * k)), Image.LANCZOS)
    sharp = np.asarray(sharp, dtype=np.float32)[round(dy * k):round(dy * k) + OH, round(dx * k):round(dx * k) + OW]

    x0, y0, x1, y1 = (int(v) for v in args.region.split(","))
    X0, Y0, X1, Y1 = (round(v * k) for v in (x0, y0, x1, y1))
    region = np.zeros((h, w), bool)
    region[y0:y1, x0:x1] = True
    edge = Image.fromarray((region * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    region_soft = np.asarray(edge, dtype=np.float32) / 255
    # where the start image itself has a hand/marker/hair, the sharp copy would leave a frozen ghost: keep the take there
    img_small = np.asarray(Image.fromarray(sharp.astype(np.uint8)).resize((w, h), Image.LANCZOS))
    img_skin = skin_mask(img_small) & region
    img_skin = np.asarray(Image.fromarray((img_skin * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(2))) > 90

    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(take), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}",
                            "-r", rate, "-i", "-", "-i", str(take), "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
                            "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                            "-shortest", str(out)], stdin=subprocess.PIPE)
    n, covered = 0, 0
    while True:
        raw = dec.stdout.read(w * h * 3)
        if len(raw) < w * h * 3:
            break
        fr = np.frombuffer(raw, np.uint8).reshape(h, w, 3)
        skin = skin_mask(fr) & region
        # drop tiny specks (ink that happens to look skin-coloured): keep blobs only via blur threshold
        sk = Image.fromarray((skin * 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(2))
        skin = np.asarray(sk) > 90
        covered += skin.any()
        skin = skin | img_skin
        keep = Image.fromarray((skin * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * (args.margin // 2) + 1))
        keep = keep.filter(ImageFilter.GaussianBlur(2))
        alpha = region_soft * (1 - np.asarray(keep, dtype=np.float32) / 255)
        up = np.asarray(Image.fromarray(fr).resize((OW, OH), Image.LANCZOS), dtype=np.float32)
        # colour-match the sharp board to this frame (per channel gain on bright board pixels)
        sub_f = up[Y0:Y1, X0:X1]
        sub_s = sharp[Y0:Y1, X0:X1]
        board = (sub_s.min(axis=2) > 170) & (sub_f.min(axis=2) > 150)
        gain = (sub_f[board].mean(axis=0) / np.maximum(sub_s[board].mean(axis=0), 1)) if board.sum() > 500 else np.ones(3)
        a = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).resize((OW, OH), Image.BILINEAR),
                       dtype=np.float32)[..., None] / 255
        comp = up * (1 - a) + np.clip(sharp * gain, 0, 255) * a
        enc.stdin.write(comp.astype(np.uint8).tobytes())
        n += 1
    enc.stdin.close()
    enc.wait()
    dec.wait()
    words = take.with_suffix(".words.json")
    if words.exists():
        shutil.copy(words, out.with_suffix(".words.json"))
    print(f"{out}: {n} frames, hand/hair over the region in {covered}")


if __name__ == "__main__":
    main()
