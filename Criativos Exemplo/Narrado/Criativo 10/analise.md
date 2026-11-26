# Análise — Criativo 10

Fonte: `Vídeo Bruto/Criativo #09.mp4`
Formato: 9:16, 360x640, 30 fps, 21,6 s. Idioma: **francês** (a referência já é para a França).
Transcrição completa com timestamps: `referencia/transcript.txt`.
Produto da referência: **Elmora** (concorrente), bisglycinate de magnésium en gummies, saveur framboise.
Produto do novo criativo: **Cinnarae** (gommes de bisglycinate de magnésium, arôme framboise). Embalagem: `Referências/Sachê de Gomas de Magnésio Premium.png`. País: França. Idioma: francês.

## Formato geral

Anúncio de "excesso de estoque", falado pela marca. Sem rosto: câmera POV (celular na mão) num armazém grande (estantes altas, paletes, caixas abertas cheias de sachês, bancada de embalagem com impressora de etiquetas). Uma mão segura e tira sachês das caixas. Voz em off feminina (~260 Hz), tom de confissão/desculpa.
Overlays fixos o vídeo todo, no topo: **"On a produit trop d'Elmora 😭"** (fundo branco) + **"AIDEZ-NOUS À VIDER NOTRE ENTREPÔT"** (fundo escuro, texto branco) e, à esquerda, um círculo vermelho **"2 ACHETÉS = 1 OFFERT"**.

## Estrutura

| # | Tempo | Bloco | Cenário / enquadramento | Fala (francês) | Tradução |
|---|-------|-------|-------------------------|----------------|----------|
| 1 | 0,0–4,95 | HOOK — confissão | POV: mão segura o sachê em close, acima de uma caixa aberta cheia de sachês. | "Je dois m'excuser publiquement auprès de tous ceux qui ont acheté Elmora avant, parce que j'ai menti." | "Preciso pedir desculpas publicamente a todos que compraram Elmora antes, porque eu menti." |
| 2 | 4,95–8,8 | BODY — motivo | POV andando pelo corredor do armazém, sachê na mão, paletes de sachês ao fundo. | "Je vous ai dit que vous n'auriez jamais un meilleur prix, et puis on a trop produit." | "Eu disse que vocês nunca teriam um preço melhor, e aí produzimos demais." |
| 3 | 8,8–18,0 | BODY — oferta | Bancada de embalagem: caixa aberta cheia de sachês, a mão tira um sachê e mostra. | "Alors c'est la dernière chance de profiter de la meilleure promo qu'on ait jamais faite. Allez en profiter à fond, tout de suite, parce qu'une fois que ce surstock est parti, c'est fini." | "Então é a última chance de aproveitar a melhor promoção que já fizemos. Aproveitem ao máximo, agora mesmo, porque quando esse excesso de estoque acabar, acabou." |
| 4 | 18,0–21,6 | CTA | Mão segura o sachê na frente de paletes empilhados. | "Je ne referai pas ça avant longtemps. Les liens sont en dessous." | "Não vou fazer isso de novo tão cedo. Os links estão aqui embaixo." |

Cortes detectados: 4,95 s, 8,78 s e 17,98 s (4 planos; outros cortes leves são movimento de câmera).

## Estilo de edição

- Legenda: branca com contorno preto, 2–3 palavras, ~80% da altura. Usaremos o padrão do `montar.py`.
- Overlays: faixas do topo + círculo vermelho. Faço como PNG local (sem custo) e colo no vídeo todo com `"mode": "patch"`.
- Produto aparece? **Sim, o tempo todo**, em close e em caixas/paletes ao fundo.
- Áudio: só voz, sem música.

## Imagens necessárias

Sem personagens (só mão). Quatro cenas, todas com o sachê Cinnarae como `--ref`:
1. **H1 — Sachê sobre caixa aberta**: POV, mão segurando o sachê Cinnarae em close, acima de uma caixa de papelão aberta cheia de sachês Cinnarae; armazém ao fundo.
2. **B1 — Corredor do armazém**: POV, mão segurando o sachê no meio de um corredor com estantes altas e paletes de sachês.
3. **B2 — Bancada de embalagem**: caixa aberta cheia de sachês, mão tirando um sachê; impressora de etiquetas e fita ao lado.
4. **B3 — Paletes**: mão segurando o sachê na frente de paletes empilhados com caixas.
5. **O1 — Faixas do topo + círculo**: PNG local, sem custo.

Total: 4 imagens × US$ 0,04 ≈ **US$ 0,16** (com refações, ~US$ 0,30).

## Takes estimados

- A copy já é francesa: ~21 s de fala, 4 takes (um por plano: 5, 4, 9 e 3,5 s), voz em off feminina com seed fixa.
- Custo estimado (360p, ~US$ 0,023/s): ~21 s ≈ **US$ 0,49**; com correções, **~US$ 0,70**.
- **Risco do rótulo**: igual ao Criativo 09. Onde o modelo deformar o rótulo, uso a imagem nítida com zoom lento (`tools/prancheta_zoom.py`) e só a voz do take, sem custo extra. Sachês pequenos ao fundo podem ficar borrados (a referência também é borrada em 360p).

Custo total estimado: **~US$ 0,65 a 1,00**.

## Adaptações

- "Elmora" → "Cinnarae" (fala e faixa: "On a produit trop de Cinnarae 😭"; "d'Elmora" vira "de Cinnarae" por causa da consoante).
- Cenário igual (armazém); embalagem trocada pela nossa.

## Alertas de política (decisão sua)

- **História de estoque e preço**: "j'ai menti", "on a trop produit", "surstock", "meilleure promo qu'on ait jamais faite", "je ne referai pas ça avant longtemps", "2 achetés = 1 offert". Se não for verdade, é prática comercial enganosa na França (Code de la consommation, art. L121-2 e L121-4). **Preciso saber qual é a oferta real da Cinnarae** (2 comprados = 1 grátis?). Se for outra, troco o círculo e a fala.
- Sem alegação de saúde na fala. Sem pessoa gerada por IA (só a mão), então não precisa de "Image virtuelle".
