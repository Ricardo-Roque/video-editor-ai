-- Takes e imagens vão compactados para o R2, para caber nos 10 GB grátis (decidido em 2026-11-26).
-- Take: H.264 CRF 26, mesma resolução (~26% do tamanho, sem diferença visível).
-- Imagem: WebP qualidade 90, mantém transparência (~17%).
-- O original fica no computador de quem gerou; o sha256 continua sendo o do original (detecta mudança).
-- bytes = tamanho guardado no R2; bytes_original = tamanho do original (null = enviado sem compactar).

alter table arquivos add column bytes_original bigint;
