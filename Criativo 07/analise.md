# Análise — Criativo 07

Fonte: `Vídeo Bruto/Criativo #07.mp4`
Formato: 9:16, 360x640, 30 fps, 1:11 (71,3 s), áudio AAC. Idioma: inglês.
Transcrição completa com timestamps: `referencia/transcript.txt`.
Produto do novo criativo: **Cinnarae**. País: França. Idioma: francês.

## Formato geral

Depoimento "falso reclamão" (UGC): uma cliente diz que está "de saco cheio" da marca, mas a reclamação é só porque pagou preço cheio e agora há promoção. O resultado do produto aparece como prova social no meio da reclamação. Um único personagem, um único cenário.

## Estrutura

| # | Tempo | Bloco | Cenário / enquadramento | Fala (resumo) |
|---|-------|-------|-------------------------|---------------|
| 1 | 0,0–11,7 | HOOK — reclamação | Selfie handheld, mulher ~40 anos, loira, cabelo ondulado no ombro, suéter cinza, cozinha americana (armários de madeira, geladeira com ímãs, plafon no teto). Gesto de "pare" com a mão. | "Estou de saco cheio das gomas de magnésio da SP Nutrition. Meninas, não comprem antes de ver isto. Comecei a tomar mês passado e..." |
| 2 | 11,9–18,6 | PROVA — resultados | 11,85–13,98: B-roll da barriga lisa de jeans (corpo, sem rosto). 13,98–16,35: selfie com PiP de dois rostos (inchado × desinchado, antes/depois). Depois volta à selfie. | "...perdi 19 libras. Meu rosto está menos inchado de manhã e não acordo às 3h há semanas." |
| 3 | 18,9–36,8 | VIRADA — oferta | Selfie; segura o pacote do produto (21,9–25,5). | "O problema não são os resultados. Descobri que estão com 20% off, brinde D3+K2 e frete grátis. Paguei preço cheio e sem brinde. Tá de brincadeira?" |
| 4 | 36,9–59,6 | BODY — mecanismo e uso | Selfie; segura uma goma entre os dedos (43,5–59,6). | "Mas estou feliz mesmo assim. Foi a primeira coisa que parou meus despertares às 3h e tirou minha barriga. Tomo duas gomas toda noite. O bisglicinato de magnésio baixa meu cortisol à noite. Sem dieta maluca, sem rotina complicada." |
| 5 | 60,0–71,0 | CTA — escassez | Selfie; segura o pacote (62,3–71). | "Estou um pouco brava por ter pago preço cheio. Mas se você ainda não tentou, não cometa meu erro. Fazem em pequenos lotes, esgota rápido. Garanta a oferta enquanto pode." |

Cortes secos: 11,85 · 13,98 · 16,35 · 18,91 · 21,95 · 25,55 · 36,35 · 43,48 · 62,25 s. Entre eles, jump cuts curtos (troca de take a cada 2–5 s).

## Estilo de edição

- Legenda: frase inteira (não palavra a palavra), caixa branca com texto preto bold, no centro-baixo do quadro. No Criativo 01 usamos legenda 1–3 palavras amarela/branca; aqui a referência usa caixa branca. **Decidir na montagem** (sugestão: manter nosso padrão, que já está pronto no `montar.py`).
- B-roll: 1 plano de barriga de jeans (2 s) + PiP antes/depois de rosto (2,4 s).
- Produto aparece: sim, pacote (pouch) e a goma na mão, em ~40% do vídeo.
- Áudio: só voz, ritmo rápido, muita expressão facial e gestos.

## Imagens necessárias

Personagem:
1. **P1 — Cliente**: mulher francesa ~40 anos, cabelo castanho-claro/loiro-escuro ondulado no ombro, maquiagem leve, suéter de tricô cinza. Folha de referência.

Cenas:
2. **B1 — Selfie cozinha**: P1 em selfie, cozinha francesa (ver adaptações), mãos livres/gesto. Base de hook, virada, body e CTA.
3. **B1b — Selfie segurando o pacote Cinnarae**: precisa da **foto real da embalagem** como `--ref`.
4. **B1c — Selfie segurando uma goma/cápsula**: depende do formato do produto.
5. **O1 — Barriga de jeans** (B-roll, sem rosto). ⚠ política (ver abaixo).
6. **O2a/O2b — Rosto inchado × desinchado** (PiP). ⚠ política.

Total: ~6–7 imagens × US$ 0,04 ≈ **US$ 0,30** (com 1 refação cada, ~US$ 0,55).

## Takes estimados

- ~65 s de fala em ~10 takes de 5–9 s (B1, B1b, B1c).
- O1 e O2 são imagens estáticas com zoom leve na montagem (custo 0), ou 2 takes curtos sem fala.
- Custo estimado (360p, ~US$ 0,023/s): ~70 s × 0,023 ≈ **US$ 1,60**; com testes e correções, **~US$ 2,50**.

## Adaptações culturais para a França

- Libras → quilos (19 lb ≈ 8,6 kg, "presque 9 kilos" ou valor real do produto).
- "3 am" → "3 h du matin".
- Cozinha americana (madeira escura, geladeira grande com ímãs) → cozinha francesa de apartamento/casa: armários claros, azulejo metrô, cafeteira italiana ou Nespresso, baguete/fruteira, janela com venezianas.
- Palavrão do hook ("fucking"): na França "putain" é comum, mas reduz entrega/aprovação no Meta. Sugestão: "J'en ai ras-le-bol de..." (estou de saco cheio).
- "Ladies" → "Les filles".
- Brindes, desconto, frete: trocar pela oferta real da Cinnarae.

## Alertas de política (decisão sua)

- **Depoimento fabricado**: pessoa gerada por IA dizendo "eu tomei e perdi X kg". Na França, a lei dos influenciadores (Loi n° 2023-451) exige a menção "Image virtuelle" em conteúdo comercial com rosto gerado por IA, e a DGCCRF trata depoimento inventado como prática comercial enganosa. Meta também pode reprovar.
- **Antes/depois de corpo e rosto** (O1, O2): Meta proíbe imagens de antes/depois em anúncios de perda de peso.
- **Alegações de saúde** (perder peso, tirar barriga, baixar cortisol, parar de acordar às 3h): não estão na lista autorizada da UE (Reg. 1924/2006) para suplementos. Vou marcar com ⚠ no roteiro e sugerir versões seguras.
