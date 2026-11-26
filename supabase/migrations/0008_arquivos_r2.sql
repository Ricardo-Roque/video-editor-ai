-- Arquivos dos criativos no Cloudflare R2 (decidido em 2026-11-26): mídia e textos de cada criativo ficam num
-- bucket privado, e esta tabela é o índice. Quem não tem o arquivo no computador vê pelo painel (link assinado).
-- Os intermediários da montagem (seg_NN.mp4, assembled.mp4) não sobem: saem de novo dos takes.
-- Guia de configuração: R2.md. Ferramenta: tools/midia.py.

create table arquivos (
  criativo_id    text not null,                      -- C03 / CN05 / CI01
  caminho        text not null,                      -- relativo à pasta do criativo ('takes/T01_v1.mp4');
                                                     -- 'prontos/<nome>' para os arquivos de Vídeos Prontos
  papel          text not null
                 check (papel in ('final','take','imagem','referencia','documento','outro')),
  chave          text not null unique,               -- objeto no bucket
  pasta          text,                               -- pasta do criativo no projeto no último envio
                                                     -- ('Criativo 20', 'Criativos Exemplo/Lo-fi/Criativo 01')
  bytes          bigint not null,
  sha256         text not null,
  tipo_mime      text,
  duracao_s      numeric(8,2),                       -- vídeos
  linha_do_tempo jsonb,                              -- vídeo final: início e fim de cada take (anotação por take)
  enviado_por    text,
  enviado_em     timestamptz not null default now(),
  primary key (criativo_id, caminho)
);
create index on arquivos (papel);

alter table arquivos enable row level security;
