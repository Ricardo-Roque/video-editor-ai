# Análise — Criativo 11

Fonte: `Vídeo Bruto/Criativo #08.mp4`
Formato: 9:16, 360x640, 30 fps, 20,0 s. Idioma: **francês** (a referência já é para a França).
Transcrição completa com timestamps: `referencia/transcript.txt`.
Produto da referência: **Elmora** (concorrente), bisglycinate de magnésium en gummies, saveur framboise. Mesmo tipo de produto e quase o mesmo layout de embalagem que o nosso.
Produto do novo criativo: **Cinnarae** (gommes de bisglycinate de magnésium, arôme framboise). Embalagem: `Referências/Sachê de Gomas de Magnésio Premium.png`. País: França. Idioma: francês.

## Formato geral

Anúncio de promoção/urgência, sem rosto. Câmera POV (celular na mão) num armazém/centro de distribuição: estantes metálicas laranja com caixas de papelão. Uma mão feminina (unhas verde-oliva escuras) segura o sachê de frente para a câmera. Voz em off feminina (tom médio, ~250 Hz), rápida e enfática, estilo "última chance".
Faixa fixa no topo durante o vídeo todo: **"2 ACHETÉS = 1 OFFERT 🚨"** (fundo vermelho, texto branco) + **"DANS LA LIMITE DES STOCKS"** (fundo branco, texto preto).

## Estrutura

| # | Tempo | Bloco | Cenário / enquadramento | Fala (francês) | Tradução |
|---|-------|-------|-------------------------|----------------|----------|
| 1 | 0,0–6,6 | HOOK — urgência | POV: mão segura o sachê na frente da estante; gira o sachê de leve. | "C'est votre dernier avertissement pour prendre le bisglycinate de magnésium Elmora au prix le plus bas qu'on ait jamais fait." | "É o seu último aviso para pegar o bisglicinato de magnésio Elmora pelo menor preço que já fizemos." |
| 2 | 6,6–12,4 | BODY — escassez | Sachê em pé sobre uma caixa de papelão, gomas vermelhas espalhadas na frente; estantes ao fundo. Câmera parada/leve movimento. | "Une promo comme ça, ça n'arrive pas souvent. Si vous ne faites pas vite, ça va partir avant même que vous vous en rendiez compte." | "Uma promoção assim não acontece sempre. Se vocês não forem rápidos, vai acabar antes mesmo de perceberem." |
| 3 | 12,4–20,0 | BODY + CTA | POV: mão segura o sachê, um dedo aponta para o rótulo; estantes ao fundo. | "Il ne reste plus que quelques heures et vous allez regretter de ne pas en avoir profité. Cliquez sur le lien juste en dessous et prenez-le tout de suite." | "Só restam algumas horas e vocês vão se arrepender de não ter aproveitado. Cliquem no link logo abaixo e peguem agora mesmo." |

Cortes detectados: 6,65 s e 12,45 s (3 planos).

## Estilo de edição

- Legenda: branca com contorno preto, 2–3 palavras, ~78% da altura. Usaremos o padrão do `montar.py` (1–3 palavras, palavra-chave em amarelo-limão), já validado.
- Overlay: faixa fixa no topo (ver acima). Faço como PNG local (sem custo) e colo no vídeo todo com `"mode": "patch"`.
- Produto aparece? **Sim, o tempo todo, em close.** É o protagonista do vídeo.
- Áudio: só voz, sem música.

## Imagens necessárias

Sem personagens (só mão). Três cenas, todas com o sachê Cinnarae como `--ref`:
1. **H1 — Mão + sachê na estante**: POV, mão feminina (unhas escuras) segurando o sachê Cinnarae de frente, estante de armazém com caixas ao fundo.
2. **B1 — Sachê na caixa com gomas**: sachê Cinnarae em pé em cima de uma caixa de papelão, gomas vermelhas de framboesa espalhadas na frente, armazém ao fundo.
3. **B2 — Dedo apontando o rótulo**: mesma mão de H1 (H1 como `--ref`), segurando o sachê com o indicador da outra mão apontando para o rótulo.
4. **O1 — Faixa do topo**: PNG local, sem custo.

Total: 3 imagens × US$ 0,04 ≈ **US$ 0,12** (com refações para acertar a embalagem, ~US$ 0,25).

## Takes estimados

- A copy já é francesa: ~19,5 s de fala, 3 takes (um por plano, de 6 a 7,5 s), voz em off feminina com seed fixa.
- Custo estimado (360p, ~US$ 0,023/s): ~20 s ≈ **US$ 0,46**; com correções, **~US$ 0,65**.
- **Risco do rótulo**: o sachê fica em close o vídeo todo, e o modelo de vídeo redesenha letras em 360p. Plano:
  - B1 (sachê parado): colar o sachê nítido por cima com `tools/colar_produto.py` (como no Criativo 10).
  - H1/B2 (mão mexendo o sachê): conferir os frames. Se o rótulo deformar, uso a imagem nítida com zoom lento (`tools/prancheta_zoom.py`) e só a voz do take, sem custo extra.

Custo total estimado: **~US$ 0,60 a 0,90**.

## Adaptações

- "Elmora" → "Cinnarae"; "le bisglycinate de magnésium Elmora" → "les gommes de bisglycinate de magnésium Cinnarae" (igual à embalagem; no roteiro detalho).
- "prenez-le" → "prenez-les" (gommes, plural).
- Cenário igual (armazém); embalagem trocada pela nossa.

## Alertas de política (decisão sua)

- **Urgência e preço**: "dernier avertissement", "il ne reste plus que quelques heures", "prix le plus bas qu'on ait jamais fait" e "2 achetés = 1 offert". Na França, prazo falso de oferta é prática comercial enganosa proibida em qualquer caso (Code de la consommation, art. L121-4), e "menor preço já feito" precisa ser verdade. **Preciso saber se a Cinnarae tem essa oferta (2 comprados = 1 grátis) e se é por tempo limitado.** Se a oferta for outra, troco a faixa e a fala.
- Sem alegação de saúde na fala (só o que está impresso na embalagem). Sem pessoa gerada por IA (só a mão), então não precisa de "Image virtuelle".
