"""Compose a static ad image from a JSON layout: photo, sharp product label, bands, seals and text.

The image model (Nano Banana) draws only the photo. Every word on the final ad is drawn here, so the
text is sharp and spelled right, and changing a price or a line costs nothing.

Usage (from the project root):
  python -I -X utf8 tools/compor_imagem.py "Criativo NN/imagem.json"

Layout file (paths relative to the project root; colors "#RRGGBB" or "#RRGGBBAA"):
{
  "size": [1080, 1350], "background": "#000000", "out": "Criativo NN/imagens/final_v1.png",
  "layers": [
    {"type": "image", "src": "...png", "box": [x, y, w, h], "blend": "lighten"},  # cover-fit; blend optional
    {"type": "rotulo", "src": "Referências/...png", "base": "...png", "box": [x, y, w, h],
     "src_pouch": [cx, top, width], "dst_pouch": [[cx, top, width], ...],
     "rows": [[sy0, sy1, xf0, xf1], ...]},                                  # paste the sharp label (see below)
    {"type": "rect", "box": [x, y, w, h], "fill": "#A0281E"},
    {"type": "line", "xy": [x0, y0, x1, y1], "fill": "#B8923A", "width": 3},
    {"type": "circle", "center": [x, y], "r": 90, "fill": "#C9A13B", "outline": "#8C6A1F", "width": 4},
    {"type": "text", "text": "...", "font": "georgiab.ttf", "size": 80, "fill": "#1A1A1A",
     "xy": [x, y], "anchor": "ma", "align": "center", "max_width": 900, "tracking": 0,
     "line_spacing": 1.15, "fit": false, "bg": "#FFFFFF", "pad": [20, 10], "emoji": false}
  ]
}
"transparent": true at the top level keeps the background transparent (PNG overlay for montar.py).
bg/pad draw a filled box behind each text line; "emoji": true renders color emoji (font seguiemj.ttf).

rotulo: the photo is first placed by an "image" layer; "rotulo" pastes the approved pouch label over each
pouch in that photo. "base" + "box" tell where the photo sits on the canvas. src_pouch is the pouch in the
source image (center x, top y, width at the top); each dst_pouch is the same in the base photo's own
pixels. Each row band [sy0, sy1, xf0, xf1] copies source rows sy0..sy1 and only the horizontal fraction
xf0..xf1 of the pouch width (use a narrower band where props cover the pouch edges). The paste is cut to
a soft-edged rectangle and color-matched to the pouch in the photo.

Fonts: a bare file name is looked up in assets/fonts/ and then C:/Windows/Fonts/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
FONT_DIRS = [ROOT / "assets" / "fonts", Path("C:/Windows/Fonts")]


def color(c: str) -> tuple:
    c = c.lstrip("#")
    vals = tuple(int(c[i:i + 2], 16) for i in range(0, len(c), 2))
    return vals if len(vals) == 4 else vals + (255,)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    p = Path(name)
    if not p.is_absolute():
        for d in FONT_DIRS:
            if (d / name).exists():
                p = d / name
                break
    return ImageFont.truetype(str(p), size)


def cover(img: Image.Image, w: int, h: int) -> Image.Image:
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def red_mask(a: np.ndarray) -> np.ndarray:
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return (r > 90) & (r - g > 55) & (r - b > 45) & (g < 110)


def pouch_silhouette(a: np.ndarray, cx: int, top: int) -> np.ndarray:
    """Filled pouch shape: the red component under (cx, top + 20), holes (the printed label) filled."""
    m = ndimage.binary_closing(red_mask(a), iterations=4)
    lab, _ = ndimage.label(m)
    k = lab[min(top + 20, a.shape[0] - 1), cx]
    if k == 0:
        return m
    return ndimage.binary_fill_holes(lab == k)


def paste_label(canvas: Image.Image, L: dict) -> None:
    src = Image.open(ROOT / L["src"]).convert("RGB")
    base = Image.open(ROOT / L["base"]).convert("RGB")
    bx, by, bw, bh = L["box"]
    bs = max(bw / base.width, bh / base.height)  # same cover-fit as the "image" layer
    offx, offy = (base.width * bs - bw) / 2, (base.height * bs - bh) / 2
    sa = np.asarray(src)
    scx, stop, sw = L["src_pouch"]
    base_a = np.asarray(base)
    for dcx, dtop, dw in L["dst_pouch"]:
        r = dw / sw  # source px -> base px
        s = r * bs  # source px -> canvas px
        # one light/color match per pouch: per-channel mean/std of the first band (same layout in the
        # source and in the photo, so the stats are comparable); one transform for all bands, no seams
        sy0, sy1, xf0, xf1 = L["rows"][0]
        sx0, sx1 = int(scx - sw / 2 + xf0 * sw), int(scx - sw / 2 + xf1 * sw)
        src_px = sa[sy0:sy1, sx0:sx1].reshape(-1, 3).astype(float)
        tx0, ty0 = int(dcx + (sx0 - scx) * r), int(dtop + (sy0 - stop) * r)
        tx1, ty1 = int(dcx + (sx1 - scx) * r), int(dtop + (sy1 - stop) * r)
        tgt = base_a[max(ty0, 0):ty1, max(tx0, 0):tx1].reshape(-1, 3).astype(float)
        rows = L["rows"]
        for i, (sy0, sy1, xf0, xf1) in enumerate(rows):
            if i + 1 < len(rows) and rows[i + 1][0] <= sy1:
                sy1 += 8  # overlap the next band so the soft edges do not leave a seam line
            sx0 = int(scx - sw / 2 + xf0 * sw)
            sx1 = int(scx - sw / 2 + xf1 * sw)
            crop = sa[sy0:sy1, sx0:sx1].astype(float)
            if len(tgt):
                crop = (crop - src_px.mean(0)) / (src_px.std(0) + 1e-6) * tgt.std(0) + tgt.mean(0)
            crop = Image.fromarray(np.clip(crop, 0, 255).astype(np.uint8))
            w, h = max(1, round(crop.width * s)), max(1, round(crop.height * s))
            crop = crop.resize((w, h), Image.LANCZOS)
            # rectangular band with soft edges: keep the bands inside the printed area of the pouch
            # (xf0..xf1 away from the pouch edges, rows above any prop in the source photo)
            mask = Image.new("L", (w, h), 0)
            ImageDraw.Draw(mask).rectangle([2, 2, w - 3, h - 3], fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(1.5))
            cx_canvas = bx + dcx * bs - offx
            top_canvas = by + dtop * bs - offy
            x = round(cx_canvas + (sx0 - scx) * s)
            y = round(top_canvas + (sy0 - stop) * s)
            canvas.paste(crop, (x, y), mask)


def wrap(draw: ImageDraw.ImageDraw, text: str, f, max_width: int | None, tracking: int) -> list[str]:
    lines = []
    for para in text.split("\n"):
        if not max_width:
            lines.append(para)
            continue
        cur = ""
        for word in para.split(" "):
            test = (cur + " " + word).strip()
            if text_width(draw, test, f, tracking) <= max_width or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def text_width(draw, s: str, f, tracking: int) -> float:
    if not tracking:
        return draw.textlength(s, font=f)
    return sum(draw.textlength(ch, font=f) for ch in s) + tracking * max(0, len(s) - 1)


def draw_text(canvas: Image.Image, L: dict) -> None:
    draw = ImageDraw.Draw(canvas)
    size, tracking = L["size"], L.get("tracking", 0)
    f = font(L["font"], size)
    mw = L.get("max_width")
    if L.get("fit") and mw:  # shrink until the longest line fits
        while size > 8 and max(text_width(draw, ln, f, tracking) for ln in L["text"].split("\n")) > mw:
            size -= 2
            f = font(L["font"], size)
        lines = L["text"].split("\n")
    else:
        lines = wrap(draw, L["text"], f, mw, tracking)
    x, y = L["xy"]
    anchor = L.get("anchor", "la")
    fill = color(L.get("fill", "#000000"))
    asc, desc = f.getmetrics()
    lh = (asc + desc) * L.get("line_spacing", 1.15)
    emoji = L.get("emoji", False)  # color emoji fonts (seguiemj.ttf) need embedded_color
    for i, ln in enumerate(lines):
        w = text_width(draw, ln, f, tracking)
        lx = x - w / 2 if anchor[0] == "m" else x - w if anchor[0] == "r" else x
        ly = y + i * lh
        if L.get("bg"):  # filled box behind the line, "pad": [horizontal, vertical]
            px, py = L.get("pad", [20, 10])
            top, bottom = ly + asc * 0.18, ly + asc + desc * 0.25
            draw.rectangle([lx - px, top - py, lx + w + px, bottom + py], fill=color(L["bg"]))
        if not tracking:
            draw.text((lx, ly), ln, font=f, fill=fill, embedded_color=emoji)
        else:
            for ch in ln:
                draw.text((lx, ly), ch, font=f, fill=fill)
                lx += draw.textlength(ch, font=f) + tracking


def main() -> int:
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    W, H = spec["size"]
    transparent = spec.get("transparent", False)  # PNG overlay for the montage ("patch" mode)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0) if transparent else color(spec.get("background", "#FFFFFF")))
    for L in spec["layers"]:
        t = L["type"]
        if t == "image":
            x, y, w, h = L["box"]
            img = cover(Image.open(ROOT / L["src"]).convert("RGB"), w, h)
            if L.get("blend") == "lighten":  # e.g. white ink on black over a dark canvas
                img = ImageChops.lighter(canvas.crop((x, y, x + w, y + h)).convert("RGB"), img)
            canvas.paste(img, (x, y))
        elif t == "rotulo":
            paste_label(canvas, L)
        elif t == "rect":
            x, y, w, h = L["box"]
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(layer).rectangle([x, y, x + w - 1, y + h - 1], fill=color(L["fill"]))
            canvas = Image.alpha_composite(canvas, layer)
        elif t == "line":
            ImageDraw.Draw(canvas).line(L["xy"], fill=color(L["fill"]), width=L.get("width", 2))
        elif t == "circle":
            cx, cy = L["center"]
            r = L["r"]
            ImageDraw.Draw(canvas).ellipse([cx - r, cy - r, cx + r, cy + r], fill=color(L["fill"]),
                                           outline=color(L["outline"]) if L.get("outline") else None,
                                           width=L.get("width", 0))
        elif t == "text":
            draw_text(canvas, L)
        else:
            raise SystemExit(f"unknown layer type: {t}")
    out = ROOT / spec["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    (canvas if transparent else canvas.convert("RGB")).save(out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
