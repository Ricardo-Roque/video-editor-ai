-- Código interno igual ao título, uma sequência por tipo e sem buracos (decidido em 2026-11-26):
--   vídeo  C03  = "Criativo #03"           pasta "Criativo 03"
--   nativo CN05 = "Criativo Nativo #05"    pasta "Criativo Nativo 05"
--   imagem CI01 = "Criativo de Imagem #01" pasta "Criativo de Imagem 01"
-- O nome do anúncio na Meta começa com o código ("CN05 | ..."). A tabela criativo_titulos (0006) fica redundante.
-- Conversão completa dos códigos antigos: CRIATIVOS.md, seção "Códigos antigos".

-- 1. Libera as regras que exigiam o formato antigo (C + número).
alter table anotacoes drop constraint anotacoes_criativo_id_check;
alter table anuncios_meta drop constraint anuncios_meta_criativo_id_check;
alter table avaliacoes drop constraint avaliacoes_criativo_id_check;
alter table criativo_variaveis drop constraint criativo_variaveis_criativo_id_check;
alter table esteira drop constraint esteira_criativo_id_check;
alter table esteira_eventos drop constraint esteira_eventos_criativo_id_check;

-- 2. Chaves estrangeiras passam a seguir a troca de código sozinhas.
alter table criativo_referencias drop constraint criativo_referencias_criativo_id_fkey, add constraint criativo_referencias_criativo_id_fkey foreign key (criativo_id) references criativos(id) on update cascade;
alter table criativo_documentos drop constraint criativo_documentos_criativo_id_fkey, add constraint criativo_documentos_criativo_id_fkey foreign key (criativo_id) references criativos(id) on update cascade;
alter table testes drop constraint testes_criativo_id_fkey, add constraint testes_criativo_id_fkey foreign key (criativo_id) references criativos(id) on update cascade;
alter table resultados drop constraint resultados_criativo_id_fkey, add constraint resultados_criativo_id_fkey foreign key (criativo_id) references criativos(id) on update cascade;
alter table ofertas drop constraint ofertas_controle_fk, add constraint ofertas_controle_fk foreign key (controle_criativo_id) references criativos(id) on update cascade;

-- 3. Conversão antigo -> novo (só os que mudam).
create temp table mapa (velho text primary key, novo text not null unique) on commit drop;
insert into mapa (velho, novo) values
  ('C04','C02'),
  ('C05','C03'),
  ('C06','C04'),
  ('C07','C05'),
  ('C08','C06'),
  ('C09','C07'),
  ('C10','C08'),
  ('C11','C09'),
  ('C12','C10'),
  ('C13','C11'),
  ('C14','C12'),
  ('C15','CN01'),
  ('C16','CN02'),
  ('C17','CN03'),
  ('C18','CN04'),
  ('C19','CN05'),
  ('C20','CN06'),
  ('C21','CN07'),
  ('C22','CN08'),
  ('C23','CN09'),
  ('C24','CN10'),
  ('C25','CN11'),
  ('C26','CN12'),
  ('C27','CN13'),
  ('C28','CN14'),
  ('C29','C13'),
  ('C30','C14'),
  ('C31','C15'),
  ('C32','CI01'),
  ('C33','CI02'),
  ('C34','CI03'),
  ('C35','C16'),
  ('C36','C17'),
  ('C37','C18'),
  ('C38','C19'),
  ('C39','C20'),
  ('C40','C21'),
  ('C41','C22');

-- 4. Em duas fases: o C06 vira C04 enquanto o C04 ainda existe.
update criativos set id = 'tmp_' || id where id in (select velho from mapa);
update criativos x set id = m.novo from mapa m where x.id = 'tmp_' || m.velho;
update anotacoes set criativo_id = 'tmp_' || criativo_id where criativo_id in (select velho from mapa);
update anotacoes x set criativo_id = m.novo from mapa m where x.criativo_id = 'tmp_' || m.velho;
update anuncios_meta set criativo_id = 'tmp_' || criativo_id where criativo_id in (select velho from mapa);
update anuncios_meta x set criativo_id = m.novo from mapa m where x.criativo_id = 'tmp_' || m.velho;
update avaliacoes set criativo_id = 'tmp_' || criativo_id where criativo_id in (select velho from mapa);
update avaliacoes x set criativo_id = m.novo from mapa m where x.criativo_id = 'tmp_' || m.velho;
update criativo_variaveis set criativo_id = 'tmp_' || criativo_id where criativo_id in (select velho from mapa);
update criativo_variaveis x set criativo_id = m.novo from mapa m where x.criativo_id = 'tmp_' || m.velho;
update esteira set criativo_id = 'tmp_' || criativo_id where criativo_id in (select velho from mapa);
update esteira x set criativo_id = m.novo from mapa m where x.criativo_id = 'tmp_' || m.velho;
update esteira_eventos set criativo_id = 'tmp_' || criativo_id where criativo_id in (select velho from mapa);
update esteira_eventos x set criativo_id = m.novo from mapa m where x.criativo_id = 'tmp_' || m.velho;
update criativos set nome_anuncio = regexp_replace(nome_anuncio, '^C[0-9]{2,3}', id) where nome_anuncio ~ '^C[0-9]{2,3}';

-- 5. Formato novo do código: C, CN ou CI + número.
alter table criativos add constraint criativos_id_formato check (id ~ '^C[NI]?[0-9]{2,3}$');
alter table anotacoes add constraint anotacoes_criativo_id_check check (criativo_id ~ '^C[NI]?[0-9]{2,3}$');
alter table anuncios_meta add constraint anuncios_meta_criativo_id_check check (criativo_id ~ '^C[NI]?[0-9]{2,3}$');
alter table avaliacoes add constraint avaliacoes_criativo_id_check check (criativo_id ~ '^C[NI]?[0-9]{2,3}$');
alter table criativo_variaveis add constraint criativo_variaveis_criativo_id_check check (criativo_id ~ '^C[NI]?[0-9]{2,3}$');
alter table esteira add constraint esteira_criativo_id_check check (criativo_id ~ '^C[NI]?[0-9]{2,3}$');
alter table esteira_eventos add constraint esteira_eventos_criativo_id_check check (criativo_id ~ '^C[NI]?[0-9]{2,3}$');

-- 6. O título agora sai do próprio código.
drop table criativo_titulos;
