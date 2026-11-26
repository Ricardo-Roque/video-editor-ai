"""Batch-generate takes from a script table (roteiro_fr.md) using tools/gerar_take.py.

Usage:
  python -I -X utf8 tools/lote_takes.py --config "Criativo 01/takes_config.json" --from T07 --to T30 [--dry-run]

The script table rows look like: | T07 | B1 | 5 | Spoken line ... |
Duration is derived from the word count (about 3 words per second) to avoid paying for silence.
"""
import argparse
import concurrent.futures as cf
import json
import math
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROW = re.compile(r"^\|\s*(T\d+[a-z]?)\s*\|\s*([^|]+?)\s*\|\s*\d+\s*\|\s*(.+?)\s*\|\s*$")


def parse_rows(md_path: pathlib.Path):
    rows = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            take, image, text = m.groups()
            image = image.split()[0]  # "H3 (+O1, O2 ...)" -> "H3"
            text = text.replace("⚠", "").strip()
            rows.append((take, image, text))
    return rows


def duration_for(text: str, words_per_sec: float, pad: float) -> int:
    words = len(text.split())
    return max(3, min(15, math.ceil(words / words_per_sec + pad)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--from", dest="start", required=True)
    ap.add_argument("--to", dest="end", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--only", help="comma-separated take ids inside the range")
    args = ap.parse_args()

    cfg_path = ROOT / args.config
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    base = cfg_path.parent
    rows = parse_rows(base / cfg["script"])
    num = lambda t: int(re.match(r"T(\d+)", t).group(1))
    rows = [r for r in rows if num(args.start) <= num(r[0]) <= num(args.end)]
    if args.only:  # e.g. "T02a,T03a": generate the "a" parts first, then the "b" parts from their last frame
        rows = [r for r in rows if r[0] in args.only.split(",")]

    jobs = []
    total_s = 0
    for take, image, text in rows:
        dur = duration_for(text, cfg.get("words_per_sec", 3.0), cfg.get("pad", 0.3))
        # Some models (e.g. Veo 3.1 Lite) only accept fixed clip lengths: round up to the next allowed one.
        allowed = sorted(cfg.get("durations", []))
        if allowed:
            dur = next((d for d in allowed if d >= dur), allowed[-1])
        total_s += dur
        persona = cfg["personas"][cfg["image_persona"][image]]
        # "say" lets off-screen narration avoid "She says", which made Veo add a woman on screen (Criativo 09).
        prompt = f'{persona["scene"]} {persona["voice"]} {cfg.get("say", "She says:")} "{text}" {cfg["suffix"]}'
        out = base / cfg["out_dir"] / f'{take}{cfg.get("out_suffix", "")}.mp4'
        jobs.append((take, base / cfg["images"][image], dur, prompt, out, persona.get("seed")))
        print(f"{take} {image:4} {dur:2}s  {text[:70]}")

    est = total_s * cfg["price_per_sec"]
    print(f"\n{len(jobs)} takes, {total_s}s billed, estimated ${est:.2f}")
    if args.dry_run:
        return 0

    def run(job):
        take, img, dur, prompt, out, seed = job
        if out.exists():
            return take, "skipped (exists)", 0.0
        cmd = [sys.executable, "-I", str(ROOT / "tools/gerar_take.py"), "--image", str(img), "--out", str(out),
               "--duration", str(dur), "--size", cfg["size"], "--prompt", prompt]
        if seed is not None:
            cmd += ["--seed", str(seed)]
        if cfg.get("model"):
            cmd += ["--model", cfg["model"]]
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        cost = 0.0
        m = re.search(r'"cost": ([0-9.]+)', p.stdout)
        if m:
            cost = float(m.group(1))
        status = "ok" if p.returncode == 0 else f"FAILED: {(p.stderr or p.stdout).strip()[-300:]}"
        return take, status, cost

    spent = 0.0
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for take, status, cost in ex.map(run, jobs):
            spent += cost
            print(f"{take}: {status} ${cost:.3f}", flush=True)
    print(f"\nspent ${spent:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
