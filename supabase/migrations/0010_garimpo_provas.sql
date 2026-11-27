-- Garimpo (pedidos de criativo) e provas sociais (decidido em 2026-11-26).
--
-- Garimpo: o dono cola o link da Biblioteca de Anúncios ou sobe o vídeo, escolhe oferta, Réplica ou Modelagem,
-- prioridade e o que quer; aprovar cria o C## / CN## / CI## na Fila da Produção (tabela esteira).
-- Referências antigas (do registro) ficam com triagem nula e não aparecem no quadro do Garimpo.
alter table referencias
  add column triagem        text check (triagem in ('nova','aprovada','reprovada')),
  add column motivo         text,                     -- por que foi reprovada
  add column oferta_alvo    text references ofertas(id),
  add column processo_alvo  text check (processo_alvo in ('replica','modelagem')),
  add column prioridade     smallint check (prioridade between 1 and 3),   -- 1 alta, 2 normal, 3 baixa
  add column pedido         text,                     -- o que o dono quer ("testar hook novo", "trocar a persona")
  add column criativo_id    text,                     -- criativo que a aprovação criou
  add column enviado_por    text,
  add column decidido_por   text,
  add column decidido_em    timestamptz;
alter table referencias alter column triagem set default 'nova';
create index on referencias (triagem) where triagem is not null;

-- O card da esteira guarda o pedido até o Claude registrar o criativo numa oferta (criativos exige formato).
alter table esteira
  add column referencia_chave text,
  add column oferta_id        text,
  add column processo         text check (processo in ('replica','modelagem')),
  add column prioridade       smallint check (prioridade between 1 and 3),
  add column pedido           text;

-- Provas sociais: peças geradas por IA (foto de pessoa com o produto, vídeo de depoimento) só para marcas de
-- demonstração (lojas de exemplo, sem venda real). Em loja real, prova social é de cliente real.
alter table marcas add column demonstracao boolean not null default false;

create table provas_sociais (
  id            text primary key check (id ~ '^PS[0-9]{2,3}$'),     -- PS01, uma sequência só
  marca_id      text not null references marcas(id),
  produto_id    text not null references produtos(id),
  oferta_id     text references ofertas(id),          -- opcional: só quando a peça cita kit, preço ou promoção
  tipo          text not null check (tipo in ('foto','video')),
  idioma        text not null,
  persona       text,                                  -- quem aparece ("mulher de 58 anos, Lyon, aposentada")
  pedido        text,                                  -- o que mostrar ou dizer
  etapa         text not null default 'fila'
                check (etapa in ('fila','texto','imagem','video','revisao','aprovada','descartada')),
  aguardando    text not null default 'claude' check (aguardando in ('claude','dono')),
  texto         text,                                  -- fala do depoimento ou legenda, no idioma da peça
  texto_pt      text,                                  -- tradução para o português
  ajuste        text,                                  -- último pedido de ajuste (vazio quando atendido)
  custo_usd     numeric(8,3) not null default 0,
  criado_por    text,
  criado_em     timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);
create index on provas_sociais (produto_id, etapa);
alter table provas_sociais enable row level security;

-- Histórico das provas sociais usa esteira_eventos (criativo_id = 'PS01').
