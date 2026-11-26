"""Ponte entre o core e o banco do negócio (Supabase / Postgres). Desenho em ARQUITETURA.md.

Uso (a partir da raiz do projeto):
  python -I -X utf8 tools/dados.py contexto <oferta>              portão de contexto: marca, produto, fatos, oferta, funil, o que falta
  python -I -X utf8 tools/dados.py chave <link|arquivo>           chave estável da referência (meta:, arq:, url:)
  python -I -X utf8 tools/dados.py buscar <link|arquivo|chave>    "já vi?": quebras, criativos, entregas, testes e números ligados
  python -I -X utf8 tools/dados.py parecidos "<texto>" [--marca M] [--limite N]   busca por semelhança
  python -I -X utf8 tools/dados.py capturar <oferta> <etapa> [--url URL | --arquivo texto.md]   captura de página do funil
  python -I -X utf8 tools/dados.py gravar <tabela> <arquivo.json> inserir ou atualizar linhas (objeto ou lista de objetos)
  python -I -X utf8 tools/dados.py embeddings [--tabela T] [--refazer]   gerar embeddings que faltam
  python -I -X utf8 tools/dados.py sql "<select ...>"             consulta somente leitura
  python -I -X utf8 tools/dados.py migrar supabase/migrations/NNNN_x.sql   aplica uma migração (uma transação)

Conexão: SUPABASE_DB_URL no .env (Session pooler). Senha com caracteres especiais é tratada aqui.
Embeddings: multilingual-e5-small (ONNX quantizado, 384 dimensões), local e grátis. Baixa ~120 MB no
primeiro uso. Todos do time precisam usar o mesmo modelo e revisão, senão a busca mistura vetores diferentes.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys
from datetime import date, datetime
from decimal import Decimal
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

import psycopg
from dotenv import dotenv_values
from psycopg.types.json import Jsonb

ROOT = pathlib.Path(__file__).resolve().parent.parent

MODELO_REPO = "Xenova/multilingual-e5-small"
MODELO_REVISAO = "761b726dd34fb83930e26aab4e9ac3899aa1fa78"
MODELO_ARQUIVO = "onnx/model_quantized.onnx"
DIMENSOES = 384
MAX_TOKENS = 512
VALIDADE_CAPTURA_DIAS = 14

# Texto que vira embedding, por tabela: (colunas da chave primária, SQL que monta o texto)
EMBED = {
    "referencias": ("chave", "concat_ws(' | ', anunciante, tipo, resumo, notas)"),
    "quebras": ("id", "concat_ws(E'\\n', titulo, conteudo)"),
    "variaveis": ("id", "concat_ws(' | ', categoria, variavel, valor, hipotese, notas)"),
    "criativo_documentos": ("id", "concat_ws(E'\\n', tipo, nome, conteudo)"),
}

CAMPOS_OBRIGATORIOS_OFERTA = {
    "pais": "país",
    "idioma": "idioma",
    "promessa": "promessa principal (big idea)",
    "avatar": "avatar",
    "oferta_atual": "oferta atual",
    "garantia": "garantia",
}


# ---------------------------------------------------------------- conexão

def conectar() -> psycopg.Connection:
    raw = dotenv_values(ROOT / ".env").get("SUPABASE_DB_URL")
    if not raw:
        sys.exit("SUPABASE_DB_URL não está no .env (Supabase > Connect > Direct > Session pooler).")
    m = re.match(r"^(postgres(?:ql)?://)([^:/]+):(.*)@([^@/]+)/(.+)$", raw.strip())
    if not m:
        sys.exit("SUPABASE_DB_URL em formato inesperado (esperado postgresql://usuario:senha@host:porta/banco).")
    pre, usuario, senha, host, banco = m.groups()
    url = f"{pre}{usuario}:{quote(senha, safe='')}@{host}/{banco}"
    try:
        return psycopg.connect(url, connect_timeout=20)
    except psycopg.OperationalError as e:
        sys.exit("Não conectou ao banco: " + str(e).replace(senha, "***")[:300])


def linhas(conn, sql, params=None):
    cur = conn.execute(sql, params)
    cols = [d.name for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def para_json(v):
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return str(v)


# ---------------------------------------------------------------- chave estável

def chave_de(alvo: str) -> str:
    alvo = alvo.strip()
    if re.match(r"^(meta|arq|url):.+", alvo):
        return alvo
    if re.fullmatch(r"\d{12,20}", alvo):
        return f"meta:{alvo}"
    if re.match(r"^https?://", alvo, re.I):
        partes = urlsplit(alvo)
        consulta = dict(parse_qsl(partes.query))
        if "facebook.com" in partes.netloc.lower() and "/ads/library" in partes.path and consulta.get("id"):
            return f"meta:{consulta['id']}"
        manter = [(k, v) for k, v in parse_qsl(partes.query)
                  if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid", "ttclid"}]
        caminho = partes.path.rstrip("/") or "/"
        return "url:" + urlunsplit((partes.scheme.lower(), partes.netloc.lower(), caminho, urlencode(manter), ""))
    p = pathlib.Path(alvo)
    if p.is_file():
        h = hashlib.sha1()
        with p.open("rb") as f:
            for bloco in iter(lambda: f.read(1 << 20), b""):
                h.update(bloco)
        return f"arq:{h.hexdigest()[:12]}"
    sys.exit(f"Não sei fazer a chave de: {alvo} (link, ID da Biblioteca de Anúncios, arquivo existente ou chave).")


# ---------------------------------------------------------------- embeddings

_modelo = None


def _carregar_modelo():
    global _modelo
    if _modelo is None:
        import os
        os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
        import numpy as np
        import onnxruntime as ort
        from huggingface_hub import hf_hub_download
        from tokenizers import Tokenizer

        caminho = hf_hub_download(MODELO_REPO, MODELO_ARQUIVO, revision=MODELO_REVISAO)
        tok = Tokenizer.from_file(hf_hub_download(MODELO_REPO, "tokenizer.json", revision=MODELO_REVISAO))
        tok.enable_truncation(MAX_TOKENS)
        tok.enable_padding()
        sessao = ort.InferenceSession(caminho, providers=["CPUExecutionProvider"])
        _modelo = (np, tok, sessao, {i.name for i in sessao.get_inputs()})
    return _modelo


def embutir(textos: list[str], tipo: str = "passage") -> list[list[float]]:
    """tipo: 'passage' para o que é guardado, 'query' para o que se procura (convenção do e5)."""
    np, tok, sessao, entradas = _carregar_modelo()
    saida = []
    for i in range(0, len(textos), 16):
        lote = tok.encode_batch([f"{tipo}: {t}" for t in textos[i:i + 16]])
        ids = np.array([e.ids for e in lote], dtype=np.int64)
        mask = np.array([e.attention_mask for e in lote], dtype=np.int64)
        feed = {"input_ids": ids, "attention_mask": mask}
        if "token_type_ids" in entradas:
            feed["token_type_ids"] = np.zeros_like(ids)
        ultimo = sessao.run(None, feed)[0]                      # (lote, tokens, 384)
        m = mask[..., None].astype(np.float32)
        media = (ultimo * m).sum(1) / np.clip(m.sum(1), 1e-9, None)
        media /= np.linalg.norm(media, axis=1, keepdims=True)
        saida.extend(media.tolist())
    return saida


def vetor_sql(v: list[float]) -> str:
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"


def preencher_embeddings(conn, tabela: str, refazer: bool = False, ids: list | None = None) -> int:
    pk, texto_sql = EMBED[tabela]
    filtro = "true" if refazer else "embedding is null"
    params = None
    if ids:
        filtro += f" and {pk} = any(%s)"
        params = (ids,)
    pendentes = linhas(conn, f"select {pk} as pk, {texto_sql} as texto from {tabela} where {filtro}", params)
    pendentes = [p for p in pendentes if (p["texto"] or "").strip()]
    if not pendentes:
        return 0
    vetores = embutir([p["texto"] for p in pendentes])
    with conn.cursor() as cur:
        cur.executemany(
            f"update {tabela} set embedding = %s::extensions.vector where {pk} = %s",
            [(vetor_sql(v), p["pk"]) for v, p in zip(vetores, pendentes)],
        )
    return len(pendentes)


# ---------------------------------------------------------------- comandos

def cmd_chave(a):
    print(chave_de(a.alvo))


def cmd_buscar(a):
    chave = chave_de(a.alvo)
    with conectar() as conn:
        ref = linhas(conn, "select * from referencias where chave = %s", (chave,))
        if not ref and pathlib.Path(a.alvo).is_file():
            ref = linhas(conn, "select * from referencias where arquivo = %s", (pathlib.Path(a.alvo).name,))
        if not ref:
            print(f"{chave}: nunca visto. Nenhuma referência com essa chave no banco.")
            return
        r = ref[0]
        h = linhas(conn, "select * from v_historico_referencia where chave = %s", (r["chave"],))[0]
        nums = linhas(conn, """
            select m.criativo_id, m.periodo_inicio, m.periodo_fim, m.gasto, m.hook_rate, m.ctr, m.cpa, m.roas
            from v_metricas m join criativo_referencias cr on cr.criativo_id = m.criativo_id
            where cr.referencia_chave = %s order by m.periodo_fim desc""", (r["chave"],))
    if a.json:
        print(json.dumps({"referencia": r | {"embedding": None}, "historico": h, "resultados": nums},
                         default=para_json, ensure_ascii=False, indent=2))
        return
    print(f"{r['chave']}: JÁ VISTO. {r['anunciante'] or ''} ({r['tipo']}), status {r['status']}")
    if r.get("url"):
        print(f"  link: {r['url']}")
    print(f"  quebras: {', '.join(h['quebras']) or 'nenhuma'}")
    print(f"  criativos: {', '.join(h['criativos']) or 'nenhum'}")
    print(f"  entregas no Drive: {', '.join(h['entregas']) or 'nenhuma'}")
    print(f"  testes: {', '.join(h['testes']) or 'nenhum'}")
    for n in nums:
        print(f"  resultado {n['criativo_id']} {n['periodo_inicio']}..{n['periodo_fim']}: gasto {n['gasto']}, "
              f"hook {n['hook_rate']}, CTR {n['ctr']}, CPA {n['cpa']}, ROAS {n['roas']}")


def cmd_parecidos(a):
    vetor = embutir([a.texto], tipo="query")[0]
    with conectar() as conn:
        res = linhas(conn, "select * from buscar_parecidos(%s::extensions.vector, %s, %s)",
                     (vetor_sql(vetor), a.limite, a.marca))
    if not res:
        print("Nada no banco com embedding ainda (rode: dados.py embeddings).")
    for r in res:
        print(f"{r['similaridade']:.3f}  {r['tipo']:<10} {r['id']:<28} {r['titulo']}")


def cmd_contexto(a):
    with conectar() as conn:
        of = linhas(conn, "select * from ofertas where id = %s", (a.oferta,))
        if not of:
            existentes = [r["id"] for r in linhas(conn, "select id from ofertas order by id")]
            sys.exit(f"Oferta {a.oferta} não existe. Ofertas no banco: {', '.join(existentes) or 'nenhuma'}.")
        o = of[0]
        marca = linhas(conn, "select * from marcas where id = %s", (o["marca_id"],))[0]
        conc = linhas(conn, """select c.nome, c.site from marca_concorrentes mc
                               join concorrentes c on c.id = mc.concorrente_id where mc.marca_id = %s""",
                      (marca["id"],))
        prod = linhas(conn, "select * from produtos where id = %s", (o["produto_id"],))[0]
        fatos = linhas(conn, "select item, valor, status, confirmado_em, fonte from fatos "
                             "where produto_id = %s order by status, item", (prod["id"],))
        funil = linhas(conn, "select * from v_capturas_atuais where oferta_id = %s order by ordem", (o["id"],))
        notas_funil = {r["ordem"]: r["notas"] for r in
                       linhas(conn, "select ordem, notas from funil_etapas where oferta_id = %s", (o["id"],))}
        paginas = []
        if a.paginas:
            paginas = linhas(conn, """
                select e.etapa, c.url, c.capturado_em, c.texto from v_capturas_atuais v
                join capturas c on c.id = v.captura_id
                join funil_etapas e on e.oferta_id = v.oferta_id and e.ordem = v.ordem
                where v.oferta_id = %s order by v.ordem""", (o["id"],))

    falta = [rotulo for campo, rotulo in CAMPOS_OBRIGATORIOS_OFERTA.items() if not o.get(campo)]
    etapas = {f["etapa"]: f for f in funil}
    if not (etapas.get("pdp") or {}).get("url"):
        falta.append("URL da página de venda (pdp)")
    if "presell" not in etapas:
        falta.append("pre-sell: usa ou não? (sem etapa 'presell' no funil)")
    vencidas = [f["etapa"] for f in funil if f["url"] and f["vencida"]]

    print(f"# Contexto da oferta {o['id']}: {o['nome']} ({o['status']})\n")
    print(f"## Marca: {marca['nome']} (prefixo {marca['prefixo']})")
    if marca["tom"]:
        print(marca["tom"])
    if marca["proibido"]:
        print("Proibido na marca: " + "; ".join(marca["proibido"]))
    if conc:
        print("Concorrentes: " + "; ".join(f"{c['nome']} ({c['site'] or '-'})" for c in conc))
    print(f"\n## Produto: {prod['nome']}")
    if prod["descricao"]:
        print(prod["descricao"])
    for f in fatos:
        marca_status = {"confirmado": "", "nao_confirmado": " [NÃO CONFIRMADO: não afirmar]",
                        "proibido": " [PROIBIDO]"}[f["status"]]
        quando = f" ({f['confirmado_em']}, {f['fonte']})" if f["confirmado_em"] or f["fonte"] else ""
        print(f"- {f['item']}: {f['valor']}{marca_status}{quando}")
    print("\n## Oferta")
    for campo in ["pais", "idioma", "tratamento", "promessa", "mecanismo_problema", "mecanismo_solucao",
                  "avatar", "consciencia", "oferta_atual", "oferta_desde", "garantia", "moeda",
                  "cpa_breakeven", "roas_alvo", "controle_criativo_id"]:
        print(f"- {campo}: {o[campo] if o[campo] is not None else '(não informado)'}")
    if o["proibido"]:
        print("- proibido nesta oferta: " + "; ".join(o["proibido"]))
    if o["notas"]:
        print(f"\n{o['notas']}")
    print("\n## Funil")
    for f in funil:
        if not f["url"]:
            estado = notas_funil.get(f["ordem"]) or "sem URL"
        elif f["captura_id"] is None:
            estado = "NUNCA CAPTURADA"
        else:
            estado = f"capturada em {f['capturado_em']:%Y-%m-%d}" + (" (VENCIDA)" if f["vencida"] else "")
        print(f"{f['ordem']}. {f['etapa']}: {f['url'] or '-'} | {estado}")
    for p in paginas:
        print(f"\n### Página {p['etapa']} ({p['url']}, {p['capturado_em']:%Y-%m-%d})\n\n{p['texto']}")
    print("\n## Portão")
    if falta:
        print("FALTA (perguntar ao dono, não inventar): " + "; ".join(falta))
    if vencidas:
        print(f"CAPTURA VENCIDA ou inexistente (> {VALIDADE_CAPTURA_DIAS} dias): {', '.join(vencidas)}. "
              f"Recapturar: dados.py capturar {o['id']} <etapa>")
    if not falta and not vencidas:
        print("OK: contexto completo e capturas em dia.")


def _texto_de_html(html: str) -> str:
    from bs4 import BeautifulSoup
    sopa = BeautifulSoup(html, "html.parser")
    for t in sopa(["script", "style", "noscript", "svg", "iframe", "template"]):
        t.decompose()
    titulo = sopa.title.get_text(strip=True) if sopa.title else ""
    corpo = sopa.body or sopa
    texto = corpo.get_text("\n")
    linhas_ = [re.sub(r"\s+", " ", ln).strip() for ln in texto.splitlines()]
    limpo, anterior = [], None
    for ln in linhas_:
        if ln and ln != anterior:
            limpo.append(ln)
        anterior = ln
    return (f"# {titulo}\n\n" if titulo else "") + "\n".join(limpo)


def cmd_capturar(a):
    with conectar() as conn:
        et = linhas(conn, "select * from funil_etapas where oferta_id = %s and etapa = %s order by ordem",
                    (a.oferta, a.etapa))
        if not et:
            sys.exit(f"A oferta {a.oferta} não tem etapa '{a.etapa}' no funil. Cadastre com: dados.py gravar funil_etapas ...")
        e = et[0]
        url = a.url or e["url"]
        if not url:
            sys.exit("Etapa sem URL. Passe --url ou cadastre a URL na etapa.")
        if a.arquivo:
            texto = pathlib.Path(a.arquivo).read_text(encoding="utf-8")
        else:
            import requests
            r = requests.get(url, timeout=30, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"})
            if r.status_code != 200:
                sys.exit(f"A página respondeu {r.status_code} (loja bloqueando acesso automático, comum na Shopify). "
                         "Capture com o Claude in Chrome (get_page_text), salve o texto em .md no scratchpad e rode "
                         f"de novo com --arquivo <caminho>.")
            texto = _texto_de_html(r.text)
        if len(texto) < 300:
            print(f"Aviso: só {len(texto)} caracteres capturados. Página montada por JavaScript? "
                  "Capture com o Claude in Chrome (get_page_text), salve em .md e use --arquivo.")
        h = hashlib.sha1(texto.encode("utf-8")).hexdigest()
        ultima = linhas(conn, "select hash, capturado_em from capturas where funil_etapa_id = %s "
                              "order by capturado_em desc limit 1", (e["id"],))
        conn.execute("insert into capturas (funil_etapa_id, url, texto, hash) values (%s, %s, %s, %s)",
                     (e["id"], url, texto, h))
        if a.url and a.url != e["url"]:
            conn.execute("update funil_etapas set url = %s where id = %s", (a.url, e["id"]))
    mudou = "primeira captura" if not ultima else (
        "SEM MUDANÇA desde " + f"{ultima[0]['capturado_em']:%Y-%m-%d}" if ultima[0]["hash"] == h
        else "A PÁGINA MUDOU desde " + f"{ultima[0]['capturado_em']:%Y-%m-%d}")
    print(f"Capturado {a.oferta}/{a.etapa}: {len(texto)} caracteres, {mudou}.")


def cmd_gravar(a):
    dados = json.loads(pathlib.Path(a.arquivo).read_text(encoding="utf-8"))
    if isinstance(dados, dict):
        dados = [dados]
    with conectar() as conn:
        pk = [r["attname"] for r in linhas(conn, """
            select a.attname from pg_index i
            join pg_attribute a on a.attrelid = i.indrelid and a.attnum = any(i.indkey)
            where i.indrelid = %s::regclass and i.indisprimary""", (f"public.{a.tabela}",))]
        tipos = {r["column_name"]: r["data_type"] for r in linhas(conn, """
            select column_name, data_type from information_schema.columns
            where table_schema = 'public' and table_name = %s""", (a.tabela,))}
        if not tipos:
            sys.exit(f"Tabela {a.tabela} não existe.")
        ids = []
        for linha in dados:
            desconhecidas = set(linha) - set(tipos)
            if desconhecidas:
                sys.exit(f"Colunas que não existem em {a.tabela}: {', '.join(sorted(desconhecidas))}")
            linha = {k: (Jsonb(v) if tipos[k] == "jsonb" else v) for k, v in linha.items()}
            if "embedding" in tipos:
                linha["embedding"] = None              # texto mudou: o embedding é refeito abaixo
            cols = list(linha)
            chave_ok = all(c in linha for c in pk)
            conflito = ""
            if chave_ok:
                atualizar = [c for c in cols if c not in pk]
                conflito = (f" on conflict ({', '.join(pk)}) do update set "
                            + ", ".join(f"{c} = excluded.{c}" for c in atualizar)) if atualizar else \
                           f" on conflict ({', '.join(pk)}) do nothing"
            sql = (f"insert into {a.tabela} ({', '.join(cols)}) values ({', '.join(['%s'] * len(cols))})"
                   f"{conflito} returning {', '.join(pk)}")
            ret = conn.execute(sql, [linha[c] for c in cols]).fetchone()
            if ret:
                ids.append(ret[0] if len(pk) == 1 else ret)
        n_emb = 0
        if a.tabela in EMBED and ids:
            n_emb = preencher_embeddings(conn, a.tabela, ids=ids)
    print(f"{a.tabela}: {len(ids)} linha(s) gravada(s)" + (f", {n_emb} embedding(s)" if n_emb else "") + ".")


def cmd_embeddings(a):
    tabelas = [a.tabela] if a.tabela else list(EMBED)
    with conectar() as conn:
        for t in tabelas:
            n = preencher_embeddings(conn, t, refazer=a.refazer)
            print(f"{t}: {n} embedding(s) gerado(s).")


def cmd_sql(a):
    with conectar() as conn:
        conn.execute("set transaction read only")
        res = linhas(conn, a.consulta)
    for r in res:
        r.pop("embedding", None)
    print(json.dumps(res, default=para_json, ensure_ascii=False, indent=2))


def cmd_migrar(a):
    sql = pathlib.Path(a.arquivo).read_text(encoding="utf-8")
    with conectar() as conn:            # uma transação: ou aplica tudo, ou nada
        conn.execute(sql)
    print(f"Migração aplicada: {pathlib.Path(a.arquivo).name}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("contexto"); p.add_argument("oferta")
    p.add_argument("--paginas", action="store_true", help="incluir o texto das páginas capturadas")
    p.set_defaults(f=cmd_contexto)
    p = sub.add_parser("chave"); p.add_argument("alvo"); p.set_defaults(f=cmd_chave)
    p = sub.add_parser("buscar"); p.add_argument("alvo"); p.add_argument("--json", action="store_true")
    p.set_defaults(f=cmd_buscar)
    p = sub.add_parser("parecidos"); p.add_argument("texto"); p.add_argument("--marca")
    p.add_argument("--limite", type=int, default=10); p.set_defaults(f=cmd_parecidos)
    p = sub.add_parser("capturar"); p.add_argument("oferta"); p.add_argument("etapa")
    g = p.add_mutually_exclusive_group(); g.add_argument("--url"); g.add_argument("--arquivo")
    p.set_defaults(f=cmd_capturar)
    p = sub.add_parser("gravar"); p.add_argument("tabela"); p.add_argument("arquivo"); p.set_defaults(f=cmd_gravar)
    p = sub.add_parser("embeddings"); p.add_argument("--tabela", choices=list(EMBED))
    p.add_argument("--refazer", action="store_true"); p.set_defaults(f=cmd_embeddings)
    p = sub.add_parser("sql"); p.add_argument("consulta"); p.set_defaults(f=cmd_sql)
    p = sub.add_parser("migrar"); p.add_argument("arquivo"); p.set_defaults(f=cmd_migrar)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
