"""Ponte com a Meta (Marketing API): métricas dos anúncios e publicação SEMPRE pausada.

Configuração (passo a passo em META.md), no .env:
  META_ACCESS_TOKEN   token do usuário do sistema da BM (nunca exibir, nunca copiar)
  META_AD_ACCOUNT_ID  act_123...
  META_PAGE_ID        página que assina os anúncios (só para publicar)
  META_IG_USER_ID     opcional: conta do Instagram ligada
  META_API_VERSION    opcional (padrão v24.0)

Uso (a partir da raiz do projeto):
  python -I -X utf8 tools/meta.py verificar                       token, permissões, conta e página
  python -I -X utf8 tools/meta.py sincronizar [--dias 30]          anúncios + números diários -> Supabase
  python -I -X utf8 tools/meta.py ligar <ad_id> <C19>              liga um anúncio a um criativo
  python -I -X utf8 tools/meta.py sem-criativo                     anúncios que ainda não têm criativo
  python -I -X utf8 tools/meta.py publicar --criativo C19 --arquivo <video|imagem> --conjunto <adset_id>
         --texto <arquivo.txt> --link <url> [--titulo T] [--descricao D] [--cta SHOP_NOW] [--nome N] [--confirmar]

Ligação anúncio -> criativo: pelo nome do anúncio, que começa com o ID do criativo
("C19 | CIN-T003 | variável: valor") ou contém "Criativo 19". Ligação manual nunca é sobrescrita.

Publicar cria só o anúncio, num conjunto que já existe, com status PAUSED (fixo no código).
Sem --confirmar é ensaio: mostra o que seria criado e não chama a API.
"""
import argparse
import json
import pathlib
import re
import sys
import time
from datetime import date, timedelta

import requests
from dotenv import dotenv_values

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from dados import ROOT, conectar, linhas  # noqa: E402

COMPRAS = ["omni_purchase", "purchase", "offsite_conversion.fb_pixel_purchase"]
CHECKOUTS = ["omni_initiated_checkout", "initiate_checkout", "offsite_conversion.fb_pixel_initiate_checkout"]
CAMPOS_INSIGHTS = ",".join([
    "ad_id", "date_start", "account_currency", "spend", "impressions", "reach", "clicks", "inline_link_clicks",
    "actions", "action_values", "video_play_actions", "video_thruplay_watched_actions",
    "video_p25_watched_actions", "video_p50_watched_actions", "video_p75_watched_actions",
    "video_p95_watched_actions", "video_p100_watched_actions", "video_play_curve_actions",
])
STATUS_TODOS = ["ACTIVE", "PAUSED", "ARCHIVED", "CAMPAIGN_PAUSED", "ADSET_PAUSED", "IN_PROCESS",
                "WITH_ISSUES", "DISAPPROVED", "PENDING_REVIEW", "PREAPPROVED", "PENDING_BILLING_INFO"]


class ErroMeta(Exception):
    pass


def config(exigir_conta=True) -> dict:
    env = dotenv_values(ROOT / ".env")
    c = {
        "token": (env.get("META_ACCESS_TOKEN") or "").strip(),
        "conta": (env.get("META_AD_ACCOUNT_ID") or "").strip(),
        "pagina": (env.get("META_PAGE_ID") or "").strip(),
        "ig": (env.get("META_IG_USER_ID") or "").strip(),
        "versao": (env.get("META_API_VERSION") or "v24.0").strip(),
    }
    if not c["token"]:
        raise ErroMeta("META_ACCESS_TOKEN não está no .env (passo a passo em META.md).")
    if exigir_conta:
        if not c["conta"]:
            raise ErroMeta("META_AD_ACCOUNT_ID não está no .env (formato act_123...).")
        if not c["conta"].startswith("act_"):
            c["conta"] = "act_" + c["conta"]
    return c


def chamar(c, metodo, caminho, params=None, data=None, files=None, timeout=120):
    url = caminho if caminho.startswith("http") else f"https://graph.facebook.com/{c['versao']}/{caminho.lstrip('/')}"
    params = dict(params or {})
    if not caminho.startswith("http"):
        params["access_token"] = c["token"]
    for tentativa in range(4):
        r = requests.request(metodo, url, params=params, data=data, files=files, timeout=timeout)
        if r.status_code < 400:
            return r.json()
        try:
            err = r.json().get("error", {})
        except ValueError:
            err = {"message": r.text[:300]}
        # 4, 17, 32, 613, 80004: limite de chamadas. Espera e tenta de novo.
        if err.get("code") in (4, 17, 32, 613, 80004) and tentativa < 3:
            time.sleep(30 * (tentativa + 1))
            continue
        msg = str(err.get("error_user_msg") or err.get("message") or r.status_code).replace(c["token"], "***")
        raise ErroMeta(f"Meta {r.status_code} (código {err.get('code')}): {msg}")
    raise ErroMeta("Meta: limite de chamadas, tente mais tarde.")


def paginar(c, caminho, params):
    resp = chamar(c, "GET", caminho, params)
    while True:
        yield from resp.get("data", [])
        prox = resp.get("paging", {}).get("next")
        if not prox:
            return
        resp = chamar(c, "GET", prox)


# ---------------------------------------------------------------- leitura dos números

def _soma(lista, tipos=None) -> float:
    if not lista:
        return 0.0
    if tipos is None:
        return sum(float(x.get("value", 0)) for x in lista)
    por_tipo = {x.get("action_type"): float(x.get("value", 0)) for x in lista}
    for t in tipos:                      # o primeiro que existir; somar dobraria a contagem
        if t in por_tipo:
            return por_tipo[t]
    return 0.0


def linha_de_insight(i: dict) -> dict:
    acoes = i.get("actions") or []
    return {
        "ad_id": i["ad_id"],
        "dia": i["date_start"],
        "moeda": i.get("account_currency"),
        "gasto": float(i.get("spend") or 0),
        "impressoes": int(i.get("impressions") or 0),
        "alcance": int(i.get("reach") or 0),
        "cliques": int(i.get("clicks") or 0),
        "cliques_link": int(i.get("inline_link_clicks") or 0),
        "views_3s": int(_soma(acoes, ["video_view"])),
        "plays": int(_soma(i.get("video_play_actions"))),
        "thruplays": int(_soma(i.get("video_thruplay_watched_actions"))),
        "p25": int(_soma(i.get("video_p25_watched_actions"))),
        "p50": int(_soma(i.get("video_p50_watched_actions"))),
        "p75": int(_soma(i.get("video_p75_watched_actions"))),
        "p95": int(_soma(i.get("video_p95_watched_actions"))),
        "p100": int(_soma(i.get("video_p100_watched_actions"))),
        "checkouts": int(_soma(acoes, CHECKOUTS)),
        "compras": int(_soma(acoes, COMPRAS)),
        "receita": _soma(i.get("action_values"), COMPRAS),
        "curva": json.dumps(i.get("video_play_curve_actions")) if i.get("video_play_curve_actions") else None,
    }


def criativo_do_nome(nome: str) -> str | None:
    m = re.match(r"^\s*\[?C(\d{2,3})\b", nome) or re.search(r"\bCriativo\s*#?\s*(\d{2,3})\b", nome, re.I)
    return f"C{int(m.group(1)):02d}" if m else None


def sincronizar(dias: int = 30, log=print) -> dict:
    c = config()
    ate = date.today()
    desde = ate - timedelta(days=dias - 1)
    anuncios = list(paginar(c, f"{c['conta']}/ads", {
        "fields": "id,name,effective_status,created_time,campaign{id,name},adset{id,name}",
        "effective_status": json.dumps(STATUS_TODOS), "limit": 500}))
    insights = list(paginar(c, f"{c['conta']}/insights", {
        "level": "ad", "time_increment": 1, "fields": CAMPOS_INSIGHTS, "limit": 500,
        "time_range": json.dumps({"since": desde.isoformat(), "until": ate.isoformat()})}))
    ligados = 0
    with conectar() as conn:
        manuais = {r["ad_id"] for r in linhas(conn, "select ad_id from anuncios_meta where ligado_por in ('manual','publicado')")}
        for a in anuncios:
            cid = criativo_do_nome(a["name"])
            ligados += bool(cid)
            conn.execute("""
                insert into anuncios_meta (ad_id, criativo_id, conta_id, nome, campanha_id, campanha_nome,
                                           conjunto_id, conjunto_nome, status, criado_na_meta, ligado_por, sincronizado_em)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, now())
                on conflict (ad_id) do update set
                  nome = excluded.nome, campanha_id = excluded.campanha_id, campanha_nome = excluded.campanha_nome,
                  conjunto_id = excluded.conjunto_id, conjunto_nome = excluded.conjunto_nome,
                  status = excluded.status, sincronizado_em = now(),
                  criativo_id = case when anuncios_meta.ad_id = any(%s::text[]) then anuncios_meta.criativo_id
                                     else coalesce(excluded.criativo_id, anuncios_meta.criativo_id) end,
                  ligado_por = case when anuncios_meta.ad_id = any(%s::text[]) then anuncios_meta.ligado_por
                                    else coalesce(excluded.ligado_por, anuncios_meta.ligado_por) end""",
                (a["id"], cid, c["conta"], a["name"], (a.get("campaign") or {}).get("id"),
                 (a.get("campaign") or {}).get("name"), (a.get("adset") or {}).get("id"),
                 (a.get("adset") or {}).get("name"), a.get("effective_status"), a.get("created_time"),
                 "nome" if cid else None, list(manuais), list(manuais)))
        conhecidos = {a["id"] for a in anuncios}
        n = 0
        for i in insights:
            if i["ad_id"] not in conhecidos:      # anúncio apagado: guarda o registro mínimo
                conn.execute("""insert into anuncios_meta (ad_id, conta_id, nome) values (%s,%s,%s)
                                on conflict (ad_id) do nothing""", (i["ad_id"], c["conta"], f"(anúncio {i['ad_id']})"))
            l = linha_de_insight(i)
            cols = list(l)
            conn.execute(
                f"insert into metricas_meta ({', '.join(cols)}, sincronizado_em) values ({', '.join(['%s'] * len(cols))}, now()) "
                f"on conflict (ad_id, dia) do update set "
                + ", ".join(f"{k} = excluded.{k}" for k in cols if k not in ("ad_id", "dia"))
                + ", sincronizado_em = now()",
                [l[k] for k in cols])
            n += 1
    res = {"anuncios": len(anuncios), "ligados_pelo_nome": ligados, "linhas_diarias": n,
           "periodo": f"{desde} a {ate}"}
    log(f"Sincronizado {res['periodo']}: {res['anuncios']} anúncios ({ligados} ligados pelo nome), "
        f"{n} linhas diárias.")
    return res


def ligar(ad_id: str, criativo_id: str | None):
    if criativo_id and not re.fullmatch(r"C\d{2,3}", criativo_id):
        raise ErroMeta("Criativo no formato C19.")
    with conectar() as conn:
        cur = conn.execute("update anuncios_meta set criativo_id = %s, ligado_por = %s where ad_id = %s",
                           (criativo_id, "manual" if criativo_id else None, ad_id))
        if cur.rowcount == 0:
            raise ErroMeta(f"Anúncio {ad_id} não está no banco (rode sincronizar).")


# ---------------------------------------------------------------- publicação (sempre pausada)

def _esperar_video(c, video_id, limite_s=900):
    t0 = time.time()
    while time.time() - t0 < limite_s:
        st = chamar(c, "GET", video_id, {"fields": "status"}).get("status", {})
        if st.get("video_status") == "ready":
            return
        if st.get("video_status") == "error":
            raise ErroMeta(f"A Meta recusou o vídeo: {st}")
        time.sleep(10)
    raise ErroMeta("Vídeo não ficou pronto na Meta em 15 min.")


def publicar(a):
    c = config()
    if not c["pagina"]:
        raise ErroMeta("META_PAGE_ID não está no .env.")
    arq = pathlib.Path(a.arquivo)
    if not arq.is_absolute():
        arq = ROOT / arq
    if not arq.exists():
        raise ErroMeta(f"Arquivo não encontrado: {arq}")
    texto = pathlib.Path(a.texto).read_text(encoding="utf-8").strip()
    video = arq.suffix.lower() in (".mp4", ".mov")
    nome = a.nome or f"{a.criativo} | {arq.stem}"
    if not nome.startswith(a.criativo):
        raise ErroMeta("O nome do anúncio precisa começar com o ID do criativo (ex.: 'C19 | ...').")
    plano = {"conta": c["conta"], "conjunto": a.conjunto, "nome": nome, "status": "PAUSED",
             "tipo": "vídeo" if video else "imagem", "arquivo": str(arq.relative_to(ROOT)) if arq.is_relative_to(ROOT) else str(arq),
             "link": a.link, "titulo": a.titulo, "descricao": a.descricao, "cta": a.cta,
             "texto": texto[:200] + ("…" if len(texto) > 200 else "")}
    print(json.dumps(plano, ensure_ascii=False, indent=2))
    if not a.confirmar:
        print("Ensaio: nada foi enviado. Rode de novo com --confirmar para criar o anúncio PAUSADO.")
        return
    cta = {"type": a.cta, "value": {"link": a.link}}
    if video:
        with arq.open("rb") as f:
            vid = chamar(c, "POST", f"{c['conta']}/advideos", data={"name": nome},
                         files={"source": (arq.name, f, "video/mp4")}, timeout=900)["id"]
        _esperar_video(c, vid)
        thumbs = chamar(c, "GET", f"{vid}/thumbnails").get("data", [])
        thumb = next((t["uri"] for t in thumbs if t.get("is_preferred")), thumbs[0]["uri"] if thumbs else None)
        spec_midia = {"video_data": {"video_id": vid, "image_url": thumb, "message": texto, "call_to_action": cta,
                                     **({"title": a.titulo} if a.titulo else {}),
                                     **({"link_description": a.descricao} if a.descricao else {})}}
    else:
        with arq.open("rb") as f:
            imgs = chamar(c, "POST", f"{c['conta']}/adimages", files={"filename": (arq.name, f)})["images"]
        img_hash = next(iter(imgs.values()))["hash"]
        spec_midia = {"link_data": {"image_hash": img_hash, "link": a.link, "message": texto, "call_to_action": cta,
                                    **({"name": a.titulo} if a.titulo else {}),
                                    **({"description": a.descricao} if a.descricao else {})}}
    spec = {"page_id": c["pagina"], **({"instagram_user_id": c["ig"]} if c["ig"] else {}), **spec_midia}
    criativo = chamar(c, "POST", f"{c['conta']}/adcreatives",
                      data={"name": nome, "object_story_spec": json.dumps(spec)})["id"]
    ad = chamar(c, "POST", f"{c['conta']}/ads", data={
        "name": nome, "adset_id": a.conjunto, "creative": json.dumps({"creative_id": criativo}),
        "status": "PAUSED"})["id"]
    with conectar() as conn:
        conn.execute("""insert into anuncios_meta (ad_id, criativo_id, conta_id, nome, conjunto_id, status, ligado_por)
                        values (%s,%s,%s,%s,%s,'PAUSED','publicado') on conflict (ad_id) do nothing""",
                     (ad, a.criativo, c["conta"], nome, a.conjunto))
    print(f"Anúncio criado PAUSADO: {ad} (criativo de anúncio {criativo}). Revise e ative no Gerenciador.")


# ---------------------------------------------------------------- comandos

def cmd_verificar(a):
    c = config(exigir_conta=False)
    eu = chamar(c, "GET", "me", {"fields": "id,name"})
    print(f"Token de: {eu.get('name')} ({eu.get('id')}), API {c['versao']}")
    perms = chamar(c, "GET", "me/permissions").get("data", [])
    ok = sorted(p["permission"] for p in perms if p.get("status") == "granted")
    print("Permissões:", ", ".join(ok) or "(nenhuma)")
    falta = [p for p in ("ads_read", "ads_management") if p not in ok]
    if falta:
        print("Faltam:", ", ".join(falta))
    if c["conta"]:
        conta = c["conta"] if c["conta"].startswith("act_") else "act_" + c["conta"]
        info = chamar(c, "GET", conta, {"fields": "name,currency,account_status,timezone_name"})
        print(f"Conta: {info.get('name')} ({conta}), moeda {info.get('currency')}, fuso {info.get('timezone_name')}, "
              f"status {info.get('account_status')} (1 = ativa)")
    else:
        print("META_AD_ACCOUNT_ID ausente. Contas que o token enxerga:")
        for x in paginar(c, "me/adaccounts", {"fields": "id,name,currency", "limit": 100}):
            print(f"  {x['id']}  {x.get('name')}  {x.get('currency')}")
    if c["pagina"]:
        pg = chamar(c, "GET", c["pagina"], {"fields": "name"})
        print(f"Página: {pg.get('name')} ({c['pagina']})")
    else:
        print("META_PAGE_ID ausente (só necessário para publicar).")


def cmd_sem_criativo(a):
    with conectar() as conn:
        rs = linhas(conn, """select a.ad_id, a.nome, a.status, a.campanha_nome, coalesce(sum(m.gasto),0) gasto
                             from anuncios_meta a left join metricas_meta m on m.ad_id = a.ad_id
                             where a.criativo_id is null group by a.ad_id order by gasto desc""")
    for r in rs:
        print(f"{r['ad_id']}  {r['status'] or '':<16} gasto {float(r['gasto']):>9.2f}  {r['nome']}  [{r['campanha_nome'] or ''}]")
    print(f"{len(rs)} anúncio(s) sem criativo. Ligue com: tools/meta.py ligar <ad_id> C19")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("verificar").set_defaults(f=cmd_verificar)
    p = sub.add_parser("sincronizar"); p.add_argument("--dias", type=int, default=30)
    p.set_defaults(f=lambda a: sincronizar(a.dias))
    p = sub.add_parser("ligar"); p.add_argument("ad_id"); p.add_argument("criativo")
    p.set_defaults(f=lambda a: (ligar(a.ad_id, a.criativo), print(f"{a.ad_id} -> {a.criativo}")))
    sub.add_parser("sem-criativo").set_defaults(f=cmd_sem_criativo)
    p = sub.add_parser("publicar")
    p.add_argument("--criativo", required=True); p.add_argument("--arquivo", required=True)
    p.add_argument("--conjunto", required=True, help="ID do conjunto de anúncios (adset) que já existe")
    p.add_argument("--texto", required=True, help="arquivo .txt com o texto principal do anúncio")
    p.add_argument("--link", required=True); p.add_argument("--titulo"); p.add_argument("--descricao")
    p.add_argument("--cta", default="SHOP_NOW"); p.add_argument("--nome")
    p.add_argument("--confirmar", action="store_true", help="sem isso é só ensaio")
    p.set_defaults(f=publicar)
    a = ap.parse_args()
    try:
        a.f(a)
    except ErroMeta as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
