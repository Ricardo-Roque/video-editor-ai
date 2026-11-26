-- Mais tipos de texto por criativo: quebra, evidências e arquivos da referência (transcrição, cortes).
alter table criativo_documentos drop constraint criativo_documentos_tipo_check;
alter table criativo_documentos add constraint criativo_documentos_tipo_check check (tipo in (
  'analise','conceito','quebra','roteiro','comparativo','prompts_imagens','copy_final',
  'takes_config','montagem','fonte','evidencias','transcricao','cortes','notas'));

-- Funções com search_path fixo (aviso do linter do Supabase).
alter function tocar_atualizado_em() set search_path = public;
