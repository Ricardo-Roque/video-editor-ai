"""Painel local dos criativos: biblioteca, player com anotação por tempo, métricas da Meta,
comparação, ranking por variável e fila de refação.

Uso (a partir da raiz do projeto):
  python -I -X utf8 tools/painel.py [--porta 8765]      abre o painel em http://127.0.0.1:8765
  python -I -X utf8 tools/painel.py fila                 pedidos de refação vindos do painel (para o Claude)
  python -I -X utf8 tools/painel.py feita <id> [<id>...] --resposta "o que foi feito, custo"
  python -I -X utf8 tools/painel.py esteira              cards com o Claude (fazer) e com o dono (aprovar)
  python -I -X utf8 tools/painel.py entregar C29 --etapa roteiro --custo 0.42 --nota "..."   etapa pronta para aprovar
  python -I -X utf8 tools/painel.py entrar C42 [--etapa fila]   põe um criativo novo na esteira
  python -I -X utf8 tools/painel.py usuario --email a@b.com --nome "Nome"   cria login (pede a senha)

Login: usuários e sessões no Supabase (senha em scrypt, cookie HttpOnly de 30 dias). No primeiro
acesso, sem nenhum usuário, a tela de login pede para criar o primeiro.
O painel escuta em 127.0.0.1 (--host 0.0.0.0 abre para a rede local) e só serve arquivos do projeto. Ele não gasta nada:
"refazer com anotações" só põe o pedido na fila; quem refaz é o Claude, com custo informado e aprovação,
como manda o PROCESSO.md. Com META_ACCESS_TOKEN no .env, sincroniza as métricas a cada META_SYNC_MIN
minutos (padrão 60) enquanto estiver aberto.
"""
import argparse
import json
import mimetypes
import os
import pathlib
import re
import subprocess
import sys
import threading
import time
import traceback
import webbrowser
from datetime import date, datetime
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, unquote, urlsplit

from dotenv import dotenv_values

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dados  # noqa: E402
from dados import ROOT  # noqa: E402

WEB = ROOT / "painel"
EXEMPLOS = ROOT / "Criativos Exemplo"
PRONTOS = ROOT / "Vídeos Prontos"
VIDEO_EXT = {".mp4", ".mov", ".webm"}
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}


# ---------------------------------------------------------------- banco

class Banco:
    """Uma conexão só, protegida por lock; reconecta se cair. Sem banco, o painel funciona só com o local."""

    def __init__(self):
        self.lock = threading.Lock()
        self.conn = None
        self.erro = None

    def _abrir(self):
        try:
            self.conn = dados.conectar()
            self.conn.autocommit = True
            self.erro = None
        except SystemExit as e:  # conectar() encerra com mensagem; aqui vira aviso no painel
            self.conn, self.erro = None, str(e)

    def ok(self) -> bool:
        with self.lock:
            if self.conn is None or self.conn.closed:
                self._abrir()
            return self.conn is not None

    def q(self, sql, params=None) -> list[dict]:
        with self.lock:
            for tentativa in range(2):
                if self.conn is None or self.conn.closed:
                    self._abrir()
                if self.conn is None:
                    return []
                try:
                    cur = self.conn.execute(sql, params)
                    if cur.description is None:     # update/insert/delete sem returning
                        return []
                    cols = [d.name for d in cur.description]
                    return [dict(zip(cols, r)) for r in cur.fetchall()]
                except dados.psycopg.OperationalError:
                    self.conn = None
                    if tentativa:
                        raise
        return []

    def lote(self, consultas: dict) -> dict:
        """Várias consultas numa ida só ao banco (cada ida ao Supabase custa ~200 ms).
        consultas = {nome: (sql, params)} -> {nome: [linhas]}. Datas voltam como texto ISO e números como float."""
        partes, params = [], []
        for nome, (sql, ps) in consultas.items():
            partes.append(f"'{nome}', (select coalesce(json_agg(t), '[]'::json) from ({sql}) t)")
            params.extend(ps or ())
        r = self.q("select json_build_object(" + ", ".join(partes) + ") r", params or None)
        return r[0]["r"] if r else {k: [] for k in consultas}


DB = Banco()


class Memo:
    """Guarda o resultado do banco até alguém gravar algo (todo POST limpa) ou até a validade vencer."""

    def __init__(self, validade: float):
        self.validade, self.t, self.v, self.lock = validade, 0.0, None, threading.Lock()

    def pegar(self, calcular):
        with self.lock:
            if self.v is None or time.time() - self.t > self.validade:
                self.v, self.t = calcular(), time.time()
            return self.v

    def limpar(self):
        self.v = None


MEMOS: list[Memo] = []


def memo(validade: float) -> Memo:
    m = Memo(validade)
    MEMOS.append(m)
    return m


def limpar_memos():
    for m in MEMOS:
        m.limpar()


# ---------------------------------------------------------------- arquivos locais

CACHE_DUR = WEB / ".cache_duracoes.json"   # fora do Git; ffprobe em pasta do OneDrive leva ~1 s por arquivo
_dur_lock = threading.Lock()
try:
    _dur_cache: dict = json.loads(CACHE_DUR.read_text(encoding="utf-8"))
except (OSError, ValueError):
    _dur_cache = {}


def duracao(p: pathlib.Path) -> float:
    st = p.stat()
    chave = f"{p}|{st.st_mtime_ns}|{st.st_size}"
    if chave not in _dur_cache:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                             capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()
        with _dur_lock:
            _dur_cache[chave] = float(out or 0)
            try:
                CACHE_DUR.write_text(json.dumps(_dur_cache), encoding="utf-8")
            except OSError:
                pass
    return _dur_cache[chave]


THUMBS = WEB / ".thumbs"                   # miniaturas geradas (fora do Git)
_thumb_sem = threading.Semaphore(4)


def miniatura(arquivo: str, t: float, largura: int) -> pathlib.Path | None:
    """Quadro do vídeo no tempo t (ou a imagem reduzida), em JPG, com cache em disco."""
    import hashlib
    p = (ROOT / arquivo).resolve()
    if not p.is_relative_to(ROOT_RES) or not p.is_file() or p.suffix.lower() not in VIDEO_EXT | IMG_EXT:
        return None
    st = p.stat()
    h = hashlib.sha1(f"{p}|{st.st_mtime_ns}|{t:.2f}|{largura}".encode()).hexdigest()[:20]
    out = THUMBS / f"{h}.jpg"
    if out.exists():
        return out
    THUMBS.mkdir(exist_ok=True)
    video = p.suffix.lower() in VIDEO_EXT
    with _thumb_sem:
        if out.exists():
            return out
        tmp = out.with_suffix(".tmp.jpg")
        cmd = ["ffmpeg", "-v", "error", "-y"] + (["-ss", f"{t:.2f}"] if video else []) + [
            "-i", str(p), "-frames:v", "1", "-vf", f"scale={largura}:-2", "-q:v", "4", str(tmp)]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode != 0 or not tmp.exists():
            if video and t > 0:                      # tempo além do fim: tenta o começo
                return miniatura(arquivo, 0.0, largura)
            return None
        tmp.replace(out)
    return out


def duracoes(ps: list[pathlib.Path]) -> list[float]:
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(8) as ex:
        return list(ex.map(duracao, ps))


ROOT_RES = ROOT.resolve()


def norm(p: pathlib.Path) -> pathlib.Path:
    """Tira os '..' sem ir ao disco (resolve() no Windows custa uma consulta ao sistema de arquivos por chamada)."""
    return pathlib.Path(os.path.normpath(p))


def rel(p: pathlib.Path) -> str:
    p = norm(p)
    try:
        return p.relative_to(ROOT_RES).as_posix()
    except ValueError:                       # caminho por atalho/symlink: aí sim resolve
        return p.resolve().relative_to(ROOT_RES).as_posix()


def url_midia(p: pathlib.Path) -> str:
    return "/media/" + quote(rel(p))


def pastas_locais() -> dict:
    """C<NN> -> pasta. A pasta na raiz (em produção) vence a de Criativos Exemplo."""
    res = {}
    bases = [d for d in EXEMPLOS.iterdir() if d.is_dir()] if EXEMPLOS.exists() else []
    for base in bases + [ROOT]:
        for d in base.iterdir():
            m = re.fullmatch(r"Criativo (\d{2,3})", d.name)
            if d.is_dir() and m:
                res[f"C{int(m.group(1)):02d}"] = d
    return res


def _script(base: pathlib.Path, cfg: dict) -> dict:
    try:
        from lote_takes import parse_rows
        return {t: text for t, _, text in parse_rows(base / cfg["script"])}
    except Exception:
        return {}


def linha_do_tempo(cfg_path: pathlib.Path) -> list[dict]:
    """Início e fim de cada take no vídeo final (soma das durações de montagem/seg_NN.mp4)."""
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    base = cfg_path.parent
    work = base / cfg.get("work_dir", "montagem")
    texto = _script(base, cfg)
    clips = cfg.get("clips", [])
    segs = [work / f"seg_{i:02d}.mp4" for i in range(len(clips))]
    if not segs or not all(s.exists() for s in segs):
        return []
    tl, t0 = [], 0.0
    for c, d in zip(clips, duracoes(segs)):
        tl.append({"take": c.get("take"), "arquivo": c.get("file"), "inicio": round(t0, 2), "fim": round(t0 + d, 2),
                   "texto": c.get("text") or texto.get(c.get("take"), "")})
        t0 += d
    return tl


_PRONTOS = memo(5)


def prontos_por_numero() -> dict:
    """Vídeos Prontos listados uma vez só (antes: dois glob por criativo a cada montagem da lista)."""
    def calcular():
        out: dict = {}
        if PRONTOS.exists():
            for p in sorted(PRONTOS.iterdir()):
                m = re.fullmatch(r"Criativo (\d{2,3})( .*)?\.mp4", p.name)
                if m:
                    out.setdefault(int(m.group(1)), []).append(p)
        return out
    return _PRONTOS.pegar(calcular)


def midias(cid: str, pasta: pathlib.Path | None, completo: bool = True) -> dict:
    """completo=False (lista): sem ffprobe, só os arquivos. completo=True (detalhe): duração e takes."""
    videos, vistos = [], set()

    def add(p: pathlib.Path, cfg: pathlib.Path | None):
        p = norm(p)
        if p.suffix.lower() in VIDEO_EXT and p not in vistos and p.is_relative_to(ROOT_RES) and p.exists():
            vistos.add(p)
            v = {"nome": p.name, "url": url_midia(p), "arquivo": rel(p)}
            if completo:
                v |= {"duracao": round(duracao(p), 2), "takes": linha_do_tempo(cfg) if cfg else []}
            videos.append(v)

    if pasta:
        for cfg in sorted(pasta.glob("montagem*.json")):
            try:
                out = json.loads(cfg.read_text(encoding="utf-8")).get("output")
            except (OSError, ValueError):
                out = None
            if out:
                add(cfg.parent / out, cfg)
    n = int(cid[1:])
    for p in prontos_por_numero().get(n, []):
            add(p, pasta / "montagem.json" if pasta and (pasta / "montagem.json").exists() else None)
    if pasta and not videos and (pasta / "montagem" / "final.mp4").exists():
        add(pasta / "montagem" / "final.mp4", pasta / "montagem.json")

    imagens, copy = [], None
    if pasta:
        for p in sorted((pasta / "imagens").glob("*")) if (pasta / "imagens").exists() else []:
            if p.suffix.lower() in IMG_EXT:
                imagens.append({"nome": p.name, "url": url_midia(p), "arquivo": rel(p)})
        cp = sorted(pasta.glob("copy_final*.txt"))
        if cp:
            copy = cp[0].read_text(encoding="utf-8", errors="replace")
    return {"videos": videos, "imagens": imagens, "copy": copy}


# ---------------------------------------------------------------- métricas

def num(v):
    if isinstance(v, Decimal):
        return float(v)
    return v


def derivar(t: dict | None) -> dict:
    t = {k: num(v) for k, v in (t or {}).items()}
    g = lambda k: t.get(k) or 0  # noqa: E731
    imp, plays = g("impressoes"), g("plays")
    div = lambda a, b: (a / b) if b else None  # noqa: E731
    return {
        "gasto": g("gasto"), "impressoes": imp, "compras": g("compras"), "receita": g("receita"),
        "checkouts": g("checkouts"), "cliques_link": g("cliques_link"), "moeda": t.get("moeda"),
        "anuncios": g("anuncios"),
        "cpa": div(g("gasto"), g("compras")), "roas": div(g("receita"), g("gasto")),
        "ctr": div(g("cliques_link"), imp), "cpm": div(g("gasto") * 1000, imp),
        "gancho": div(g("views_3s"), imp),                # hook rate: views de 3 s / impressões
        "thruplay": div(g("thruplays"), imp),
        "retencao50": div(g("p50"), plays),
        "curva": {k: div(g(k), plays) for k in ("p25", "p50", "p75", "p95", "p100")} | {"v3s": div(g("views_3s"), plays)}
                 if plays else None,
        "primeiro_dia": str(t["primeiro_dia"]) if t.get("primeiro_dia") else None,
        "ultimo_dia": str(t["ultimo_dia"]) if t.get("ultimo_dia") else None,
        "tem_dados": imp > 0,
        # somas brutas: o front recalcula a média só dos criativos do escopo (marca, produto, oferta)
        "brutos": {k: g(k) for k in ("gasto", "impressoes", "cliques_link", "views_3s", "plays", "thruplays",
                                     "p25", "p50", "p75", "p95", "p100", "checkouts", "compras", "receita")},
    }


_BANCO_LISTA = memo(60)


def banco_lista() -> dict:
    """Tudo que a lista precisa do banco, numa ida só e guardado até o próximo POST (ou 60 s)."""
    def calcular():
        r = DB.lote({
            "criativos": ("""select c.id, c.tipo, c.formato, c.status, c.processo, c.descricao, c.idioma, c.duracao_s,
                                    c.drive_nome, c.nome_anuncio, c.oferta_id, o.nome oferta_nome, o.pais, o.marca_id,
                                    m.nome marca_nome, o.produto_id, p.nome produto_nome
                             from criativos c join ofertas o on o.id = c.oferta_id
                             join marcas m on m.id = o.marca_id join produtos p on p.id = o.produto_id""", None),
            "totais": ("select * from v_criativo_totais", None),
            "notas": ("select criativo_id, round(avg(nota),1) nota, count(*) n from avaliacoes group by criativo_id", None),
            "anot": ("select criativo_id, status, count(*) n from anotacoes group by 1, 2", None),
            "vars": ("""select cv.criativo_id, cv.papel, v.id, v.categoria, v.variavel, v.valor, v.status
                        from criativo_variaveis cv join variaveis v on v.id = cv.variavel_id order by v.id""", None),
            "esteira": ("select * from esteira", None),
        })
        anot, vars_ = {}, {}
        for x in r["anot"]:
            anot.setdefault(x["criativo_id"], {})[x["status"]] = x["n"]
        for x in r["vars"]:
            vars_.setdefault(x["criativo_id"], []).append(x)
        return {"banco": {x["id"]: x for x in r["criativos"]}, "tot": {x["criativo_id"]: x for x in r["totais"]},
                "notas": {x["criativo_id"]: x for x in r["notas"]}, "anot": anot, "vars": vars_,
                "est": {x["criativo_id"]: x for x in r["esteira"]}}
    return _BANCO_LISTA.pegar(calcular)


def totais() -> dict:
    return banco_lista()["tot"]


def media_geral(tot: dict) -> dict:
    """Média ponderada de todos os criativos com dados (razão das somas)."""
    soma: dict = {}
    for t in tot.values():
        for k, v in t.items():
            if isinstance(v, (int, float, Decimal)) and k != "anuncios":
                soma[k] = soma.get(k, 0) + float(v)
    d = derivar(soma)
    n = sum(1 for t in tot.values() if (t.get("impressoes") or 0) > 0)
    d["criativos"] = n
    for k in ("gasto", "impressoes", "compras", "receita", "checkouts", "cliques_link"):  # contagens: média por criativo
        d[k] = d[k] / n if n else None
    return d


# ---------------------------------------------------------------- montagem das respostas

_LISTA = memo(5)          # pastas locais: reler a cada 5 s basta (o Claude cria arquivos enquanto trabalha)


def lista_criativos() -> list[dict]:
    return _LISTA.pegar(_montar_lista)


def invalidar_lista():
    """Depois de gravar algo: limpa a lista e tudo que veio do banco."""
    limpar_memos()
    _DETALHE.clear()


def reler_pastas():
    """Só os arquivos locais (barato); o que veio do banco continua guardado."""
    _LISTA.limpar()


def _montar_lista() -> list[dict]:
    locais = pastas_locais()
    bl = banco_lista()
    banco, tot, notas, anot, vars_, est = bl["banco"], bl["tot"], bl["notas"], bl["anot"], bl["vars"], bl["est"]
    ids = sorted(set(locais) | set(banco) | set(est), key=lambda x: int(x[1:]))
    out = []
    for cid in ids:
        b, pasta = banco.get(cid, {}), locais.get(cid)
        m = midias(cid, pasta, completo=False)
        tipo = b.get("tipo") or ("video" if m["videos"] or (pasta and (pasta / "montagem.json").exists())
                                 else "nativo" if m["copy"] else "video")
        formato = b.get("formato") or (pasta.parent.name if pasta and pasta.parent != ROOT else None)
        capa = (m["videos"][0]["url"] if m["videos"] else None)
        capa_img = m["imagens"][-1]["url"] if (not capa and m["imagens"]) else None
        capa_arq = m["videos"][0]["arquivo"] if capa else (m["imagens"][-1]["arquivo"] if capa_img else None)
        out.append({
            "id": cid, "tipo": tipo, "formato": formato,
            "status": b.get("status") or ("em_producao" if pasta and pasta.parent == ROOT else "entregue"),
            "no_banco": bool(b), "processo": b.get("processo"), "descricao": b.get("descricao"),
            "idioma": b.get("idioma"),
            "oferta_id": b.get("oferta_id"), "oferta_nome": b.get("oferta_nome"), "pais": b.get("pais"),
            "marca_id": b.get("marca_id"), "marca_nome": b.get("marca_nome"),
            "produto_id": b.get("produto_id"), "produto_nome": b.get("produto_nome"),
            "drive_nome": b.get("drive_nome"), "pasta": rel(pasta) if pasta else None,
            "capa_video": capa, "capa_imagem": capa_img, "capa_arquivo": capa_arq, "n_videos": len(m["videos"]),
            "metricas": derivar(tot.get(cid)), "nota": num((notas.get(cid) or {}).get("nota")),
            "anotacoes": anot.get(cid, {}), "variaveis": vars_.get(cid, []),
        })
        c = out[-1]
        if cid in est:                       # a linha da esteira manda: está em produção
            e = est[cid]
            c["status"] = "em_producao"
            c["esteira"] = {"etapa": e["etapa"], "aguardando": e["aguardando"], "desde": e["desde"],
                            "custo_usd": num(e["custo_usd"]), "inferida": False}
        elif c["status"] == "em_producao":   # ainda sem linha: etapa deduzida dos arquivos da pasta
            etapa = etapa_pelos_arquivos(pasta, tipo, bool(m["videos"]))
            c["esteira"] = {"etapa": etapa, "aguardando": "claude" if etapa == "fila" else "dono",
                            "desde": None, "custo_usd": None, "inferida": True}
    return out


# ---------------------------------------------------------------- esteira de produção

ETAPAS = ["fila", "analise", "roteiro", "imagens", "takes", "montagem", "revisao"]
ETAPAS_NATIVO = ["fila", "analise", "roteiro", "imagens", "revisao"]       # sem takes nem montagem
DOCS = ["conceito.md", "quebra.md", "analise.md", "roteiro_*.md", "comparativo_roteiro.md", "prompts_imagens.md",
        "copy_final*.txt", "notas*.md"]


def etapas_de(tipo: str | None) -> list[str]:
    return ETAPAS if tipo == "video" else ETAPAS_NATIVO


def etapa_pelos_arquivos(pasta: pathlib.Path | None, tipo: str | None, tem_video: bool = False) -> str:
    """Etapa de um criativo que ainda não tem linha na esteira, pelo que já existe na pasta."""
    if not pasta:
        return "fila"
    tem = lambda d, ext: (pasta / d).exists() and any(p.suffix.lower() in ext for p in (pasta / d).rglob("*"))  # noqa: E731
    if tem_video or (pasta / "montagem" / "final.mp4").exists() or (tipo != "video" and (list(pasta.glob("copy_final*.txt")))
                                                        and tem("imagens", IMG_EXT)):
        return "revisao"
    if tem("takes", VIDEO_EXT):
        return "takes"
    if tem("imagens", IMG_EXT):
        return "imagens"
    if list(pasta.glob("roteiro_*.md")):
        return "roteiro"
    if any((pasta / n).exists() for n in ("analise.md", "quebra.md", "conceito.md")):
        return "analise"
    return "fila"


def tipo_de(cid: str) -> str | None:
    c = next((x for x in lista_criativos() if x["id"] == cid), None)
    return c["tipo"] if c else None


def esteira_estado(cid: str) -> dict | None:
    r = DB.q("select * from esteira where criativo_id = %s", (cid,))
    if r:
        return r[0]
    c = next((x for x in lista_criativos() if x["id"] == cid), None)
    if c and c.get("esteira"):                    # deduzida: grava a linha na primeira ação
        e = c["esteira"]
        return DB.q("""insert into esteira (criativo_id, etapa, aguardando) values (%s,%s,%s)
                       on conflict (criativo_id) do update set etapa = esteira.etapa returning *""",
                    (cid, e["etapa"], e["aguardando"]))[0]
    return None


def esteira_evento(cid, etapa, acao, autor, comentario=None, custo=None):
    DB.q("""insert into esteira_eventos (criativo_id, etapa, acao, autor, comentario, custo_usd)
            values (%s,%s,%s,%s,%s,%s)""", (cid, etapa, acao, autor, comentario, custo))


def esteira_acao(b: dict, autor: str) -> dict:
    """Ações do painel: aprovar a etapa, pedir ajuste, mover de etapa ou descartar."""
    cid, acao = b.get("criativo_id", ""), b.get("acao")
    comentario = (b.get("comentario") or "").strip() or None
    if not re.fullmatch(r"C\d{2,3}", cid):
        raise ValueError("Criativo inválido.")
    e = esteira_estado(cid)
    if not e:
        raise ValueError("Este criativo não está na esteira de produção.")
    etapas = etapas_de(tipo_de(cid))
    etapa = e["etapa"]
    if acao == "aprovar":
        if etapa == "revisao":                    # última porta: sai da esteira e vai para a biblioteca
            if not DB.q("select 1 from criativos where id = %s", (cid,)):
                raise ValueError("Defina a oferta do criativo (botão no card Oferta) antes de aprovar a entrega.")
            DB.q("update criativos set status = 'entregue', entregue_em = now() where id = %s", (cid,))
            DB.q("delete from esteira where criativo_id = %s", (cid,))
            esteira_evento(cid, etapa, "concluiu", autor, comentario)
            return {"ok": True, "entregue": True}
        prox = etapas[min(etapas.index(etapa) + 1, len(etapas) - 1)] if etapa in etapas else etapas[1]
        DB.q("""update esteira set etapa = %s, aguardando = 'claude', desde = now(), atualizado_por = %s,
                atualizado_em = now() where criativo_id = %s""", (prox, autor, cid))
        esteira_evento(cid, etapa, "aprovou", autor, comentario)
        return {"ok": True, "etapa": prox}
    if acao == "ajuste":
        if not comentario:
            raise ValueError("Escreva o que ajustar.")
        # O pedido vira anotação na fila (junto com as anotações abertas do criativo): o Claude refaz a etapa.
        DB.q("""insert into anotacoes (criativo_id, arquivo, tempo_s, take, texto, autor, status, pedida_em)
                values (%s, null, null, null, %s, %s, 'pedida', now())""", (cid, f"[{etapa}] {comentario}", autor))
        DB.q("update anotacoes set status = 'pedida', pedida_em = now() where criativo_id = %s and status = 'aberta'", (cid,))
        DB.q("""update esteira set aguardando = 'claude', atualizado_por = %s, atualizado_em = now()
                where criativo_id = %s""", (autor, cid))
        esteira_evento(cid, etapa, "pediu_ajuste", autor, comentario)
        return {"ok": True}
    if acao == "mover":
        nova, ag = b.get("etapa"), b.get("aguardando") or "claude"
        if nova not in etapas or ag not in ("claude", "dono"):
            raise ValueError("Etapa inválida para este tipo de criativo.")
        DB.q("""update esteira set etapa = %s, aguardando = %s, desde = case when etapa = %s then desde else now() end,
                atualizado_por = %s, atualizado_em = now() where criativo_id = %s""", (nova, ag, nova, autor, cid))
        esteira_evento(cid, nova, "moveu", autor, comentario or f"de {etapa} para {nova}")
        return {"ok": True}
    if acao == "descartar":
        DB.q("update criativos set status = 'descartado' where id = %s", (cid,))
        DB.q("delete from esteira where criativo_id = %s", (cid,))
        esteira_evento(cid, etapa, "descartou", autor, comentario)
        return {"ok": True}
    raise ValueError("Ação desconhecida.")


def ficha_e_documentos(pasta: pathlib.Path | None) -> dict:
    """ficha.json (roteiro dissecado e anúncio, escrita pelo Claude) + os textos da pasta + os takes."""
    out = {"ficha": None, "ficha_erro": None, "documentos": [], "takes_arquivos": []}
    if not pasta:
        return out
    f = pasta / "ficha.json"
    if f.exists():
        try:
            out["ficha"] = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            out["ficha_erro"] = f"ficha.json inválida: {e}"
    vistos = set()
    for padrao in DOCS:
        for p in sorted(pasta.glob(padrao)):
            if p not in vistos and p.is_file():
                vistos.add(p)
                out["documentos"].append({"nome": p.name, "texto": p.read_text(encoding="utf-8", errors="replace")})
    if (pasta / "takes").exists():
        for p in sorted((pasta / "takes").glob("*")):
            if p.suffix.lower() in VIDEO_EXT:
                m = re.match(r"(T\d+[a-z]?)", p.name)
                out["takes_arquivos"].append({"nome": p.name, "take": m.group(1) if m else p.stem,
                                              "url": url_midia(p), "arquivo": rel(p)})
    return out


def detalhe(cid: str) -> dict:
    locais = pastas_locais()
    pasta = locais.get(cid)
    base = next((dict(c) for c in lista_criativos() if c["id"] == cid), None)   # cópia: não mexe no cache
    if not base:
        return {}
    m = midias(cid, pasta)
    tot = totais()
    base.update(m)
    base["media"] = media_geral(tot)
    base.update(detalhe_banco(cid))
    base.update(ficha_e_documentos(pasta))
    base["etapas"] = etapas_de(base.get("tipo"))
    return base


_DETALHE: dict = {}       # cid -> (hora, dados do banco); limpo a cada POST (invalidar_lista)


def detalhe_banco(cid: str) -> dict:
    """As 6 consultas do detalhe numa ida só ao banco, guardadas por 60 s ou até o próximo POST."""
    hit = _DETALHE.get(cid)
    if hit and time.time() - hit[0] < 60:
        return hit[1]
    r = DB.lote({
        "anotacoes_lista": ("select * from anotacoes where criativo_id = %s order by coalesce(tempo_s, -1), id", (cid,)),
        "avaliacoes": ("select autor, nota, comentario, atualizado_em from avaliacoes where criativo_id = %s", (cid,)),
        "anuncios": ("""select a.ad_id, a.nome, a.status, a.campanha_nome, a.conjunto_nome,
                               coalesce(sum(m.gasto),0) gasto, coalesce(sum(m.compras),0) compras
                        from anuncios_meta a left join metricas_meta m on m.ad_id = a.ad_id
                        where a.criativo_id = %s group by a.ad_id order by gasto desc""", (cid,)),
        "diario": ("""select m.dia, sum(m.gasto) gasto, sum(m.compras) compras, sum(m.impressoes) impressoes
                      from metricas_meta m join anuncios_meta a on a.ad_id = m.ad_id
                      where a.criativo_id = %s group by m.dia order by m.dia""", (cid,)),
        "manuais": ("select * from resultados where criativo_id = %s order by periodo_inicio", (cid,)),
        "eventos": ("select * from esteira_eventos where criativo_id = %s order by em desc limit 60", (cid,)),
    })
    _DETALHE[cid] = (time.time(), r)
    return r


def take_no_tempo(cid: str, arquivo: str | None, tempo: float | None) -> str | None:
    if tempo is None or not arquivo:
        return None
    for v in midias(cid, pastas_locais().get(cid))["videos"]:
        if v["arquivo"] == arquivo:
            for t in v["takes"]:
                if t["inicio"] <= tempo < t["fim"]:
                    return t["take"]
    return None


_VARS = memo(60)


def variaveis_ranking() -> list[dict]:
    return _VARS.pegar(_variaveis_ranking)


def _variaveis_ranking() -> list[dict]:
    out = []
    ids = {}
    r_ = DB.lote({"cv": ("select variavel_id, criativo_id, papel from criativo_variaveis order by criativo_id", None),
                  "vd": ("select * from v_variavel_desempenho order by categoria, variavel_id", None)})
    for r in r_["cv"]:
        ids.setdefault(r["variavel_id"], []).append({"id": r["criativo_id"], "papel": r["papel"]})
    for r in r_["vd"]:
        d = derivar(r)
        out.append({k: num(r[k]) for k in ("variavel_id", "marca_id", "categoria", "variavel", "valor", "status",
                                           "criativos", "criativos_com_dados")}
                   | {"metricas": d, "criativos_ids": ids.get(r["variavel_id"], [])})
    return out


# ---------------------------------------------------------------- sincronização automática

ESTADO = {"ultima_sync": None, "sync_erro": None, "sync_rodando": False}


def meta_configurada() -> bool:
    env = dotenv_values(ROOT / ".env")
    return bool(env.get("META_ACCESS_TOKEN") and env.get("META_AD_ACCOUNT_ID"))


def sincronizar_agora(dias=30) -> dict:
    import meta
    if ESTADO["sync_rodando"]:
        return {"ok": False, "erro": "Sincronização já em andamento."}
    ESTADO["sync_rodando"] = True
    try:
        res = meta.sincronizar(dias, log=lambda s: print("[meta]", s))
        ESTADO.update(ultima_sync=datetime.now().isoformat(timespec="seconds"), sync_erro=None)
        invalidar_lista()                           # números novos: limpa o que estava guardado
        return {"ok": True, **res}
    except Exception as e:  # noqa: BLE001
        ESTADO["sync_erro"] = str(e)
        return {"ok": False, "erro": str(e)}
    finally:
        ESTADO["sync_rodando"] = False


def laco_sync():
    minutos = int(dotenv_values(ROOT / ".env").get("META_SYNC_MIN") or 60)
    while True:
        if meta_configurada() and DB.ok():
            sincronizar_agora()
        time.sleep(max(5, minutos) * 60)


# ---------------------------------------------------------------- marca > produto > oferta

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{1,40}$")


_CATALOGO = memo(300)


def catalogo() -> dict:
    return _CATALOGO.pegar(lambda: DB.lote({
        "marcas": ("select id, nome, prefixo from marcas order by nome", None),
        "produtos": ("select id, marca_id, nome, descricao from produtos order by nome", None),
        "ofertas": ("""select o.id, o.marca_id, o.produto_id, o.nome, o.status, o.pais, o.idioma, o.moeda,
                              o.oferta_atual, count(c.id) criativos
                       from ofertas o left join criativos c on c.oferta_id = o.id
                       group by o.id order by o.status, o.id""", None),
    }))


def salvar_catalogo(tipo: str, b: dict) -> dict:
    """Cria ou edita marca, produto ou oferta com os campos mínimos. O resto da oferta (promessa,
    avatar, funil) continua pelo portão de contexto do dados.py."""
    if tipo == "marca":
        if not SLUG.match(b.get("id", "")) or not b.get("nome") or not re.fullmatch(r"[A-Z]{2,5}", b.get("prefixo", "")):
            raise ValueError("Marca: id em minúsculas (ex.: cinnarae), nome e prefixo de 2 a 5 letras maiúsculas (ex.: CIN).")
        DB.q("""insert into marcas (id, nome, prefixo) values (%s,%s,%s)
                on conflict (id) do update set nome = excluded.nome""", (b["id"], b["nome"].strip(), b["prefixo"]))
    elif tipo == "produto":
        if not SLUG.match(b.get("id", "")) or not b.get("nome") or not b.get("marca_id"):
            raise ValueError("Produto: id em minúsculas (ex.: cayenne-softgels), marca e nome.")
        DB.q("""insert into produtos (id, marca_id, nome, descricao) values (%s,%s,%s,%s)
                on conflict (id) do update set nome = excluded.nome, descricao = excluded.descricao""",
             (b["id"], b["marca_id"], b["nome"].strip(), b.get("descricao")))
    elif tipo == "oferta":
        if not re.fullmatch(r"[A-Z]{2,5}-[A-Z]{2}-\d{2}", b.get("id", "")):
            raise ValueError("Oferta: id no formato PREFIXO-PAÍS-NN (ex.: CIN-FR-02).")
        if not all(b.get(k) for k in ("marca_id", "produto_id", "nome", "pais", "idioma")):
            raise ValueError("Oferta: marca, produto, nome, país e idioma são obrigatórios.")
        if b.get("status", "ativa") not in ("ativa", "pausada", "encerrada"):
            raise ValueError("Status inválido.")
        DB.q("""insert into ofertas (id, marca_id, produto_id, nome, status, pais, idioma, moeda, oferta_atual)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                on conflict (id) do update set nome = excluded.nome, status = excluded.status,
                  oferta_atual = coalesce(excluded.oferta_atual, ofertas.oferta_atual), moeda = excluded.moeda""",
             (b["id"], b["marca_id"], b["produto_id"], b["nome"].strip(), b.get("status") or "ativa",
              b["pais"].upper(), b["idioma"].lower(), (b.get("moeda") or "EUR").upper(), b.get("oferta_atual") or None))
    else:
        raise ValueError("tipo desconhecido")
    return {"ok": True}


def registrar_criativo(b: dict) -> dict:
    """Põe um criativo local na tabela criativos (ou troca a oferta de um que já está lá)."""
    cid = b.get("id", "")
    if not re.fullmatch(r"C\d{2,3}", cid) or not b.get("oferta_id"):
        raise ValueError("Criativo e oferta são obrigatórios.")
    if DB.q("select 1 from criativos where id = %s", (cid,)):
        DB.q("update criativos set oferta_id = %s where id = %s", (b["oferta_id"], cid))
        return {"ok": True, "acao": "oferta trocada"}
    if b.get("processo") not in ("replica", "modelagem") or b.get("tipo") not in ("video", "nativo", "imagem") \
            or not b.get("formato") or not b.get("idioma"):
        raise ValueError("Para registrar: processo, tipo, formato e idioma.")
    status = b.get("status") or "em_producao"
    if status not in ("em_producao", "entregue", "no_ar", "pausado", "descartado"):
        raise ValueError("Status inválido.")
    DB.q("""insert into criativos (id, oferta_id, processo, tipo, formato, idioma, status, descricao)
            values (%s,%s,%s,%s,%s,%s,%s,%s)""",
         (cid, b["oferta_id"], b["processo"], b["tipo"], b["formato"].strip(), b["idioma"].lower(), status,
          b.get("descricao") or None))
    return {"ok": True, "acao": "registrado"}


# ---------------------------------------------------------------- login

import hashlib  # noqa: E402
import hmac  # noqa: E402
import secrets  # noqa: E402

COOKIE = "painel_sessao"
SESSAO_DIAS = 30
_sessoes_cache: dict = {}            # sha256(token) -> (usuario, validade do cache)
_falhas: dict = {}                   # ip -> [horários de senha errada]


def hash_senha(senha: str) -> str:
    sal = secrets.token_bytes(16)
    h = hashlib.scrypt(senha.encode("utf-8"), salt=sal, n=2 ** 14, r=8, p=1, dklen=32)
    return f"scrypt$16384$8$1${sal.hex()}${h.hex()}"


def confere_senha(senha: str, guardado: str) -> bool:
    try:
        _, n, r, p, sal, h = guardado.split("$")
        calc = hashlib.scrypt(senha.encode("utf-8"), salt=bytes.fromhex(sal), n=int(n), r=int(r), p=int(p), dklen=32)
        return hmac.compare_digest(calc.hex(), h)
    except (ValueError, TypeError):
        return False


def validar_senha(senha: str) -> None:
    if len(senha or "") < 10:
        raise ValueError("A senha precisa de pelo menos 10 caracteres.")


def criar_usuario(email: str, nome: str, senha: str) -> dict:
    email = (email or "").strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) or not (nome or "").strip():
        raise ValueError("E-mail e nome são obrigatórios.")
    validar_senha(senha)
    if DB.q("select 1 from usuarios where email = %s", (email,)):
        raise ValueError("Já existe um usuário com esse e-mail.")
    return DB.q("insert into usuarios (email, nome, senha_hash) values (%s,%s,%s) returning id, email, nome",
                (email, nome.strip(), hash_senha(senha)))[0]


def n_usuarios() -> int:
    r = DB.q("select count(*) n from usuarios")
    return r[0]["n"] if r else 0


def abrir_sessao(usuario_id: int, ip: str) -> str:
    token = secrets.token_urlsafe(32)
    DB.q("insert into sessoes (token_hash, usuario_id, expira_em, ip) values (%s,%s, now() + %s * interval '1 day', %s)",
         (hashlib.sha256(token.encode()).hexdigest(), usuario_id, SESSAO_DIAS, ip))
    DB.q("update usuarios set ultimo_login = now() where id = %s", (usuario_id,))
    DB.q("delete from sessoes where expira_em < now()")
    return token


def usuario_da_sessao(token: str | None) -> dict | None:
    if not token:
        return None
    th = hashlib.sha256(token.encode()).hexdigest()
    hit = _sessoes_cache.get(th)
    if hit and hit[1] > time.time():
        return hit[0]
    r = DB.q("""select u.id, u.email, u.nome from sessoes s join usuarios u on u.id = s.usuario_id
                where s.token_hash = %s and s.expira_em > now() and u.ativo""", (th,))
    u = r[0] if r else None
    if u:
        _sessoes_cache[th] = (u, time.time() + 300)  # evita uma ida ao banco por requisição (5 min)
    return u


def fechar_sessao(token: str | None):
    if token:
        th = hashlib.sha256(token.encode()).hexdigest()
        _sessoes_cache.pop(th, None)
        DB.q("delete from sessoes where token_hash = %s", (th,))


def bloqueado(ip: str) -> bool:
    agora = time.time()
    _falhas[ip] = [t for t in _falhas.get(ip, []) if agora - t < 900]
    return len(_falhas[ip]) >= 8                     # 8 erros em 15 min


# ---------------------------------------------------------------- HTTP

def para_json(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if isinstance(o, Decimal):
        return float(o)
    return str(o)


class Handler(BaseHTTPRequestHandler):
    server_version = "Painel/1"

    def log_message(self, fmt, *args):
        if "/api/" in str(args[0] if args else ""):
            sys.stderr.write("%s\n" % (fmt % args))

    def _json(self, obj, code=200):
        body = json.dumps(obj, default=para_json, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _corpo(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}") if n else {}

    def _arquivo(self, p: pathlib.Path, raiz: pathlib.Path = ROOT):
        try:
            p = p.resolve(strict=True)
        except OSError:
            return self.send_error(404)
        if not p.is_relative_to(raiz.resolve()) or not p.is_file() or ".env" in p.name:
            return self.send_error(403)
        tamanho = p.stat().st_size
        tipo = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        inicio, fim = 0, tamanho - 1
        rng = self.headers.get("Range")
        if rng and (m := re.match(r"bytes=(\d*)-(\d*)", rng)):
            if m.group(1):
                inicio = int(m.group(1))
                fim = int(m.group(2)) if m.group(2) else fim
            else:
                inicio = max(0, tamanho - int(m.group(2)))
            fim = min(fim, tamanho - 1)
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {inicio}-{fim}/{tamanho}")
        else:
            self.send_response(200)
        self.send_header("Content-Type", tipo + ("; charset=utf-8" if tipo.startswith("text/") else ""))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(fim - inicio + 1))
        if getattr(self, "_cache_longo", False):     # miniatura: pode mudar se o vídeo for refeito
            self.send_header("Cache-Control", "max-age=600")
        self.end_headers()
        if self.command == "HEAD":
            return
        with p.open("rb") as f:
            f.seek(inicio)
            falta = fim - inicio + 1
            try:
                while falta > 0:
                    bloco = f.read(min(1 << 20, falta))
                    if not bloco:
                        break
                    self.wfile.write(bloco)
                    falta -= len(bloco)
            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                pass

    def do_HEAD(self):
        self.do_GET()

    # --- sessão
    def _token(self) -> str | None:
        from http.cookies import SimpleCookie
        c = SimpleCookie(self.headers.get("Cookie") or "")
        return c[COOKIE].value if COOKIE in c else None

    def _ip(self) -> str:
        return self.client_address[0]

    def _cookie_sessao(self, token: str, apagar=False):
        idade = 0 if apagar else SESSAO_DIAS * 86400
        self.send_header("Set-Cookie", f"{COOKIE}={'' if apagar else token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={idade}")

    def _redirecionar(self, para: str):
        self.send_response(302)
        self.send_header("Location", para)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        u = urlsplit(self.path)
        qs = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            # rotas abertas: tela de login e o que ela precisa
            if u.path == "/login":
                return self._arquivo(WEB / "login.html")
            if u.path in ("/static/style.css", "/static/login.js"):
                return self._arquivo(WEB / u.path[len("/static/"):])
            if u.path == "/api/primeiro_acesso":
                return self._json({"sem_usuarios": DB.ok() and n_usuarios() == 0, "banco": DB.ok()})
            self.usuario = usuario_da_sessao(self._token())
            if not self.usuario:
                if u.path.startswith("/api/"):
                    return self._json({"erro": "sessão expirada", "login": True}, 401)
                if u.path in ("/", "/index.html"):
                    return self._redirecionar("/login")
                return self.send_error(401)
            if u.path in ("/", "/index.html"):
                return self._arquivo(WEB / "index.html")
            if u.path.startswith("/static/"):
                return self._arquivo(WEB / unquote(u.path[len("/static/"):]))
            if u.path == "/api/eu":
                return self._json(self.usuario)
            if u.path == "/api/catalogo":
                return self._json(catalogo())
            if u.path == "/api/usuarios":
                return self._json({"usuarios": DB.q("select id, email, nome, ativo, criado_em, ultimo_login from usuarios order by id")})
            if u.path.startswith("/media/"):
                return self._arquivo(ROOT / unquote(u.path[len("/media/"):]))
            if u.path == "/thumb":
                larg = max(80, min(720, int(qs.get("w") or 320)))
                p = miniatura(qs.get("arquivo", ""), float(qs.get("t") or 0), larg)
                if not p:
                    return self.send_error(404)
                self._cache_longo = True
                return self._arquivo(p, raiz=WEB)
            if u.path == "/api/estado":
                return self._json({"banco": DB.ok(), "banco_erro": DB.erro, "meta": meta_configurada(), **ESTADO})
            if u.path == "/api/criativos":
                reler_pastas()                    # arquivos novos aparecem; o banco vem do cache até o próximo POST
                tot = totais()
                return self._json({"criativos": lista_criativos(), "media": media_geral(tot)})
            if m := re.fullmatch(r"/api/criativos/(C\d{2,3})", u.path):
                d = detalhe(m.group(1))
                return self._json(d) if d else self._json({"erro": "não encontrado"}, 404)
            if u.path == "/api/fila":
                return self._json({"anotacoes": DB.q("""
                    (select * from anotacoes where status in ('pedida','aberta'))
                    union all
                    (select * from anotacoes where status = 'feita' order by feita_em desc limit 30)
                    order by criativo_id, tempo_s nulls first""")})
            if u.path == "/api/variaveis":
                return self._json({"variaveis": variaveis_ranking()})
            if u.path == "/api/anuncios":
                filtro = "where a.criativo_id is null" if qs.get("sem_criativo") else ""
                return self._json({"anuncios": DB.q(f"""
                    select a.ad_id, a.nome, a.status, a.campanha_nome, a.criativo_id, coalesce(sum(m.gasto),0) gasto
                    from anuncios_meta a left join metricas_meta m on m.ad_id = a.ad_id {filtro}
                    group by a.ad_id order by gasto desc""")})
            return self.send_error(404)
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            return self._json({"erro": str(e)}, 500)

    def do_POST(self):
        u = urlsplit(self.path)
        invalidar_lista()
        try:
            b = self._corpo()
            # --- rotas abertas: entrar e criar o primeiro usuário
            if u.path == "/api/login":
                ip = self._ip()
                if bloqueado(ip):
                    return self._json({"erro": "Muitas tentativas. Espere 15 minutos."}, 429)
                r = DB.q("select id, senha_hash from usuarios where email = %s and ativo",
                         ((b.get("email") or "").strip().lower(),))
                if not r or not confere_senha(b.get("senha") or "", r[0]["senha_hash"]):
                    _falhas.setdefault(ip, []).append(time.time())
                    return self._json({"erro": "E-mail ou senha incorretos."}, 401)
                token = abrir_sessao(r[0]["id"], ip)
                corpo = json.dumps({"ok": True}).encode()
                self.send_response(200)
                self._cookie_sessao(token)
                self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(corpo)))
                self.end_headers(); self.wfile.write(corpo)
                return
            if u.path == "/api/primeiro_acesso":
                if n_usuarios() > 0:
                    return self._json({"erro": "Já existe usuário. Entre com e-mail e senha."}, 403)
                criar_usuario(b.get("email"), b.get("nome"), b.get("senha"))
                return self._json({"ok": True})
            self.usuario = usuario_da_sessao(self._token())
            if not self.usuario:
                return self._json({"erro": "sessão expirada", "login": True}, 401)
            # Protege contra outro site postando no painel com o cookie do navegador.
            origem = self.headers.get("Origin")
            if origem and urlsplit(origem).netloc != self.headers.get("Host"):
                return self._json({"erro": "origem não permitida"}, 403)
            autor = self.usuario["nome"]
            if u.path == "/api/logout":
                fechar_sessao(self._token())
                corpo = b'{"ok": true}'
                self.send_response(200)
                self._cookie_sessao("", apagar=True)
                self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(corpo)))
                self.end_headers(); self.wfile.write(corpo)
                return
            if u.path == "/api/usuarios":
                return self._json(criar_usuario(b.get("email"), b.get("nome"), b.get("senha")))
            if u.path == "/api/senha":
                r = DB.q("select senha_hash from usuarios where id = %s", (self.usuario["id"],))
                if not r or not confere_senha(b.get("atual") or "", r[0]["senha_hash"]):
                    return self._json({"erro": "Senha atual incorreta."}, 400)
                validar_senha(b.get("nova"))
                DB.q("update usuarios set senha_hash = %s where id = %s", (hash_senha(b["nova"]), self.usuario["id"]))
                return self._json({"ok": True})
            if m := re.fullmatch(r"/api/catalogo/(marca|produto|oferta)", u.path):
                return self._json(salvar_catalogo(m.group(1), b))
            if u.path == "/api/criativos/registrar":
                return self._json(registrar_criativo(b))
            if u.path == "/api/esteira":
                return self._json(esteira_acao(b, autor))
            if u.path == "/api/anotacoes":
                cid = b["criativo_id"]
                texto = (b.get("texto") or "").strip()
                if not re.fullmatch(r"C\d{2,3}", cid) or not texto:
                    return self._json({"erro": "criativo e texto são obrigatórios"}, 400)
                tempo = b.get("tempo_s")
                tempo = round(float(tempo), 2) if tempo is not None else None
                take = take_no_tempo(cid, b.get("arquivo"), tempo)
                r = DB.q("""insert into anotacoes (criativo_id, arquivo, tempo_s, take, texto, autor)
                            values (%s,%s,%s,%s,%s,%s) returning *""", (cid, b.get("arquivo"), tempo, take, texto, autor))
                return self._json(r[0] if r else {"erro": "sem banco"}, 200 if r else 503)
            if m := re.fullmatch(r"/api/anotacoes/(\d+)", u.path):
                campos = {k: b[k] for k in ("texto", "status") if k in b}
                if campos.get("status") not in (None, "aberta", "pedida", "feita", "descartada"):
                    return self._json({"erro": "status inválido"}, 400)
                if b.get("apagar"):
                    DB.q("delete from anotacoes where id = %s and status = 'aberta'", (int(m.group(1)),))
                    return self._json({"ok": True})
                for k, v in campos.items():
                    DB.q(f"update anotacoes set {k} = %s where id = %s", (v, int(m.group(1))))
                return self._json({"ok": True})
            if u.path == "/api/refazer":
                r = DB.q("""update anotacoes set status = 'pedida', pedida_em = now()
                            where criativo_id = %s and status = 'aberta' returning id""", (b["criativo_id"],))
                # Em produção, pedir refação devolve o card para o Claude (o mesmo que "Pedir ajuste").
                esteira_estado(b["criativo_id"])          # grava a linha se a etapa ainda era deduzida
                e = DB.q("""update esteira set aguardando = 'claude', atualizado_por = %s, atualizado_em = now()
                            where criativo_id = %s returning etapa""", (autor, b["criativo_id"]))
                if e and r:
                    esteira_evento(b["criativo_id"], e[0]["etapa"], "pediu_ajuste", autor, f"{len(r)} anotação(ões)")
                return self._json({"pedidas": len(r)})
            if u.path == "/api/nota":
                nota = int(b["nota"])
                DB.q("""insert into avaliacoes (criativo_id, autor, nota, comentario) values (%s,%s,%s,%s)
                        on conflict (criativo_id, autor) do update set nota = excluded.nota,
                        comentario = coalesce(excluded.comentario, avaliacoes.comentario), atualizado_em = now()""",
                     (b["criativo_id"], autor, nota, b.get("comentario")))
                return self._json({"ok": True})
            if u.path == "/api/criativo_variaveis":
                if b.get("remover"):
                    DB.q("delete from criativo_variaveis where criativo_id = %s and variavel_id = %s",
                         (b["criativo_id"], b["variavel_id"]))
                else:
                    DB.q("""insert into criativo_variaveis (criativo_id, variavel_id, papel) values (%s,%s,%s)
                            on conflict (criativo_id, variavel_id) do update set papel = excluded.papel""",
                         (b["criativo_id"], b["variavel_id"], b.get("papel") or "base"))
                return self._json({"ok": True})
            if u.path == "/api/resultado":
                if not DB.q("select 1 from criativos where id = %s", (b["criativo_id"],)):
                    return self._json({"erro": "Número manual só para criativo registrado no banco. "
                                               "Peça ao Claude para registrá-lo."}, 400)
                cols = ["criativo_id", "periodo_inicio", "periodo_fim", "moeda", "gasto", "impressoes", "views_3s",
                        "cliques_link", "compras", "receita", "notas"]
                vals = [b.get(c) if b.get(c) not in ("",) else None for c in cols]
                vals[3] = vals[3] or "EUR"
                DB.q(f"""insert into resultados ({', '.join(cols)}) values ({', '.join(['%s'] * len(cols))})
                         on conflict (criativo_id, periodo_inicio, periodo_fim) do update set
                         {', '.join(f'{c} = excluded.{c}' for c in cols[3:])}""", vals)
                return self._json({"ok": True})
            if u.path == "/api/ligar":
                import meta
                meta.ligar(b["ad_id"], b.get("criativo_id") or None)
                return self._json({"ok": True})
            if u.path == "/api/sincronizar":
                if not meta_configurada():
                    return self._json({"ok": False, "erro": "Meta não configurada no .env (ver META.md)."}, 400)
                return self._json(sincronizar_agora(int(b.get("dias") or 30)))
            return self.send_error(404)
        except ValueError as e:                   # erro de validação: mensagem para quem usa
            return self._json({"erro": str(e)}, 400)
        except dados.psycopg.errors.ForeignKeyViolation:
            return self._json({"erro": "Referência inexistente (marca, produto ou oferta)."}, 400)
        except dados.psycopg.errors.UniqueViolation:
            return self._json({"erro": "Já existe um registro com esse valor (ex.: prefixo da marca)."}, 400)
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            return self._json({"erro": str(e)}, 500)


# ---------------------------------------------------------------- linha de comando

def cmd_fila(a):
    pastas = pastas_locais()
    rs = DB.q("select * from anotacoes where status = 'pedida' order by criativo_id, arquivo, tempo_s nulls first, id")
    if not rs:
        print("Fila vazia: nenhum pedido de refação.")
        return
    atual = None
    for r in rs:
        if (r["criativo_id"], r["arquivo"]) != atual:
            atual = (r["criativo_id"], r["arquivo"])
            p = pastas.get(r["criativo_id"])
            print(f"\n{r['criativo_id']}  pasta: {rel(p) if p else '(sem pasta local)'}  arquivo: {r['arquivo'] or '-'}")
        t = f"{float(r['tempo_s']):6.2f}s" if r["tempo_s"] is not None else "  peça "
        print(f"  #{r['id']:<4} {t}  {r['take'] or '--':<5} {r['texto']}  ({r['autor'] or '?'}, {r['pedida_em']:%d/%m %H:%M})")


def cmd_feita(a):
    for i in a.ids:
        DB.q("update anotacoes set status = 'feita', feita_em = now(), resposta = %s where id = %s",
             (a.resposta, int(i)))
    print(f"{len(a.ids)} pedido(s) marcado(s) como feito(s).")


ROTULO = {"fila": "Fila", "analise": "Análise", "roteiro": "Roteiro", "imagens": "Imagens", "takes": "Takes",
          "montagem": "Montagem", "revisao": "Revisão"}


def cmd_esteira(a):
    """O que está com o Claude (e o que espera o dono), com os pedidos de ajuste de cada card."""
    lista = [c for c in lista_criativos() if c.get("esteira")]
    if not lista:
        print("Esteira vazia.")
        return
    pastas = pastas_locais()
    pedidas = {}
    for r in DB.q("select * from anotacoes where status = 'pedida' order by criativo_id, tempo_s nulls first, id"):
        pedidas.setdefault(r["criativo_id"], []).append(r)
    for vez, titulo in (("claude", "COM O CLAUDE (fazer agora, com custo antes)"), ("dono", "AGUARDANDO O DONO")):
        cs = [c for c in lista if c["esteira"]["aguardando"] == vez]
        print(f"\n== {titulo}: {len(cs)}")
        for c in cs:
            e, p = c["esteira"], pastas.get(c["id"])
            print(f"  {c['id']}  {ROTULO.get(e['etapa'], e['etapa']):<9} {c.get('formato') or '-':<12} "
                  f"{c.get('oferta_id') or 'sem oferta':<10} {rel(p) if p else '(sem pasta)'}"
                  + ("  [etapa deduzida dos arquivos]" if e["inferida"] else ""))
            if vez == "claude":
                for r in pedidas.get(c["id"], []):
                    t = f"{float(r['tempo_s']):.1f}s" if r["tempo_s"] is not None else "peça"
                    print(f"      #{r['id']} {t} {r['take'] or ''} {r['texto']}  ({r['autor'] or '?'})")
    print("\nAo terminar uma etapa: painel.py entregar <C##> --etapa <etapa> --custo <US$> [--nota \"...\"]")


def cmd_entregar(a):
    """O Claude terminou a etapa: o card vai para 'aguardando o dono' com o gasto somado."""
    cid = a.criativo.upper()
    etapas = etapas_de(tipo_de(cid) or ("video" if a.etapa in ("takes", "montagem") else None))
    if a.etapa not in etapas:
        sys.exit(f"Etapa inválida. Use uma de: {', '.join(etapas)}")
    DB.q("""insert into esteira (criativo_id, etapa, aguardando, custo_usd, atualizado_por)
            values (%s,%s,'dono',%s,'Claude')
            on conflict (criativo_id) do update set
              desde = case when esteira.etapa = excluded.etapa then esteira.desde else now() end,
              etapa = excluded.etapa, aguardando = 'dono', custo_usd = esteira.custo_usd + excluded.custo_usd,
              atualizado_por = 'Claude', atualizado_em = now()""", (cid, a.etapa, a.custo or 0))
    esteira_evento(cid, a.etapa, "entregou", "Claude", a.nota, a.custo)
    print(f"{cid}: {ROTULO[a.etapa]} entregue para aprovação no painel.")


def cmd_entrar(a):
    """Põe um criativo na esteira (enquanto o Garimpo não existe, é assim que um criativo novo entra)."""
    cid = a.criativo.upper()
    DB.q("""insert into esteira (criativo_id, etapa, aguardando, atualizado_por) values (%s,%s,'claude','Claude')
            on conflict (criativo_id) do nothing""", (cid, a.etapa))
    esteira_evento(cid, a.etapa, "criou", "Claude", a.nota)
    print(f"{cid} na esteira, etapa {ROTULO[a.etapa]}.")


def cmd_usuario(a):
    import getpass
    senha = getpass.getpass("Senha (mín. 10 caracteres, não aparece na tela): ")
    if senha != getpass.getpass("Repita a senha: "):
        sys.exit("As senhas não conferem.")
    try:
        u = criar_usuario(a.email, a.nome, senha)
    except ValueError as e:
        sys.exit(str(e))
    print(f"Usuário criado: {u['nome']} <{u['email']}>")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--porta", type=int, default=8765)
    ap.add_argument("--host", default="127.0.0.1",
                    help="0.0.0.0 abre para a rede local (HTTP sem criptografia: só em rede de confiança)")
    ap.add_argument("--sem-navegador", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("fila").set_defaults(f=cmd_fila)
    p = sub.add_parser("feita"); p.add_argument("ids", nargs="+"); p.add_argument("--resposta", default=None)
    p.set_defaults(f=cmd_feita)
    sub.add_parser("esteira", help="o que está com o Claude e o que espera o dono").set_defaults(f=cmd_esteira)
    p = sub.add_parser("entregar", help="terminei a etapa: card vai para aprovação do dono")
    p.add_argument("criativo"); p.add_argument("--etapa", required=True, choices=ETAPAS)
    p.add_argument("--custo", type=float, default=0.0, help="gasto real da etapa em US$")
    p.add_argument("--nota", default=None, help="o que foi feito (aparece no histórico do card)")
    p.set_defaults(f=cmd_entregar)
    p = sub.add_parser("entrar", help="põe um criativo novo na esteira")
    p.add_argument("criativo"); p.add_argument("--etapa", default="fila", choices=ETAPAS); p.add_argument("--nota", default=None)
    p.set_defaults(f=cmd_entrar)
    p = sub.add_parser("usuario", help="cria um usuário do painel (pede a senha no terminal)")
    p.add_argument("--email", required=True); p.add_argument("--nome", required=True); p.set_defaults(f=cmd_usuario)
    a = ap.parse_args()
    if a.cmd:
        if not DB.ok():
            sys.exit(DB.erro or "Sem banco.")
        return a.f(a)
    if not DB.ok():
        print("Aviso: sem banco (", DB.erro, "). O painel abre só com os arquivos locais.")
    threading.Thread(target=laco_sync, daemon=True).start()
    srv = ThreadingHTTPServer((a.host, a.porta), Handler)
    url = f"http://127.0.0.1:{a.porta}"
    print(f"Painel em {url}  (Ctrl+C para fechar)")
    if a.host != "127.0.0.1":
        print(f"Aberto na rede em {a.host}:{a.porta}. HTTP sem criptografia: use só em rede de confiança.")
    if DB.ok() and n_usuarios() == 0:
        print("Nenhum usuário ainda: o primeiro acesso pede para criar o seu.")
    if not a.sem_navegador:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
