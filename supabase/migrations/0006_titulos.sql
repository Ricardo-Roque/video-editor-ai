-- Título de exibição dos criativos, com uma sequência por tipo e sem buracos:
--   video  -> "Criativo #NN"
--   nativo -> "Criativo Nativo #NN"
--   imagem -> "Criativo de Imagem #NN"
-- O ID interno (C19, pasta "Criativo 19", prefixo do anúncio "C19 |") não muda: ele liga banco, pastas e Meta.
-- O número é atribuído uma vez (na ordem dos IDs) e não muda depois. Substitui a numeração antiga do Drive.

create table criativo_titulos (
  criativo_id text primary key check (criativo_id ~ '^C[0-9]{2,3}$'),
  serie       text not null check (serie in ('video','nativo','imagem')),
  numero      integer not null check (numero > 0),
  criado_em   timestamptz not null default now(),
  unique (serie, numero)
);

alter table criativo_titulos enable row level security;
