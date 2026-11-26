-- Login do painel: usuários (dono e sócio) e sessões.
-- Senha guardada só como hash scrypt (tools/painel.py). Sessão: só o SHA-256 do token vai ao banco.

create table usuarios (
  id           bigint generated always as identity primary key,
  email        text not null unique check (email = lower(email)),
  nome         text not null,
  senha_hash   text not null,
  ativo        boolean not null default true,
  criado_em    timestamptz not null default now(),
  ultimo_login timestamptz
);

create table sessoes (
  token_hash  text primary key,
  usuario_id  bigint not null references usuarios(id) on delete cascade,
  criada_em   timestamptz not null default now(),
  expira_em   timestamptz not null,
  ip          text
);
create index on sessoes (usuario_id);

alter table usuarios enable row level security;
alter table sessoes enable row level security;
