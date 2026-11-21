# Roteiro FR — Criativo 06 (decupagem por take)

Base: transcrição da referência (`referencia/transcript.txt`), traduzida para o francês falado, mesma ordem, sem cortes nem acréscimos.
Personagem: profissional de saúde francesa fictícia de ~50 anos, scrub azul royal, de pé num quarto de hospital (mesmo visual da referência, rosto novo). Produto não aparece, como na referência. Sem a menção "Image virtuelle" (padrão do usuário).
Decisão do usuário (2026-11-19): copy fiel e agressiva, riscos de política aceitos.

Adaptações (só o que não existe ou não faz sentido na França):
1. "Family medicine PA" virou "infirmière en médecine générale" (enfermeira de clínica geral): a profissão "PA" não existe na França.
2. "A horse pill" virou "un comprimé énorme" (um comprimido enorme), a expressão natural em francês.
3. "Made in the US" foi retirado: o usuário não confirmou onde a Cinnarae é fabricada. Se confirmar, o T13 pode ser refeito com o país.
4. "Third-party tested" virou "testé par un laboratoire indépendant" (testado por um laboratório independente), a forma usual em francês.
5. "$1,400" virou "1 400 euros".
6. "Over 40" virou "de plus de 40 ans".

⚠ = alegação de risco (Reg. UE 1924/2006, DGCCRF, política da Meta). Mantidas por decisão do usuário.

Imagens: H1 (mão mostrando 5), B1 (base, mãos relaxadas), B1b (indicador levantado), B1c (mão no peito).

| Take | Imagem | ~s | Fala (FR) |
|------|--------|----|-----------|
| T01 | H1 | 5 | Cinq choses que toute femme devrait savoir avant de commencer le magnésium. |
| T02 | B1c | 8 | Je suis infirmière en médecine générale et maman de deux enfants, et voici mes cinq conseils les plus importants. |
| T03 | B1 | 10 | D'abord, pourquoi c'est plus important que n'importe quel autre complément que vous prenez. Le magnésium est le minéral le plus important pour le corps d'une femme. |
| T04 | B1 | 10 | Il fait tourner plus de quatre cents processus enzymatiques. Votre cœur, vos muscles, vos nerfs, vos hormones, votre énergie : rien ne fonctionne sans lui. |
| T05 | B1b | 9 | Et la plupart des femmes de plus de quarante ans en manquent déjà. Numéro un : prenez-le le soir, tous les soirs sans exception. |
| T06 | B1b | 9 | Pas quand vous y pensez, pas quand vous êtes stressée. Tous les soirs, parce que votre corps l'utilise pendant que vous dormez. |
| T07 | B1c | 8 | Moi, je le prends en gomme, parce que je ne vais pas avaler un comprimé énorme avant de dormir. |
| T08a | B1b | 8 | Numéro deux : pourquoi le prendre. Un meilleur sommeil, moins d'anxiété, moins de crampes, une énergie plus stable. ⚠ |
| T08b | B1 | 5 | Et c'est ce qui fait redescendre votre cortisol en fin de journée. ⚠ |
| T09a | B1b | 7 | Numéro trois : donnez-lui quatre semaines avant de juger. Vos réserves se reconstituent lentement. |
| T09b | B1 | 7 | La plupart des femmes remarquent d'abord le sommeil, vers la deuxième semaine. Le reste vient après. |
| T10 | B1 | 7 | Numéro quatre : la forme, c'est tout. Le bisglycinate de magnésium est la meilleure forme qui existe. ⚠ |
| T11 | B1 | 8 | Il est lié à la glycine, qui le transporte à travers la barrière hémato-encéphalique, là où le cortisol est vraiment régulé. ⚠ |
| T12 | B1 | 7 | Et il est doux pour l'estomac, donc vous ne vous levez pas la nuit pour une mauvaise raison. |
| T13a | B1 | 5 | Et numéro cinq : ne prenez surtout pas le moins cher que vous trouvez. |
| T13b | B1 | 5 | Testé par un laboratoire indépendant et validé par de vrais médecins. |
| T14 | B1 | 8 | Parce qu'une marque qui teste son propre produit, ce n'est pas un test. Je vous mets le lien juste en dessous. |
| T15 | B1c | 8 | Une femme a dépensé mille quatre cents euros dans le mauvais magnésium avant qu'un médecin lui explique enfin tout ça. |
| T16 | B1 | 7 | Et elle a écrit tout ce qu'elle a découvert. Allez le lire avant d'acheter quoi que ce soit. |

Os números estão por extenso na fala para o modelo de voz pronunciar certo; na legenda entram como "400", "40" e "1 400 €" (campo `text` no `montagem.json`).

Total estimado: 138 s de takes brutos (US$ 3,20 em 360p); final esperado ~95–100 s depois do corte de silêncio.

## Notas de produção

- Imagens: P1_v1 (US$ 0,04). B1_v1 gerada com P1 + frame da referência com a mulher coberta (`referencia/sala/sala_mascarada.png`), só para o cenário; o quadro branco veio com "You Got This!" em inglês, então B1_v2 é a edição com o quadro em branco (US$ 0,08 nas duas).
- Takes: imagens H1, B1b e B1c não foram geradas; todos os takes saem da B1_v2 e o gesto vai no prompt do take (personas `nurse_hook`, `nurse_point`, `nurse_chest`, mesma seed e voz).
- 2026-11-19 ~17h40: `gemini-omni-1.2-flash` fora do ar no Google (0% de disponibilidade). Por decisão do usuário, os takes saem em `google/gemini-omni-1.1-flash` (`VIDEO_MODEL=google/gemini-omni-1.1-flash`), ~US$ 0,034/s.
- Teste T01–T03: T02 falhou uma vez (sem custo) e passou na segunda. Gasto US$ 0,78; os três sem corte de fala e com o texto igual ao roteiro.
- O `gemini-omni-1.1-flash` só aceita takes de 3 a 10 s: T08 e T09 (12 s) foram divididos em T08a/T08b e T09a/T09b, sem mudar o texto.
- T10 falhou 4 vezes com a persona da mão no peito (sem custo); passou com a persona base (B1).
- T13 falhou cerca de 15 vezes nos dois modelos, todas sem custo. Foi dividido em T13a/T13b. O T13b passou. O T13a só passou depois que "n'achetez pas le moins cher" virou "ne prenez surtout pas le moins cher" (mesmo sentido: "não pegue de jeito nenhum o mais barato"). O modelo parece bloquear "n'achetez pas".
- Montagem v1: `Vídeos Prontos/Criativo 06 - FR.mp4`, 114,9 s (a referência tem 87 s; o francês falado saiu mais longo). A legenda do valor usa "1400€" para não quebrar "€" numa legenda separada.
- Gasto total: US$ 4,42 (imagens US$ 0,11; takes US$ 4,31, quase todos em `gemini-omni-1.1-flash`).
