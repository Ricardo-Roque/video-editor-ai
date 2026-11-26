"""Draw an Instagram-style question box ("caixinha de perguntas") as a full-frame transparent PNG (1080x1920).

Used by the Caixinha de perguntas format (Criativo 14). It is pasted over the video with a montagem.json
overlay {"mode": "patch", "x": 0, "y": 0}, limited to the hook with clip_index / from_word / to_word.

Usage:
  python -I -X utf8 tools/caixinha.py --header "Posez-moi vos questions" \
      --question "Je me lève 3 fois par nuit pour aller aux toilettes… c'est normal ? 😩" \
      --top 170 --out "Criativo 14/imagens/cenas/K1_caixinha_v1.png"

An emoji at the very end of the question is drawn in colour (Segoe UI Emoji); the rest of the text in Arial.
"""
import argparse
import pathlib

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
REG = "C:/Windows/Fonts/arial.ttf"
BOLD = "C:/Windows/Fonts/arialbd.ttf"
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
# Instagram-like gradient for the header band (purple -> pink -> orange).
GRAD = [(131, 58, 180), (225, 48, 108), (247, 119, 55)]


def text_w(draw, text, font):
    l, _, r, _ = draw.textbbox((0, 0), text, font=font)
    return r - l


def wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if text_w(draw, trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def gradient(w, h):
    g = Image.new("RGBA", (w, h))
    px = g.load()
    for x in range(w):
        t = x / max(1, w - 1)
        seg = 0 if t < 0.5 else 1
        lt = t * 2 if seg == 0 else (t - 0.5) * 2
        a, b = GRAD[seg], GRAD[seg + 1]
        col = tuple(int(a[i] + (b[i] - a[i]) * lt) for i in range(3)) + (255,)
        for y in range(h):
            px[x, y] = col
    return g


def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    tmp = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((0, 0), ch, font=f, embedded_color=True)
    return tmp.crop(tmp.getbbox()).resize((size, size), Image.LANCZOS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--header", default="Posez-moi vos questions")
    ap.add_argument("--question", required=True)
    ap.add_argument("--top", type=int, default=170, help="y of the top of the box")
    ap.add_argument("--width", type=int, default=860)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    question = args.question.strip()
    emo = None
    if question and ord(question[-1]) > 0x2600:  # trailing emoji
        emo = question[-1]
        question = question[:-1].rstrip()

    bw, pad, radius = args.width, 44, 42
    f_head = ImageFont.truetype(BOLD, 40)
    f_q = ImageFont.truetype(BOLD, 52)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    lines = wrap(probe, question, f_q, bw - 2 * pad - (70 if emo else 0))
    line_h = 66
    head_h = 96
    body_h = pad + line_h * len(lines) + pad - 10
    bh = head_h + body_h

    box = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw - 1, bh - 1), radius, fill=255)
    fill = Image.new("RGBA", (bw, bh), (255, 255, 255, 255))
    fill.alpha_composite(gradient(bw, head_h), (0, 0))
    box.paste(fill, (0, 0), mask)

    d = ImageDraw.Draw(box)
    hw = text_w(d, args.header, f_head)
    d.text(((bw - hw) / 2, (head_h - 46) / 2), args.header, font=f_head, fill=(255, 255, 255, 255))
    y = head_h + pad - 6
    for i, line in enumerate(lines):
        lw = text_w(d, line, f_q)
        extra = 70 if (emo and i == len(lines) - 1) else 0
        x = (bw - lw - extra) / 2
        d.text((x, y), line, font=f_q, fill=(20, 20, 20, 255))
        if extra:
            box.alpha_composite(emoji_img(emo, 56), (int(x + lw + 14), int(y + 2)))
        y += line_h

    # soft shadow
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((0, 0, bw - 1, bh - 1), radius, fill=(0, 0, 0, 70))
    x0 = (W - bw) // 2
    out.alpha_composite(shadow, (x0 + 6, args.top + 10))
    out.alpha_composite(box, (x0, args.top))

    path = pathlib.Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    out.save(path)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
