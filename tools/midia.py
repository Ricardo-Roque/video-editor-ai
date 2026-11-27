"""Arquivos dos criativos no Cloudflare R2: mídia e textos de cada criativo num bucket privado, com o índice
na tabela `arquivos` do Supabase. Quem não tem o arquivo no computador vê pelo painel (link assinado) ou baixa.

Configuração (passo a passo em R2.md), no .env:
  R2_ACCOUNT_ID         ID da conta Cloudflare
  R2_ACCESS_KEY_ID      chave do token da API do R2 (nunca exibir, nunca copiar)
  R2_SECRET_ACCESS_KEY  segredo do token (idem)
  R2_BUCKET             opcional (padrão: criativos)

Uso (a partir da raiz do projeto):
  python -I -X utf8 tools/midia.py verificar                  credenciais, bucket e quanto já está guardado
  python -I -X utf8 tools/midia.py subir C13 [CN05 ...]       envia o que é novo ou mudou (o resto é pulado)
  python -I -X utf8 tools/midia.py subir --todos [--ensaio]   todos os criativos com pasta local
  python -I -X utf8 tools/midia.py baixar C13 [--papel take]  traz para o computador o que só está no R2
  python -I -X utf8 tools/midia.py estado [C13]               o que está no R2, por criativo

O que sobe: tudo da pasta do criativo (textos, ficha.json, referencia/, imagens/, takes/, ilustracao/...) e os
vídeos finais (saídas dos montagem*.json e os de Vídeos Prontos com o código no nome). Os intermediários da
montagem (seg_NN.mp4, assembled.mp4, cards) não sobem: saem de novo dos takes. `painel.py entregar` sobe sozinho.
Um arquivo apagado no computador não é apagado do R2.

Para caber nos 10 GB grátis, takes e imagens vão compactados (o original fica no computador de quem gerou):
take em H.264 CRF 26 na mesma resolução (~26% do tamanho), imagem em WebP 90 (~17%). `baixar` devolve a imagem
no formato do nome (.png/.jpg). Vídeo final, referência e textos vão intactos. `verificar`, `estado` e `subir`
mostram o uso; a partir de 80% dos 10 GB sai um aviso.
"""
import argparse
import getpass
import hashlib
import json
import mimetypes
import pathlib
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from fnmatch import fnmatch

from dotenv import dotenv_values

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dados  # noqa: E402
from dados import ROOT  # noqa: E402

LIXO = ("desktop.ini", "Thumbs.db", ".DS_Store", "*.tmp", "*.tmp.*", "*.pyc", "~$*")
SHA_CACHE = ROOT / "painel" / ".r2_sha.json"      # fora do Git: evita recalcular o sha de vídeo que não mudou
GRATIS_GB = 10                                    # plano grátis do R2; o aviso sai a partir de 80%
VIDEO_EXT = {".mp4", ".mov", ".webm"}
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}


# ---------------------------------------------------------------- conexão com o R2

_CFG = {"t": 0.0, "v": None}


def config() -> dict | None:
    """Lê o .env no máximo a cada 30 s (o painel pergunta isso a cada vídeo e miniatura)."""
    import time
    if time.time() - _CFG["t"] > 30:
        env = dotenv_values(ROOT / ".env")
        c = {k: (env.get(k) or "").strip() for k in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY")}
        c["R2_BUCKET"] = (env.get("R2_BUCKET") or "criativos").strip()
        _CFG.update(t=time.time(), v=c if all(c[k] for k in c) else None)
    return _CFG["v"]


def configurado() -> bool:
    return config() is not None


_cli, _cli_lock = None, threading.Lock()


def cliente():
    global _cli
    with _cli_lock:
        if _cli is None:
            c = config()
            if not c:
                sys.exit("R2 não configurado no .env (ver R2.md).")
            import boto3
            from botocore.config import Config
            _cli = boto3.client(
                "s3", endpoint_url=f"https://{c['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
                aws_access_key_id=c["R2_ACCESS_KEY_ID"], aws_secret_access_key=c["R2_SECRET_ACCESS_KEY"],
                region_name="auto", config=Config(signature_version="s3v4", retries={"max_attempts": 5}))
        return _cli


def bucket() -> str:
    return config()["R2_BUCKET"]


def assinar(chave: str, segundos: int = 6 * 3600) -> str:
    """Link temporário para ler um objeto (o bucket é privado). Não chama a rede."""
    return cliente().generate_presigned_url("get_object", Params={"Bucket": bucket(), "Key": chave}, ExpiresIn=segundos)


_TEXTOS: dict = {}


def ler_texto(chave: str, sha: str | None = None) -> str:
    """Texto pequeno (documento, ficha.json, copy), guardado em memória pelo sha."""
    k = sha or chave
    if k not in _TEXTOS:
        corpo = cliente().get_object(Bucket=bucket(), Key=chave)["Body"].read()
        _TEXTOS[k] = corpo.decode("utf-8", errors="replace").replace("\r\n", "\n")   # igual ao read_text local
    return _TEXTOS[k]


# ---------------------------------------------------------------- o que sobe

def papel_de(caminho: str) -> str:
    topo = caminho.split("/", 1)[0] if "/" in caminho else ""
    if caminho.startswith("prontos/"):
        return "final"
    if topo in ("takes", "video"):          # video/: take da prova social
        return "take"
    if topo == "final":                     # final/: prova social com o selo
        return "final"
    if topo in ("imagens", "ilustracao"):
        return "imagem"
    if topo == "referencia":
        return "referencia"
    if not topo and pathlib.Path(caminho).suffix.lower() in (".md", ".json", ".txt"):
        return "documento"
    return "outro"


def coletar(cid: str, pasta: pathlib.Path | None) -> list[dict]:
    """Arquivos de um criativo: [{caminho, p (Path local), papel, cfg (montagem*.json que gerou o vídeo final)}]."""
    import painel
    out, vistos = [], set()

    def add(caminho, p, papel, cfg=None):
        if caminho not in vistos and p.is_file():
            vistos.add(caminho)
            out.append({"caminho": caminho, "p": p, "papel": papel, "cfg": cfg})

    if pasta:
        for p in sorted(pasta.rglob("*")):
            r = p.relative_to(pasta)
            intermediario = len(r.parts) > 1 and r.parts[0].startswith("montagem")   # montagem/, montagem_hook/
            if not p.is_file() or intermediario or any(fnmatch(p.name, x) for x in LIXO) or "__pycache__" in r.parts:
                continue
            add(r.as_posix(), p, papel_de(r.as_posix()))
        for cfg in sorted(pasta.glob("montagem*.json")):
            try:
                saida = json.loads(cfg.read_text(encoding="utf-8")).get("output")
            except (OSError, ValueError):
                saida = None
            if saida:
                p = painel.norm(cfg.parent / saida)
                if p.is_relative_to(painel.norm(pasta)):
                    add(p.relative_to(painel.norm(pasta)).as_posix(), p, "final", cfg)
                elif p.is_relative_to(painel.norm(painel.PRONTOS)):
                    add("prontos/" + p.name, p, "final", cfg)
    cfg = pasta / "montagem.json" if pasta and (pasta / "montagem.json").exists() else None
    for p in painel.prontos_por_codigo().get(cid, []):
        add("prontos/" + p.name, p, "final", cfg)
    # montagem/final.mp4 costuma ser cópia do que foi para Vídeos Prontos: só sobe se não houver outro final.
    finais = [it for it in out if it["papel"] == "final"]
    if len(finais) > 1:
        out = [it for it in out if it["caminho"] != "montagem/final.mp4"]
    elif not finais and pasta and (pasta / "montagem" / "final.mp4").exists():
        add("montagem/final.mp4", pasta / "montagem" / "final.mp4", "final", cfg)
    return out


def _sha(p: pathlib.Path, cache: dict) -> str:
    st = p.stat()
    k = f"{p}|{st.st_mtime_ns}|{st.st_size}"
    if k not in cache:
        h = hashlib.sha256()
        with p.open("rb") as f:
            for bloco in iter(lambda: f.read(1 << 20), b""):
                h.update(bloco)
        cache[k] = h.hexdigest()
    return cache[k]


def _mb(n) -> str:
    return f"{(n or 0) / 1048576:,.1f} MB"


def compactavel(it: dict) -> bool:
    """Takes e imagens vão compactados (o original fica no computador). Final e referência vão intactos."""
    ext = it["p"].suffix.lower()
    return (it["papel"] == "take" and ext in VIDEO_EXT) or (it["papel"] == "imagem" and ext in IMG_EXT)


def compactar(it: dict, pasta_tmp: pathlib.Path) -> tuple[pathlib.Path, str] | None:
    """Take: H.264 CRF 26 na mesma resolução. Imagem: WebP 90 (mantém transparência).
    Devolve (arquivo, tipo) ou None se não valer a pena (ganho menor que 15%) ou se falhar."""
    import subprocess
    p, ext = it["p"], it["p"].suffix.lower()
    out = pasta_tmp / (hashlib.sha1(str(p).encode()).hexdigest()[:16] + (".mp4" if ext in VIDEO_EXT else ".webp"))
    try:
        if ext in VIDEO_EXT:
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-map", "0:v:0", "-map", "0:a?",
                                "-c:v", "libx264", "-crf", "26", "-preset", "medium", "-pix_fmt", "yuv420p",
                                "-threads", "2", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out)],
                               capture_output=True)
            if r.returncode != 0:
                return None
            tipo = "video/mp4"
        else:
            from PIL import Image
            with Image.open(p) as im:
                im.save(out, "WEBP", quality=90, method=5)
            tipo = "image/webp"
    except Exception:  # noqa: BLE001 - na dúvida, sobe o original
        return None
    if not out.exists() or out.stat().st_size > 0.85 * p.stat().st_size:
        return None
    return out, tipo


def uso() -> dict:
    with dados.conectar() as conn:
        return dados.linhas(conn, """select count(*) n, coalesce(sum(bytes),0) b, count(distinct criativo_id) c,
                                            coalesce(sum(coalesce(bytes_original, bytes)),0) b_orig from arquivos""")[0]


def linha_uso(r: dict) -> str:
    pct = r["b"] / (GRATIS_GB * 1024 ** 3)
    economia = f" (originais somam {_mb(r['b_orig'])})" if r["b_orig"] > r["b"] else ""
    aviso = "  ATENÇÃO: passou de 80% do plano grátis." if pct >= 0.8 else ""
    return f"Guardado: {r['n']} arquivos de {r['c']} criativos, {_mb(r['b'])}{economia}; {pct:.0%} dos {GRATIS_GB} GB grátis.{aviso}"


def subir(cids: list[str], ensaio: bool = False, log=print) -> dict:
    """Envia ao R2 o que é novo ou mudou e atualiza o índice. Devolve {enviados, bytes, pulados, erros}."""
    import painel
    try:
        cache = json.loads(SHA_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        cache = {}
    locais = painel.pastas_todas()
    autor = getpass.getuser()
    tot = {"enviados": 0, "bytes": 0, "pulados": 0, "erros": 0}
    with dados.conectar() as conn:
        conn.autocommit = True
        ja = {(r["criativo_id"], r["caminho"]): r for r in dados.linhas(conn,
              """select criativo_id, caminho, chave, sha256, pasta, bytes_original from arquivos
                 where criativo_id = any(%s)""", (cids,))}
        for cid in cids:
            pasta = locais.get(cid)
            pasta_rel = painel.rel(pasta) if pasta else None
            itens = coletar(cid, pasta)
            if not itens:
                log(f"{cid}: nada para enviar (sem pasta local nem vídeo pronto).")
                continue
            novos, so_pasta = [], []
            for it in itens:
                it["sha"] = _sha(it["p"], cache)
                antigo = ja.get((cid, it["caminho"]))
                it["chave"] = antigo["chave"] if antigo else f"{cid}/{it['caminho']}"
                # Igual e já tratado: pula. Take/imagem enviado antes da compactação (bytes_original vazio) vai de novo.
                if antigo and antigo["sha256"] == it["sha"] and (antigo["bytes_original"] or not compactavel(it)):
                    tot["pulados"] += 1
                    if antigo["pasta"] != pasta_rel:
                        so_pasta.append(it)
                else:
                    novos.append(it)
            tamanho = sum(it["p"].stat().st_size for it in novos)
            log(f"{cid}: {len(novos)} para enviar ({_mb(tamanho)}), {len(itens) - len(novos)} já no R2."
                + ("  [ensaio]" if ensaio else ""))
            if ensaio:
                tot["enviados"] += len(novos); tot["bytes"] += tamanho
                continue

            def enviar(it):
                fonte, tipo = it["p"], mimetypes.guess_type(it["p"].name)[0] or "application/octet-stream"
                original = it["p"].stat().st_size
                # bytes_original preenchido = compactação já tentada (mesmo quando não valeu a pena)
                it["bytes_original"] = original if compactavel(it) else None
                c = compactar(it, tmp) if compactavel(it) else None
                if c:
                    fonte, tipo = c
                try:
                    cliente().upload_file(str(fonte), bucket(), it["chave"], ExtraArgs={"ContentType": tipo})
                    it["tipo"], it["bytes"] = tipo, fonte.stat().st_size
                finally:
                    if c:
                        fonte.unlink(missing_ok=True)
                return it

            linhas = []
            import tempfile
            with tempfile.TemporaryDirectory(prefix="r2_") as tmpdir, ThreadPoolExecutor(4) as ex:
                tmp = pathlib.Path(tmpdir)
                for it, fut in [(it, ex.submit(enviar, it)) for it in novos]:
                    try:
                        fut.result()
                    except Exception as e:  # noqa: BLE001 - um arquivo com erro não para os outros
                        tot["erros"] += 1
                        log(f"  erro em {it['caminho']}: {str(e)[:200]}")
                        continue
                    video = it["p"].suffix.lower() in painel.VIDEO_EXT
                    tl = painel.linha_do_tempo(it["cfg"]) if it["papel"] == "final" and it["cfg"] else []
                    linhas.append((cid, it["caminho"], it["papel"], it["chave"], pasta_rel, it["bytes"],
                                   it["bytes_original"], it["sha"], it["tipo"],
                                   round(painel.duracao(it["p"]), 2) if video else None,
                                   json.dumps(tl) if tl else None, autor))
                    tot["enviados"] += 1; tot["bytes"] += it["bytes"]
            if linhas:
                with conn.cursor() as cur:
                    cur.executemany("""
                        insert into arquivos (criativo_id, caminho, papel, chave, pasta, bytes, bytes_original, sha256,
                                              tipo_mime, duracao_s, linha_do_tempo, enviado_por)
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        on conflict (criativo_id, caminho) do update set papel = excluded.papel,
                          chave = excluded.chave, pasta = excluded.pasta, bytes = excluded.bytes,
                          bytes_original = excluded.bytes_original,
                          sha256 = excluded.sha256, tipo_mime = excluded.tipo_mime, duracao_s = excluded.duracao_s,
                          linha_do_tempo = excluded.linha_do_tempo, enviado_por = excluded.enviado_por,
                          enviado_em = now()""", linhas)
            if so_pasta:       # pasta mudou de lugar (ex.: entregue para Criativos Exemplo): só o índice muda
                conn.execute("update arquivos set pasta = %s where criativo_id = %s", (pasta_rel, cid))
    try:
        SHA_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    except OSError:
        pass
    return tot


def baixar(cid: str, papel: str | None = None, log=print) -> int:
    """Traz para o computador o que está no R2 e falta aqui (nunca sobrescreve arquivo local)."""
    import painel
    pasta = painel.pastas_todas().get(cid)
    with dados.conectar() as conn:
        rs = dados.linhas(conn, "select * from arquivos where criativo_id = %s" + (" and papel = %s" if papel else "")
                          + " order by caminho", (cid, papel) if papel else (cid,))
    n = 0
    for r in rs:
        if r["caminho"].startswith("prontos/"):
            destino = painel.PRONTOS / r["caminho"][len("prontos/"):]
        else:
            destino = (pasta or ROOT / (r["pasta"] or cid)) / r["caminho"]
        if destino.exists():
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        tmp = destino.with_name(destino.name + ".baixando")
        cliente().download_file(bucket(), r["chave"], str(tmp))
        if r["tipo_mime"] == "image/webp" and destino.suffix.lower() != ".webp":
            from PIL import Image                 # imagem guardada em WebP: volta ao formato do nome (.png/.jpg)
            with Image.open(tmp) as im:
                (im.convert("RGB") if destino.suffix.lower() in (".jpg", ".jpeg") else im).save(destino)
            tmp.unlink()
        else:
            tmp.replace(destino)
        n += 1
        log(f"  {painel.rel(destino)}  ({_mb(r['bytes'])})")
    log(f"{cid}: {n} arquivo(s) baixado(s).")
    return n


# ---------------------------------------------------------------- linha de comando

def cmd_verificar(a):
    c = config()
    if not c:
        sys.exit("Faltam R2_ACCOUNT_ID, R2_ACCESS_KEY_ID e R2_SECRET_ACCESS_KEY no .env (ver R2.md).")
    try:
        cliente().head_bucket(Bucket=c["R2_BUCKET"])
    except Exception as e:  # noqa: BLE001
        sys.exit(f"Não acessou o bucket '{c['R2_BUCKET']}': {str(e)[:200]}")
    teste = "_verificar/ok.txt"
    cliente().put_object(Bucket=c["R2_BUCKET"], Key=teste, Body=b"ok")
    cliente().delete_object(Bucket=c["R2_BUCKET"], Key=teste)
    print(f"R2 ok: bucket '{c['R2_BUCKET']}' lê e grava.")
    print(linha_uso(uso()))


def cmd_subir(a):
    import painel
    cids = (sorted(painel.pastas_locais(), key=painel.ordem) + sorted(painel.pastas_provas())) if a.todos \
        else [c.upper() for c in a.criativos]
    if not cids:
        sys.exit("Diga quais criativos (ex.: subir C13) ou use --todos.")
    if not a.ensaio and not configurado():
        sys.exit("R2 não configurado no .env (ver R2.md).")
    t = subir(cids, ensaio=a.ensaio)
    print(f"\n{'Seriam enviados' if a.ensaio else 'Enviados'}: {t['enviados']} arquivo(s), {_mb(t['bytes'])}"
          + (" (antes de compactar takes e imagens)" if a.ensaio else "") + f"; "
          f"{t['pulados']} já estavam no R2" + (f"; {t['erros']} com erro" if t["erros"] else "") + ".")
    if not a.ensaio:
        print(linha_uso(uso()))


def cmd_baixar(a):
    for c in a.criativos:
        baixar(c.upper(), a.papel)


def cmd_estado(a):
    with dados.conectar() as conn:
        rs = dados.linhas(conn, """select criativo_id, papel, count(*) n, sum(bytes) b, max(enviado_em) em
                                   from arquivos""" + (" where criativo_id = any(%s)" if a.criativos else "") +
                          " group by 1, 2 order by 1, 2", ([c.upper() for c in a.criativos],) if a.criativos else None)
    if not rs:
        print("Nada no R2 ainda.")
    for r in rs:
        print(f"{r['criativo_id']:<6} {r['papel']:<11} {r['n']:>4} arquivo(s) {_mb(r['b']):>12}  último envio {r['em']:%d/%m %H:%M}")
    print(linha_uso(uso()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("verificar").set_defaults(f=cmd_verificar)
    p = sub.add_parser("subir"); p.add_argument("criativos", nargs="*"); p.add_argument("--todos", action="store_true")
    p.add_argument("--ensaio", action="store_true", help="só mostra o que seria enviado"); p.set_defaults(f=cmd_subir)
    p = sub.add_parser("baixar"); p.add_argument("criativos", nargs="+")
    p.add_argument("--papel", choices=["final", "take", "imagem", "referencia", "documento", "outro"])
    p.set_defaults(f=cmd_baixar)
    p = sub.add_parser("estado"); p.add_argument("criativos", nargs="*"); p.set_defaults(f=cmd_estado)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
