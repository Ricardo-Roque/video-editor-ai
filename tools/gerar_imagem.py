"""Generate or edit an image with Nano Banana (Gemini image models) via OpenRouter.

Usage:
  python tools/gerar_imagem.py --prompt "..." --out path.png [--ref img1.png --ref img2.jpg]
                               [--model google/gemini-2.5-flash-image] [--aspect 9:16]

Reads OPENROUTER_API_KEY from the environment or from a .env file at the project root.
Reference images (--ref) are sent alongside the prompt for character consistency or edits.
"""
import argparse
import base64
import json
import mimetypes
import os
import pathlib
import sys

import requests
from dotenv import load_dotenv

ROOT = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DEFAULT_MODEL = os.getenv("IMAGE_MODEL", "google/gemini-nano-banana-2.1")


def to_data_url(path: str) -> str:
    mime = mimetypes.guess_type(path)[0] or "image/png"
    data = base64.b64encode(pathlib.Path(path).read_bytes()).decode()
    return f"data:{mime};base64,{data}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--aspect", default="9:16")
    args = ap.parse_args()

    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        print("OPENROUTER_API_KEY not set (environment or .env)", file=sys.stderr)
        return 2

    content = [{"type": "text", "text": args.prompt}]
    for ref in args.ref:
        content.append({"type": "image_url", "image_url": {"url": to_data_url(ref)}})

    body = {
        "model": args.model,
        "messages": [{"role": "user", "content": content}],
        "modalities": ["image", "text"],
        "image_config": {"aspect_ratio": args.aspect},
    }
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        data=json.dumps(body),
        timeout=300,
    )
    if r.status_code != 200:
        print(f"HTTP {r.status_code}: {r.text[:1000]}", file=sys.stderr)
        return 1

    msg = r.json()["choices"][0]["message"]
    images = msg.get("images") or []
    if not images:
        print("No image returned. Model text:", msg.get("content"), file=sys.stderr)
        return 1

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    for i, img in enumerate(images):
        url = img["image_url"]["url"]
        raw = base64.b64decode(url.split(",", 1)[1])
        target = out if i == 0 else out.with_name(f"{out.stem}_{i}{out.suffix}")
        target.write_bytes(raw)
        print(target)
    usage = r.json().get("usage")
    if usage:
        print("usage:", json.dumps(usage))
    return 0


if __name__ == "__main__":
    sys.exit(main())
