-- Claude automático (decidido em 2026-11-26): o painel dispara o Claude Code sem chat (claude -p) sempre que um
-- card fica "com o Claude". Cada etapa roda sozinha até o limite de gasto (LIMITE_AUTO_USD no .env, padrão
-- US$ 1,00); acima disso, ou quando falta informação, o card volta ao dono com uma pendência.

create table trabalhos (
  id            bigint generated always as identity primary key,
  alvo          text not null,                        -- C23, CN15, PS01
  etapa         text not null,
  chave         text not null unique,                 -- alvo|etapa|atualizado_em do card: o mesmo estado roda uma vez só
  status        text not null default 'rodando' check (status in ('rodando','feito','parado','erro')),
  maquina       text,                                 -- computador que rodou
  motivo        text,                                 -- por que parou (resumo da saída)
  custo_claude_usd numeric(8,3),                      -- custo do Claude Code informado pelo CLI (referência)
  sessao        text,                                 -- session_id do Claude Code
  inicio        timestamptz not null default now(),
  fim           timestamptz
);
create index on trabalhos (alvo, inicio desc);
alter table trabalhos enable row level security;

-- Pendência do card: {"tipo": "gasto", "custo": 2.4, "plano": "..."} ou {"tipo": "pergunta", "texto": "..."}.
-- gasto_liberado: quanto o dono liberou para a próxima rodada desta etapa (zera na entrega).
alter table esteira
  add column pendencia      jsonb,
  add column gasto_liberado numeric(8,3) not null default 0;
alter table provas_sociais
  add column pendencia      jsonb,
  add column gasto_liberado numeric(8,3) not null default 0;

alter table esteira_eventos drop constraint esteira_eventos_acao_check;
alter table esteira_eventos add constraint esteira_eventos_acao_check
  check (acao in ('criou','entregou','aprovou','pediu_ajuste','moveu','descartou','concluiu',
                  'pediu_gasto','liberou_gasto','perguntou','trabalhou'));
