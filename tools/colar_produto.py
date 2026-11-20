"""Make a sharp product-label patch to paste over takes where the video model warps the label text.

The pouch must stay still in the takes (static camera, pouch standing on a table). The patch is cut from the
approved still (the take's source image), scaled to the final 1080x1920 frame, aligned to a real frame of the
take by brute-force search, colour-matched to the take, and given a feathered rounded-rectangle alpha mask.
The output PNG goes into montagem.json as an overlay with "mode": "patch" and the printed x, y.

Usage:
  python -I -X utf8 tools/colar_produto.py --image "Criativo 10/imagens/cenas/B1_v1.png" \
      --take "Criativo 10/takes/T01_360p_v1.mp4" --box 478,780,728,1172 --out "Criativo 10/imagens/cenas/pacote_patch.png"

--box is x0,y0,x1,y1 in the still's pixels, slightly inside the pouch edges.
"""
import argparse
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920


def frame_at(video: str, t: float) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", video, "-frames:v", "1",
                          "-vf", f"scale={W}:{H}:flags=lanczos", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--take", required=True)
    ap.add_argument("--box", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--t", type=float, default=1.0, help="time of the take frame used for alignment")
    ap.add_argument("--search", type=int, default=30)
    args = ap.parse_args()

    x0, y0, x1, y1 = map(int, args.box.split(","))
    still = Image.open(args.image).convert("RGB")
    sw, sh = still.size
    # the video model centre-crops the still to 9:16 and scales it to the frame
    crop_h = sw * H / W
    off_y = (sh - crop_h) / 2
    s = W / sw
    px, py = round(x0 * s), round((y0 - off_y) * s)
    pw, ph = round((x1 - x0) * s), round((y1 - y0) * s)
    patch = np.asarray(still.crop((x0, y0, x1, y1)).resize((pw, ph), Image.LANCZOS)).astype(np.float32)

    frame = frame_at(args.take, args.t)
    g = patch.mean(2)
    best = None
    for dy in range(-args.search, args.search + 1, 2):
        for dx in range(-args.search, args.search + 1, 2):
            X, Y = px + dx, py + dy
            if X < 0 or Y < 0 or X + pw > W or Y + ph > H:
                continue
            sad = np.abs(frame[Y:Y + ph, X:X + pw].mean(2) - g)[::3, ::3].mean()
            if best is None or sad < best[0]:
                best = (sad, X, Y)
    _, X, Y = best
    for dy in (-1, 0, 1):  # refine to 1 px
        for dx in (-1, 0, 1):
            sad = np.abs(frame[Y + dy:Y + dy + ph, X + dx:X + dx + pw].mean(2) - g)[::3, ::3].mean()
            if sad < best[0]:
                best = (sad, X + dx, Y + dy)
    sad, X, Y = best

    # colour match: per-channel gain so the patch has the take's brightness and tint
    region = frame[Y:Y + ph, X:X + pw]
    gain = region.reshape(-1, 3).mean(0) / np.maximum(patch.reshape(-1, 3).mean(0), 1)
    patch = np.clip(patch * gain, 0, 255).astype(np.uint8)

    feather = max(4, pw // 40)
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle((feather, feather, pw - feather, ph - feather), radius=feather * 3, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather / 2))
    out = Image.fromarray(patch).convert("RGBA")
    out.putalpha(mask)
    out.save(args.out)
    print(f"x={X} y={Y} size={pw}x{ph} sad={sad:.1f} gain={np.round(gain, 3).tolist()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
