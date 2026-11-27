"""Selo "ilustrativo · IA" no canto da prova social (foto ou vídeo) feita por IA.

Toda prova social gerada aqui leva o selo no arquivo final (pasta final/ da prova). É o que impede que uma
peça de loja de demonstração passe por avaliação de cliente real se for parar numa loja de verdade.

Uso (a partir da raiz do projeto):
  python -I -X utf8 tools/selo_ia.py "Provas Sociais/PS01/imagens/PS01_v1.png" "Provas Sociais/PS01/final/PS01.jpg" --idioma fr
  python -I -X utf8 tools/selo_ia.py "Provas Sociais/PS02/video/PS02_v1.mp4" "Provas Sociais/PS02/final/PS02.mp4" --idioma fr

O texto sai no idioma da peça (fr, en, es, de, it, pt; outro idioma usa o inglês). --texto troca o texto.
"""
import argparse
import pathlib
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTE = ROOT / "assets" / "fonts" / "Montserrat-ExtraBold.ttf"
TEXTOS = {"fr": "Illustration · IA", "en": "Illustrative · AI", "es": "Ilustrativo · IA", "de": "Illustration · KI",
          "it": "Illustrativo · IA", "pt": "Ilustrativo · IA"}
VIDEO = {".mp4", ".mov", ".webm"}


def selo_png(largura: int, texto: str) -> Image.Image:
    """Pílula semitransparente com o texto, proporcional à largura da peça (~3,2% de altura de letra)."""
    tam = max(12, round(largura * 0.032))
    fonte = ImageFont.truetype(str(FONTE), tam)
    caixa = fonte.getbbox(texto)
    pad_x, pad_y = round(tam * 0.7), round(tam * 0.45)
    w, h = caixa[2] - caixa[0] + 2 * pad_x, caixa[3] - caixa[1] + 2 * pad_y
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(0, 0, 0, 150))
    d.text((pad_x - caixa[0], pad_y - caixa[1]), texto, font=fonte, fill=(255, 255, 255, 235))
    return im


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--idioma", default="pt")
    ap.add_argument("--texto", default=None)
    a = ap.parse_args()
    ent, sai = pathlib.Path(a.entrada), pathlib.Path(a.saida)
    if not ent.is_file():
        sys.exit(f"Não achei {ent}")
    texto = a.texto or TEXTOS.get(a.idioma.lower()[:2], TEXTOS["en"])
    sai.parent.mkdir(parents=True, exist_ok=True)
    if ent.suffix.lower() in VIDEO:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width",
                              "-of", "csv=p=0", str(ent)], capture_output=True, text=True).stdout.strip()
        largura = int(out.split(",")[0] or 720)
        with tempfile.TemporaryDirectory() as tmp:
            png = pathlib.Path(tmp) / "selo.png"
            selo = selo_png(largura, texto)
            selo.save(png)
            margem = round(largura * 0.035)
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ent), "-i", str(png), "-filter_complex",
                                f"[0:v][1:v]overlay={margem}:main_h-overlay_h-{margem}", "-c:v", "libx264", "-crf", "20",
                                "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
                                str(sai)], capture_output=True, text=True)
            if r.returncode:
                sys.exit(r.stderr[-800:])
    else:
        with Image.open(ent) as im:
            base = im.convert("RGBA")
        selo = selo_png(base.width, texto)
        margem = round(base.width * 0.035)
        base.alpha_composite(selo, (margem, base.height - selo.height - margem))
        if sai.suffix.lower() in (".jpg", ".jpeg"):
            base.convert("RGB").save(sai, quality=92)
        else:
            base.save(sai)
    print(f"Selo \"{texto}\" aplicado: {sai}")


if __name__ == "__main__":
    main()
