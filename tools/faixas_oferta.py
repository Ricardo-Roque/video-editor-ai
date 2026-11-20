"""Draw the fixed promo banners of Criativos 11 and 12 as full-frame transparent PNGs (1080x1920).

They are pasted over the whole video with a montagem.json overlay {"mode": "patch", "x": 0, "y": 0}.

Usage:
  python -I -X utf8 tools/faixas_oferta.py --style stock --out "Criativo 11/imagens/cenas/O1_faixas_v1.png"
  python -I -X utf8 tools/faixas_oferta.py --style surstock --brand Cinnarae --out "Criativo 12/imagens/cenas/O1_faixas_v1.png"
"""
import argparse

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BOLD = "C:/Windows/Fonts/arialbd.ttf"
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
RED = (228, 30, 37, 255)


def text_w(draw, text, font):
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    return r - l


def emoji(img, ch, x, y, size):
    """Paste a colour emoji (Segoe UI Emoji renders at 109 px, then it is resized)."""
    f = ImageFont.truetype(EMOJI, 109)
    tmp = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((0, 0), ch, font=f, embedded_color=True)
    tmp = tmp.crop(tmp.getbbox()).resize((size, size), Image.LANCZOS)
    img.alpha_composite(tmp, (int(x), int(y)))


def box(img, x, y, text, font, fg, bg, pad=(18, 10), radius=6, emoji_ch=None):
    d = ImageDraw.Draw(img)
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    tw, th = r - l, b - t
    ew = th + 14 if emoji_ch else 0
    w, h = tw + ew + 2 * pad[0], th + 2 * pad[1]
    if x == "center":
        x = (W - w) // 2
    d.rounded_rectangle((x, y, x + w, y + h), radius, fill=bg)
    d.text((x + pad[0] - l, y + pad[1] - t), text, font=font, fill=fg)
    if emoji_ch:
        emoji(img, emoji_ch, x + pad[0] + tw + 10, y + pad[1] - 2, th + 4)
    return h


def stock(img):
    """Criativo 11: red '2 ACHETÉS = 1 OFFERT 🚨' over white 'DANS LA LIMITE DES STOCKS', top left."""
    f = ImageFont.truetype(BOLD, 50)
    y = 150
    h = box(img, 30, y, "2 ACHETÉS = 1 OFFERT", f, "white", RED, emoji_ch="🚨")
    box(img, 30, y + h + 6, "DANS LA LIMITE DES STOCKS", ImageFont.truetype(BOLD, 44), "black", "white")


def surstock(img, brand):
    """Criativo 12: white 'On a produit trop de <brand> 😭', dark 'AIDEZ-NOUS À VIDER / NOTRE ENTREPÔT', red circle."""
    y = 150
    h = box(img, "center", y, f"On a produit trop de {brand}", ImageFont.truetype(BOLD, 44), "black", "white",
            emoji_ch="😭")
    f2 = ImageFont.truetype(BOLD, 46)
    y2 = y + h + 12
    for line in ("AIDEZ-NOUS À VIDER", "NOTRE ENTREPÔT"):
        y2 += box(img, "center", y2, line, f2, "white", (40, 40, 40, 200), pad=(16, 8)) + 4
    d = ImageDraw.Draw(img)
    cx, cy, r = 130, y2 + 150, 115
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED)
    f3 = ImageFont.truetype(BOLD, 38)
    lines = ["2 ACHETÉS", "=", "1 OFFERT"]
    lh = 44
    for i, line in enumerate(lines):
        d.text((cx - text_w(d, line, f3) / 2, cy - lh * 1.5 + i * lh), line, font=f3, fill="white")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", choices=["stock", "surstock"], required=True)
    ap.add_argument("--brand", default="Cinnarae")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    stock(img) if a.style == "stock" else surstock(img, a.brand)
    img.save(a.out)
    print(a.out)


if __name__ == "__main__":
    main()
