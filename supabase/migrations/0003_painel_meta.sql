-- Painel de criativos + métricas da Meta.
-- anuncios_meta: cada anúncio do Gerenciador, ligado (ou não) a um criativo nosso.
-- metricas_meta: números diários por anúncio, vindos da API da Meta (tools/meta.py sincronizar).
-- anotacoes: pedidos de mudança num ponto exato do vídeo (painel), que viram refação do take.
-- avaliacoes: nota de 0 a 10 por criativo e por pessoa.
-- criativo_variaveis: quais variáveis da biblioteca cada criativo usa (base do ranking por variável).
--
-- criativo_id nestas tabelas é texto 'C<NN>' sem chave estrangeira: criativos em produção
-- ainda não estão na tabela criativos e precisam receber anotação e variáveis.

create table anuncios_meta (
  ad_id           text primary key,
  criativo_id     text check (criativo_id ~ '^C[0-9]{2,3}$'),   -- null = ainda não ligado
  conta_id        text not null,                                 -- 'act_123'
  nome            text not null,
  campanha_id     text,
  campanha_nome   text,
  conjunto_id     text,
  conjunto_nome   text,
  status          text,                                          -- effective_status da Meta
  criado_na_meta  timestamptz,
  ligado_por      text check (ligado_por in ('nome','manual','publicado')),
  sincronizado_em timestamptz not null default now()
);

create table metricas_meta (
  ad_id         text not null references anuncios_meta(ad_id) on delete cascade,
  dia           date not null,
  moeda         text,
  gasto         numeric(12,2) not null default 0,
  impressoes    bigint not null default 0,
  alcance       bigint,
  cliques       bigint not null default 0,          -- todos os cliques
  cliques_link  bigint not null default 0,          -- inline_link_clicks
  views_3s      bigint not null default 0,          -- actions video_view (3 s)
  plays         bigint not null default 0,          -- video_play_actions
  thruplays     bigint not null default 0,          -- 15 s ou até o fim
  p25           bigint not null default 0,
  p50           bigint not null default 0,
  p75           bigint not null default 0,
  p95           bigint not null default 0,
  p100          bigint not null default 0,
  checkouts     int not null default 0,             -- initiate_checkout
  compras       int not null default 0,
  receita       numeric(12,2) not null default 0,
  curva         jsonb,                              -- video_play_curve_actions bruto
  sincronizado_em timestamptz not null default now(),
  primary key (ad_id, dia)
);

create table anotacoes (
  id          bigint generated always as identity primary key,
  criativo_id text not null check (criativo_id ~ '^C[0-9]{2,3}$'),
  arquivo     text,                                 -- caminho relativo do vídeo/imagem anotado
  tempo_s     numeric(7,2),                         -- null = vale para a peça inteira
  take        text,                                 -- 'T05' (calculado pelo montagem.json)
  texto       text not null,
  status      text not null default 'aberta'
              check (status in ('aberta','pedida','feita','descartada')),
  autor       text,
  criado_em   timestamptz not null default now(),
  pedida_em   timestamptz,
  feita_em    timestamptz,
  resposta    text                                  -- o que foi feito (custo, versão nova)
);

create table avaliacoes (
  criativo_id  text not null check (criativo_id ~ '^C[0-9]{2,3}$'),
  autor        text not null,
  nota         smallint not null check (nota between 0 and 10),
  comentario   text,
  atualizado_em timestamptz not null default now(),
  primary key (criativo_id, autor)
);

create table criativo_variaveis (
  criativo_id  text not null check (criativo_id ~ '^C[0-9]{2,3}$'),
  variavel_id  text not null references variaveis(id) on delete cascade,
  papel        text not null default 'base' check (papel in ('base','em_teste')),
  criado_em    timestamptz not null default now(),
  primary key (criativo_id, variavel_id)
);

create index on anuncios_meta (criativo_id);
create index on metricas_meta (dia);
create index on anotacoes (criativo_id, status);
create index on criativo_variaveis (variavel_id);

-- Somatório por criativo: Meta (via anuncios_meta) + lançamentos manuais (resultados).
create view v_criativo_totais with (security_invoker = on) as
with meta as (
  select a.criativo_id,
         sum(m.gasto) gasto, sum(m.impressoes) impressoes, sum(m.cliques_link) cliques_link,
         sum(m.views_3s) views_3s, sum(m.plays) plays, sum(m.thruplays) thruplays,
         sum(m.p25) p25, sum(m.p50) p50, sum(m.p75) p75, sum(m.p95) p95, sum(m.p100) p100,
         sum(m.checkouts) checkouts, sum(m.compras) compras, sum(m.receita) receita,
         min(m.dia) primeiro_dia, max(m.dia) ultimo_dia, max(m.moeda) moeda,
         count(distinct a.ad_id) anuncios
  from anuncios_meta a join metricas_meta m on m.ad_id = a.ad_id
  where a.criativo_id is not null
  group by a.criativo_id
), manual as (
  select criativo_id,
         sum(gasto) gasto, sum(impressoes) impressoes, sum(cliques_link) cliques_link,
         sum(views_3s) views_3s, sum(compras) compras, sum(receita) receita,
         min(periodo_inicio) primeiro_dia, max(periodo_fim) ultimo_dia, max(moeda) moeda
  from resultados group by criativo_id
)
select
  coalesce(meta.criativo_id, manual.criativo_id) as criativo_id,
  coalesce(meta.gasto, 0) + coalesce(manual.gasto, 0) as gasto,
  coalesce(meta.impressoes, 0) + coalesce(manual.impressoes, 0) as impressoes,
  coalesce(meta.cliques_link, 0) + coalesce(manual.cliques_link, 0) as cliques_link,
  coalesce(meta.views_3s, 0) + coalesce(manual.views_3s, 0) as views_3s,
  coalesce(meta.plays, 0) as plays, coalesce(meta.thruplays, 0) as thruplays,
  coalesce(meta.p25, 0) p25, coalesce(meta.p50, 0) p50, coalesce(meta.p75, 0) p75,
  coalesce(meta.p95, 0) p95, coalesce(meta.p100, 0) p100,
  coalesce(meta.checkouts, 0) as checkouts,
  coalesce(meta.compras, 0) + coalesce(manual.compras, 0) as compras,
  coalesce(meta.receita, 0) + coalesce(manual.receita, 0) as receita,
  least(meta.primeiro_dia, manual.primeiro_dia) as primeiro_dia,
  greatest(meta.ultimo_dia, manual.ultimo_dia) as ultimo_dia,
  coalesce(meta.moeda, manual.moeda) as moeda,
  coalesce(meta.anuncios, 0) as anuncios
from meta full join manual on manual.criativo_id = meta.criativo_id;

-- Desempenho por variável: soma dos criativos que usam a variável.
create view v_variavel_desempenho with (security_invoker = on) as
select v.id as variavel_id, v.marca_id, v.categoria, v.variavel, v.valor, v.status,
       count(distinct cv.criativo_id) as criativos,
       count(distinct t.criativo_id) filter (where t.impressoes > 0) as criativos_com_dados,
       sum(t.gasto) gasto, sum(t.impressoes) impressoes, sum(t.cliques_link) cliques_link,
       sum(t.views_3s) views_3s, sum(t.thruplays) thruplays, sum(t.compras) compras, sum(t.receita) receita
from variaveis v
left join criativo_variaveis cv on cv.variavel_id = v.id
left join v_criativo_totais t on t.criativo_id = cv.criativo_id
group by v.id;

do $$
declare t text;
begin
  foreach t in array array['anuncios_meta','metricas_meta','anotacoes','avaliacoes','criativo_variaveis']
  loop
    execute format('alter table %I enable row level security', t);
  end loop;
end $$;
