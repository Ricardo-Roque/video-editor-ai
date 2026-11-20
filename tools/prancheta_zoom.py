"""Render a sharp still image (e.g. an infographic board) as a 1080x1920 video with a smooth camera move,
using the audio of a generated take. Use it when the video model blurs or deforms small text.

Usage:
  python -I -X utf8 tools/prancheta_zoom.py --audio TAKE.mp4 --out OUT.mp4 \
      --image 0:Q1a.png [--image 4.3:Q1b.png] \
      --key 0:1.0:688 --key 3:1.3:512 --key end:1.35:512 \
      [--head-video 4.8]

  --image T:PATH   image shown from time T (seconds) on.
  --key T:Z:CY     camera keyframe: zoom Z (1 = whole width) centred vertically on CY (source image pixels).
                   T may be "end". Moves between keyframes are eased (smoothstep).
  --head-video S   keep the first S seconds of the take's own video, then switch to the image.
"""
import argparse
import subprocess

from PIL import Image

W, H, FPS = 1080, 1920, 30


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout
    return float(out)


def ease(a):
    return a * a * (3 - 2 * a)


def camera(keys, t):
    if t <= keys[0][0]:
        return keys[0][1:]
    for (t0, z0, c0), (t1, z1, c1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            a = ease((t - t0) / (t1 - t0)) if t1 > t0 else 1.0
            return z0 + (z1 - z0) * a, c0 + (c1 - c0) * a
    return keys[-1][1:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--image", action="append", required=True)
    ap.add_argument("--key", action="append", required=True)
    ap.add_argument("--head-video", type=float, default=0.0)
    args = ap.parse_args()

    total = duration(args.audio)
    head = args.head_video
    dur = total - head
    images = []
    for spec in args.image:
        t, path = spec.split(":", 1)
        im = Image.open(path).convert("RGB")
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)  # 2x source keeps text crisp after the move
        images.append((float(t), im))
    keys = []
    for spec in args.key:
        t, z, cy = spec.split(":")
        keys.append((dur if t == "end" else float(t), float(z), float(cy) * 2))
    keys.sort()

    body = args.out + ".body.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", body],
                           stdin=subprocess.PIPE)
    n = round(dur * FPS)
    for i in range(n):
        t = i / FPS
        im = [img for t0, img in images if t0 <= t][-1] if any(t0 <= t for t0, _ in images) else images[0][1]
        z, cy = camera(keys, t)
        vw = im.width / z
        vh = vw * H / W
        if vh > im.height:
            vh = im.height
            vw = vh * W / H
        cx = im.width / 2
        x0 = min(max(cx - vw / 2, 0), im.width - vw)
        y0 = min(max(cy - vh / 2, 0), im.height - vh)
        frame = im.transform((W, H), Image.EXTENT, (x0, y0, x0 + vw, y0 + vh), Image.BICUBIC)
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    enc.wait()

    if head > 0:
        flt = (f"[0:v]trim=0:{head},setpts=PTS-STARTPTS,scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1[a];"
               f"[1:v]setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]")
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", args.audio, "-i", body, "-filter_complex", flt,
               "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-shortest", args.out]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", body, "-i", args.audio, "-map", "0:v", "-map", "1:a",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", args.out]
    subprocess.run(cmd, check=True)
    import os
    os.remove(body)
    print(args.out)


if __name__ == "__main__":
    main()
