-- Esteira de produção no painel: em que etapa cada criativo está e com quem está a vez.
-- Sem chave estrangeira para criativos: um criativo novo entra na esteira antes de ser registrado numa oferta.
-- Saída da esteira: aprovação da revisão (status 'entregue' em criativos) ou descarte.

create table esteira (
  criativo_id    text primary key check (criativo_id ~ '^C[0-9]{2,3}$'),
  etapa          text not null
                 check (etapa in ('fila','analise','roteiro','imagens','takes','montagem','revisao')),
  aguardando     text not null default 'claude' check (aguardando in ('claude','dono')),
  desde          timestamptz not null default now(),          -- quando entrou na etapa atual
  custo_usd      numeric(8,3) not null default 0,              -- soma do gasto em API até agora
  atualizado_por text,
  atualizado_em  timestamptz not null default now()
);

create table esteira_eventos (
  id           bigint generated always as identity primary key,
  criativo_id  text not null check (criativo_id ~ '^C[0-9]{2,3}$'),
  etapa        text not null,
  acao         text not null
               check (acao in ('criou','entregou','aprovou','pediu_ajuste','moveu','descartou','concluiu')),
  autor        text,
  comentario   text,
  custo_usd    numeric(8,3),
  em           timestamptz not null default now()
);
create index on esteira_eventos (criativo_id, em desc);

alter table esteira enable row level security;
alter table esteira_eventos enable row level security;
