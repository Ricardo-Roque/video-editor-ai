"""Build Criativo 39/ilustracao/Txx.json specs for T02-T21 from word timings, then render them."""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(r"c:/Users/ricar_6x5unl1/OneDrive/Documentos/Business/Projetos/Editor de Vídeo")
C = ROOT / "Criativo 39"
FOCUS = {"C03": (380, 420), "C04": (290, 640), "C05": (384, 640), "C06": (300, 900), "C07": (440, 800),
         "C08": (384, 700), "C09": (440, 680), "C10": (360, 560), "C11": (300, 560), "C12": (220, 540),
         "C13": (480, 760), "C14": (360, 520), "C15": (340, 440), "C16": (384, 700), "C17": (560, 440),
         "C18": (440, 720), "C19": (384, 700), "C20": (150, 1000), "C21": (400, 640), "C22": (360, 560),
         "C23": (384, 640), "C24": (280, 760), "C25": (384, 690), "C26": (384, 700), "C27": (280, 680),
         "C28": (340, 690), "C29": (320, 420), "C30": (340, 760), "C31": (220, 600), "C32": (380, 590),
         "C33": (384, 700), "C34": (280, 560), "C01": (205, 1170)}
FILE = {"T03": "T03_360p_corte_v1"}
VER = {"C05": 3, "C11": 2, "C12": 2, "C15": 2, "C17": 2, "C20": 2, "C24": 2, "C25": 2, "C32": 2, "C33": 2}
# take: [(image, switch word or None for start, overlays)]
PLAN = {
    "T02": [("C03", None), ("C04", "'est")],
    "T03": [("C05", None), ("C06", "agressée")],
    "T04": [("C07", None), ("C08", "comme")],
    "T05": [("C09", None), ("C10", "vous")],
    "T06": [("C11", None)],
    "T07": [("C12", None)],
    "T08": [("C13", None, [{"type": "label", "text": "70 %", "x": 384, "y": 300, "size": 130, "w": "70"}]),
            ("C14", "sentez")],
    "T09": [("C15", None), ("C16", "pousse")],
    "T10": [("C17", None)],
    "T11": [("C18", None), ("C19", "devient")],
    "T12": [("C20", None)],
    "T13": [("C21", None), ("C22", "bouche")],
    "T14": [("C23", None), ("C24", "infarctus")],
    "T15": [("C25", None), ("C26", "commence")],
    "T16": [("C27", None), ("C28", "dissoute")],
    "T17": [("C29", None)],
    "T18": [("C30", None), ("C31", "gardez")],
    "T19": [("C32", None, [{"type": "text", "text": "15", "x": 380, "y": 590, "size": 190, "color": [40, 40, 40],
                            "w": "15"}])],
    "T20": [("C33", None)],
    "T21": [("C34", None), ("C01", "avant")],
}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if c.isalnum() or c == "'").replace("’", "'")


def find(words, key, after=0.0):
    k = norm(key)
    for w in words:
        if w["s"] >= after - 0.01 and k in norm(w["w"]).replace("quinze", "15"):
            return w["s"]
    raise SystemExit(f"word not found: {key}")


def cam(img, a, b, idx):
    """Camera keys for one image shown from a to b: wide push for short shots; long shots alternate
    wide and close framings (hard reframe) about every 2.4 s, so the picture changes like a cut."""
    fx, fy = FOCUS[img]
    n = max(1, round((b - a) / 2.4))
    keys, step = [], (b - a) / n
    for i in range(n):
        t0, t1 = a + i * step, a + (i + 1) * step
        close = (i + idx) % 2 == 1
        if close:
            keys += [[t0, 1.6, fx, fy], [t1 - 0.001, 1.75, fx, fy]]
        else:
            keys += [[t0, 1.0, 384, 688], [t1 - 0.001, 1.18, (384 + fx) / 2, (688 + fy) / 2]]
    return keys


def main():
    takes = sys.argv[1:] or list(PLAN)
    for tk in takes:
        words = json.loads((C / f"takes/{FILE.get(tk, tk + '_360p_v1')}.words.json").read_text(encoding="utf-8"))
        end = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    str(C / f"takes/{FILE.get(tk, tk + '_360p_v1')}.mp4")], capture_output=True, text=True).stdout)
        plan = PLAN[tk]
        starts, prev = [], 0.0
        for item in plan:
            t = 0.0 if item[1] is None else find(words, item[1], prev) - 0.05
            starts.append(t)
            prev = t
        segs = []
        for i, item in enumerate(plan):
            img = item[0]
            a, b = starts[i], (starts[i + 1] if i + 1 < len(plan) else end)
            seg = {"start": a, "image": f"imagens/cenas/{img}_v{VER.get(img, 1)}.png", "keys": cam(img, a, b, i)}
            if img == "C13":  # stay wide so the "70 %" label at the top stays in frame
                seg["keys"] = [[a, 1.0, 384, 688], [b, 1.15, 400, 640]]
            if tk == "T21" and img == "C01":  # ending: from the blocked artery out to the whole grid
                seg["keys"] = [[a, 2.8, 205, 1170], [b, 1.0, 384, 688]]
            ovs = []
            for ov in (item[2] if len(item) > 2 else []):
                ov = dict(ov)
                ov["t"] = find(words, ov.pop("w"), a)
                ovs.append(ov)
            if ovs:
                seg["overlays"] = ovs
            segs.append(seg)
        spec = {"audio": f"takes/{FILE.get(tk, tk + '_360p_v1')}.mp4", "out": f"takes/{tk}_ilus_v1.mp4",
                "font": "../assets/fonts/Montserrat-ExtraBold.ttf", "segments": segs}
        p = C / f"ilustracao/{tk}.json"
        p.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        subprocess.run([sys.executable, "-I", "-X", "utf8", str(ROOT / "tools/ilustrar_take.py"), str(p)], check=True,
                       capture_output=True)
        src = C / f"takes/{FILE.get(tk, tk + '_360p_v1')}.words.json"
        (C / f"takes/{tk}_ilus_v1.words.json").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(tk, "ok", [s["image"].split("/")[-1] for s in segs], flush=True)


if __name__ == "__main__":
    main()
