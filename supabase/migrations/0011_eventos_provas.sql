-- O histórico das provas sociais (PS01...) usa esteira_eventos, junto com o dos criativos (C03 / CN05 / CI01).
alter table esteira_eventos drop constraint esteira_eventos_criativo_id_check;
alter table esteira_eventos add constraint esteira_eventos_criativo_id_check
  check (criativo_id ~ '^(C[NI]?|PS)[0-9]{2,3}$');
