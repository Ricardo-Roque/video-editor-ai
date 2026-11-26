-- Esquema inicial do banco do Editor de Vídeo (Supabase / Postgres).
-- Desenho em ARQUITETURA.md. Os dados do negócio moram aqui; mídia fica no Google Drive (só o link no banco).
-- Listas de valores usam CHECK em vez de ENUM, para poderem crescer sem migração complicada.
-- RLS ligado em todas as tabelas e sem políticas: só a chave de serviço (ferramentas do core) acessa.
-- A interface web vai ganhar políticas próprias quando tiver login.

-- ============================================================
-- Utilitário: atualizado_em automático
-- ============================================================
create or replace function tocar_atualizado_em() returns trigger
language plpgsql as $$
begin
  new.atualizado_em = now();
  return new;
end $$;

-- ============================================================
-- Nível 1: marca
-- ============================================================
create table marcas (
  id            text primary key,                    -- slug: 'cinnarae'
  nome          text not null,
  prefixo       text not null unique,                -- prefixo dos IDs: 'CIN'
  tom           text,                                -- Markdown: tom de voz, padrões de criativo
  proibido      text[] not null default '{}',        -- o que nunca dizer, em qualquer oferta
  notas         text,
  criado_em     timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

create table concorrentes (
  id              text primary key,                  -- slug: 'elmora'
  nome            text not null,
  site            text,
  pagina_meta_id  text,                              -- ID da página na Biblioteca de Anúncios
  notas           text,
  criado_em       timestamptz not null default now(),
  atualizado_em   timestamptz not null default now()
);

create table marca_concorrentes (
  marca_id       text not null references marcas(id),
  concorrente_id text not null references concorrentes(id),
  notas          text,
  primary key (marca_id, concorrente_id)
);

-- ============================================================
-- Nível 2: produto e fatos confirmados
-- ============================================================
create table produtos (
  id            text primary key,                    -- slug: 'gomas-magnesio'
  marca_id      text not null references marcas(id),
  nome          text not null,
  descricao     text,
  criado_em     timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

-- Um fato por linha. "nao_confirmado" deixa explícito o que não pode ser afirmado.
create table fatos (
  id             bigint generated always as identity primary key,
  produto_id     text not null references produtos(id),
  item           text not null,                      -- 'Açúcar', 'Formato da goma'
  valor          text not null,
  status         text not null default 'confirmado'
                 check (status in ('confirmado','nao_confirmado','proibido')),
  confirmado_em  date,
  fonte          text,                               -- 'dono', 'PDP 2026-11-22'
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now(),
  unique (produto_id, item)
);

-- ============================================================
-- Nível 3: oferta (unidade de trabalho) e funil
-- ============================================================
create table ofertas (
  id                 text primary key,               -- 'CIN-FR-01'
  marca_id           text not null references marcas(id),
  produto_id         text not null references produtos(id),
  nome               text not null,                  -- 'França -20% + frete grátis'
  status             text not null default 'ativa'
                     check (status in ('ativa','pausada','encerrada')),
  pais               text not null,                  -- ISO: 'FR'
  idioma             text not null,                  -- 'fr'
  tratamento         text,                           -- 'vous'
  promessa           text,                           -- big idea
  mecanismo_problema text,                           -- UMP
  mecanismo_solucao  text,                           -- UMS
  avatar             text,
  consciencia        text
                     check (consciencia in ('inconsciente','problema','solucao','produto','total')),
  oferta_atual       text,
  oferta_desde       date,
  garantia           text,
  proibido           text[] not null default '{}',   -- além do proibido da marca
  moeda              text not null default 'EUR',
  cpa_breakeven      numeric(10,2),
  roas_alvo          numeric(6,2),
  controle_criativo_id text,                         -- FK adicionada depois de criativos
  notas              text,
  criado_em          timestamptz not null default now(),
  atualizado_em      timestamptz not null default now()
);

create table funil_etapas (
  id         bigint generated always as identity primary key,
  oferta_id  text not null references ofertas(id),
  ordem      int  not null,
  etapa      text not null
             check (etapa in ('anuncio','presell','pdp','checkout','upsell','obrigado','outra')),
  url        text,
  notas      text,
  unique (oferta_id, ordem)
);

-- Texto capturado de cada página do funil, com data. Validade: 14 dias (ver v_capturas_atuais).
create table capturas (
  id             bigint generated always as identity primary key,
  funil_etapa_id bigint not null references funil_etapas(id),
  url            text not null,
  capturado_em   timestamptz not null default now(),
  texto          text not null,                      -- Markdown da página, sem imagens
  hash           text                                -- SHA-1 do texto, para saber se a página mudou
);

-- ============================================================
-- Fontes de referência (só leitura) e referências
-- ============================================================
create table fontes (
  id             text primary key,                   -- 'F-elmora-adlib'
  tipo           text not null
                 check (tipo in ('adlibrary','bot','drive','pasta','url')),
  local          text not null,                      -- caminho, URL ou ID da página
  concorrente_id text references concorrentes(id),
  dono           text,
  notas          text,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

-- Chave estável: 'meta:<ID do anúncio>' | 'arq:<12 primeiros do SHA-1>' | 'url:<URL normalizada>'
create table referencias (
  chave          text primary key
                 check (chave ~ '^(meta|arq|url):.+'),
  fonte_id       text references fontes(id),
  concorrente_id text references concorrentes(id),
  anunciante     text,
  tipo           text not null check (tipo in ('video','nativo','imagem','carrossel')),
  url            text,                               -- link da Biblioteca de Anúncios ou da origem
  arquivo        text,                               -- nome do arquivo na fonte (pode mudar; a chave não)
  midia_url      text,                               -- cópia no Drive, se houver
  no_ar_desde    date,
  visto_em       date,                               -- última vez que vimos ativo
  status         text not null default 'nova'
                 check (status in ('nova','quebrada','modelada','replicada','descartada')),
  dados          jsonb not null default '{}',        -- extras do bot: posição, impressões, variantes
  notas          text,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now()
);

-- ============================================================
-- Quebras e biblioteca de variáveis
-- ============================================================
create table quebras (
  id            text primary key,                    -- 'CIN-Q001'
  marca_id      text not null references marcas(id),
  oferta_id     text references ofertas(id),         -- opcional: quebra avulsa não exige oferta
  data          date not null default current_date,
  titulo        text not null,                       -- '<anunciante> - <tema>'
  conteudo      text not null,                       -- Markdown do quebra.md
  evidencias    text,                                -- Markdown do evidencias.md
  criado_em     timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

create table quebra_referencias (
  quebra_id       text not null references quebras(id),
  referencia_chave text not null references referencias(chave),
  primary key (quebra_id, referencia_chave)
);

-- Mesmas colunas fixas de Variáveis/README.md, mais a marca.
create table variaveis (
  id            text primary key,                    -- 'CIN-V001'
  marca_id      text not null references marcas(id),
  categoria     text not null check (categoria in (
                  'Avatar','Autoridade','UMP','UMS','Consciência','Sofisticação','Lead','Hook',
                  'Formato','Filmagem','Mensageiro','Cenário','Figurino','Estrutura','Texto na tela',
                  'Áudio e ritmo','Imagem (nativo)','Prova','Oferta','CTA')),
  variavel      text not null,
  valor         text not null,
  status        text not null check (status in ('Winner','Loser','Candidate','Random')),
  fonte         text not null,                       -- 'Criativo 05', 'swipe Elmora 1655...', 'CIN-Q001'
  evidencia     text not null default 'sem dados',
  hipotese      text,
  data          date not null default current_date,
  notas         text,
  criado_em     timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

-- ============================================================
-- Criativos
-- ============================================================
create table criativos (
  id             text primary key,                   -- 'C19' (numeração única do projeto)
  oferta_id      text not null references ofertas(id),
  processo       text not null check (processo in ('replica','modelagem')),
  tipo           text not null check (tipo in ('video','nativo','imagem')),
  formato        text not null,                      -- pasta em Criativos Exemplo: 'Lo-fi', 'Nativo'...
  descricao      text,
  idioma         text not null,
  status         text not null default 'em_producao'
                 check (status in ('em_producao','entregue','no_ar','pausado','descartado')),
  quebra_id      text references quebras(id),
  duracao_s      numeric(7,1),
  aspecto        text,                               -- '9:16', '4:5'
  custo_usd      numeric(8,3),
  drive_nome     text,                               -- 'Criativo Nativo #11'
  drive_url      text,                               -- arquivo final no Drive
  nome_anuncio   text,                               -- 'C19 | CIN-T003 | variável: valor'
  licoes         text,                               -- Markdown: o que o criativo ensinou
  criado_em      timestamptz not null default now(),
  entregue_em    timestamptz,
  atualizado_em  timestamptz not null default now()
);

alter table ofertas
  add constraint ofertas_controle_fk foreign key (controle_criativo_id) references criativos(id);

create table criativo_referencias (
  criativo_id      text not null references criativos(id),
  referencia_chave text not null references referencias(chave),
  papel            text not null default 'base'
                   check (papel in ('base','formato','copy','estilo')),
  primary key (criativo_id, referencia_chave)
);

-- Textos do criativo: análise, conceito, roteiro, comparativo, prompts, copy final, notas.
-- Um criativo pode ter várias versões do mesmo tipo (ex.: 07 e 07 Sono): 'nome' diferencia.
create table criativo_documentos (
  id            bigint generated always as identity primary key,
  criativo_id   text not null references criativos(id),
  tipo          text not null check (tipo in (
                  'analise','conceito','roteiro','comparativo','prompts_imagens',
                  'copy_final','takes_config','montagem','fonte','notas')),
  nome          text not null,                       -- nome do arquivo de origem: 'roteiro_fr_sono.md'
  conteudo      text not null,
  atualizado_em timestamptz not null default now(),
  unique (criativo_id, nome)
);

-- ============================================================
-- Testes de conceito e resultados
-- ============================================================
create table testes (
  id                 text primary key,               -- 'CIN-T001'
  marca_id           text not null references marcas(id),
  criativo_id        text references criativos(id),
  data               date not null default current_date,
  vencedoras         text[] not null default '{}',   -- IDs de variaveis
  variavel_em_teste  text not null,                  -- '<variável>: <valor atual> → <valor novo>'
  hipotese           text not null,
  vence_se           text not null,
  perde_se           text not null,
  status             text not null default 'proposto'
                     check (status in ('proposto','em_producao','entregue','no_ar',
                                       'vencedor','perdedor','inconclusivo')),
  resultado          text,
  criado_em          timestamptz not null default now(),
  atualizado_em      timestamptz not null default now()
);

-- Números do Gerenciador, por criativo e período. Manual hoje; API da Meta depois.
create table resultados (
  id              bigint generated always as identity primary key,
  criativo_id     text not null references criativos(id),
  periodo_inicio  date not null,
  periodo_fim     date not null,
  moeda           text not null default 'EUR',
  gasto           numeric(12,2),
  impressoes      bigint,
  views_3s        bigint,
  cliques_link    bigint,
  compras         int,
  receita         numeric(12,2),
  origem          text not null default 'manual' check (origem in ('manual','meta_api')),
  notas           text,
  criado_em       timestamptz not null default now(),
  unique (criativo_id, periodo_inicio, periodo_fim)
);

-- ============================================================
-- Busca por semelhança (pgvector)
-- Embeddings de 384 dimensões gerados localmente por tools/dados.py com
-- intfloat/multilingual-e5-small (grátis, entende francês, português e inglês).
-- Trocar de modelo = nova migração com a nova dimensão e reprocessar.
-- ============================================================
create extension if not exists vector with schema extensions;

alter table referencias          add column resumo text;   -- resumo do anúncio (base do embedding)
alter table referencias          add column embedding extensions.vector(384);
alter table quebras              add column embedding extensions.vector(384);
alter table variaveis            add column embedding extensions.vector(384);
alter table criativo_documentos  add column embedding extensions.vector(384);

create index on referencias         using hnsw (embedding extensions.vector_cosine_ops);
create index on quebras             using hnsw (embedding extensions.vector_cosine_ops);
create index on variaveis           using hnsw (embedding extensions.vector_cosine_ops);
create index on criativo_documentos using hnsw (embedding extensions.vector_cosine_ops);

-- "O que já vimos parecido com isto?" em referências, quebras, variáveis e textos de criativos.
-- marca opcional filtra quebras, variáveis e criativos de uma marca.
create or replace function buscar_parecidos(
  consulta extensions.vector(384),
  limite   int  default 10,
  marca    text default null
) returns table (tipo text, id text, titulo text, similaridade float)
language sql stable
set search_path = public, extensions
as $$
  select * from (
    select 'referencia', r.chave, coalesce(r.anunciante, '') || ' ' || coalesce(left(r.resumo, 120), ''),
           1 - (r.embedding <=> consulta)
    from referencias r where r.embedding is not null
    union all
    select 'quebra', q.id, q.titulo, 1 - (q.embedding <=> consulta)
    from quebras q where q.embedding is not null and (marca is null or q.marca_id = marca)
    union all
    select 'variavel', v.id, v.status || ' | ' || v.variavel || ': ' || left(v.valor, 120),
           1 - (v.embedding <=> consulta)
    from variaveis v where v.embedding is not null and (marca is null or v.marca_id = marca)
    union all
    select 'documento', d.criativo_id || '/' || d.nome, d.tipo, 1 - (d.embedding <=> consulta)
    from criativo_documentos d
    join criativos c on c.id = d.criativo_id
    join ofertas o on o.id = c.oferta_id
    where d.embedding is not null and (marca is null or o.marca_id = marca)
  ) t
  order by 4 desc
  limit limite
$$;

-- ============================================================
-- Índices
-- ============================================================
create index on produtos (marca_id);
create index on fatos (produto_id);
create index on ofertas (marca_id);
create index on funil_etapas (oferta_id);
create index on capturas (funil_etapa_id, capturado_em desc);
create index on referencias (fonte_id);
create index on referencias (concorrente_id);
create index on quebras (marca_id);
create index on quebra_referencias (referencia_chave);
create index on variaveis (marca_id, categoria);
create index on criativos (oferta_id);
create index on criativo_referencias (referencia_chave);
create index on testes (marca_id);
create index on resultados (criativo_id);

-- ============================================================
-- Triggers de atualizado_em
-- ============================================================
do $$
declare t text;
begin
  foreach t in array array['marcas','concorrentes','produtos','fatos','ofertas','fontes','referencias',
                           'quebras','variaveis','criativos','criativo_documentos','testes']
  loop
    execute format('create trigger %I_atualizado before update on %I
                    for each row execute function tocar_atualizado_em()', t, t);
  end loop;
end $$;

-- ============================================================
-- Visões
-- ============================================================

-- Última captura de cada etapa do funil e se está vencida (mais de 14 dias).
create view v_capturas_atuais with (security_invoker = on) as
select distinct on (e.id)
  e.oferta_id, e.ordem, e.etapa, e.url,
  c.id as captura_id, c.capturado_em,
  (c.capturado_em is null or c.capturado_em < now() - interval '14 days') as vencida
from funil_etapas e
left join capturas c on c.funil_etapa_id = e.id
order by e.id, c.capturado_em desc nulls last;

-- "Já vi esse anúncio?": tudo que existe sobre uma referência.
create view v_historico_referencia with (security_invoker = on) as
select
  r.chave, r.anunciante, r.tipo, r.status, r.url,
  coalesce(array_agg(distinct qr.quebra_id) filter (where qr.quebra_id is not null), '{}') as quebras,
  coalesce(array_agg(distinct cr.criativo_id) filter (where cr.criativo_id is not null), '{}') as criativos,
  coalesce(array_agg(distinct c.drive_nome) filter (where c.drive_nome is not null), '{}') as entregas,
  coalesce(array_agg(distinct t.id || ' ' || t.status) filter (where t.id is not null), '{}') as testes
from referencias r
left join quebra_referencias qr on qr.referencia_chave = r.chave
left join criativo_referencias cr on cr.referencia_chave = r.chave
left join criativos c on c.id = cr.criativo_id
left join testes t on t.criativo_id = cr.criativo_id
group by r.chave;

-- Métricas derivadas por período.
create view v_metricas with (security_invoker = on) as
select
  r.*,
  case when r.impressoes > 0 then round(r.views_3s::numeric / r.impressoes, 4) end as hook_rate,
  case when r.impressoes > 0 then round(r.cliques_link::numeric / r.impressoes, 4) end as ctr,
  case when r.compras > 0 then round(r.gasto / r.compras, 2) end as cpa,
  case when r.gasto > 0 then round(r.receita / r.gasto, 2) end as roas
from resultados r;

-- ============================================================
-- Segurança: RLS ligado, sem políticas (só a chave de serviço acessa por enquanto)
-- ============================================================
do $$
declare t text;
begin
  foreach t in array array['marcas','concorrentes','marca_concorrentes','produtos','fatos','ofertas',
                           'funil_etapas','capturas','fontes','referencias','quebras','quebra_referencias',
                           'variaveis','criativos','criativo_referencias','criativo_documentos',
                           'testes','resultados']
  loop
    execute format('alter table %I enable row level security', t);
  end loop;
end $$;
