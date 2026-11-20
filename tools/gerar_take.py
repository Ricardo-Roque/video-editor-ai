"""Generate a video take from a start image via OpenRouter's video API.

Usage:
  python tools/gerar_take.py --image start.png --prompt "..." --out take.mp4
                             [--duration 8] [--model google/gemini-omni-1.2-flash]
                             [--size 720x1280] [--seed 42] [--no-audio]

Reads OPENROUTER_API_KEY from the environment or from a .env file at the project root.
Submits the job, polls until it finishes, downloads the MP4 and prints the cost.
"""
import argparse
import base64
import json
import mimetypes
import os
import pathlib
import sys
import time

import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
API = "https://openrouter.ai/api/v1/videos"


def to_data_url(path: str) -> str:
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(pathlib.Path(path).read_bytes()).decode()}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image")
    ap.add_argument("--prompt")
    ap.add_argument("--out", required=True)
    ap.add_argument("--resume", metavar="JOB_ID", help="download an already-submitted job instead of submitting")
    ap.add_argument("--duration", type=int, default=8)
    ap.add_argument("--model", default=os.getenv("VIDEO_MODEL", "google/gemini-omni-1.2-flash"))
    ap.add_argument("--size", default="720x1280")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--timeout", type=int, default=900, help="max seconds to wait for the job")
    args = ap.parse_args()

    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        print("OPENROUTER_API_KEY not set (environment or .env)", file=sys.stderr)
        return 2
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if args.resume:
        return finish(args.resume, args.out, headers, args.timeout)
    if not (args.image and args.prompt):
        ap.error("--image and --prompt are required unless --resume is given")

    body = {
        "model": args.model,
        "prompt": args.prompt,
        "duration": max(3, min(15, args.duration)),
        "aspect_ratio": "9:16",
        "size": args.size,
        "generate_audio": not args.no_audio,
        "frame_images": [
            {"type": "image_url", "frame_type": "first_frame", "image_url": {"url": to_data_url(args.image)}}
        ],
    }
    if args.seed is not None:
        body["seed"] = args.seed

    for attempt in range(8):
        r = requests.post(API, headers=headers, data=json.dumps(body), timeout=120)
        # OpenRouter rejects new jobs while too many are in flight; wait and retry (not billed).
        if r.status_code in (200, 201, 202) or "budget_exhausted" not in r.text:
            break
        wait = int(r.headers.get("Retry-After", "60") or 60)
        print(f"in-flight budget full, retrying in {wait}s", file=sys.stderr, flush=True)
        time.sleep(wait)
    if r.status_code not in (200, 201, 202):
        print(f"submit HTTP {r.status_code}: {r.text[:1500]}", file=sys.stderr)
        return 1
    job = r.json()
    job_id = job["id"]
    print("job", job_id, flush=True)
    # Keep a log so a take can be recovered (--resume) if this process dies before downloading.
    with open(ROOT / "tools" / "jobs.log", "a", encoding="utf-8") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{job_id}\t{args.out}\n")
    return finish(job_id, args.out, headers, args.timeout)


def finish(job_id: str, out_path: str, headers: dict, timeout: int) -> int:

    deadline = time.time() + timeout
    while True:
        s = requests.get(f"{API}/{job_id}", headers=headers, timeout=60).json()
        status = s.get("status")
        if status in ("completed", "failed", "cancelled", "expired"):
            break
        if time.time() > deadline:
            print(f"timeout waiting for job {job_id} (last status {status})", file=sys.stderr)
            return 1
        time.sleep(10)

    if status != "completed":
        print(f"job {status}: {json.dumps(s.get('error') or s)[:1500]}", file=sys.stderr)
        return 1

    v = requests.get(f"{API}/{job_id}/content", headers=headers, timeout=300)
    v.raise_for_status()
    out = pathlib.Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(v.content)
    print(out)
    print("usage:", json.dumps(s.get("usage")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
