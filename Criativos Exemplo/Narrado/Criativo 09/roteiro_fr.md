# Roteiro FR — Criativo 09 (decupagem por take)

Base: transcrição da referência (`referencia/transcript.txt`). A referência já é em francês, para a França; a fala é mantida palavra por palavra, mesma ordem, sem cortes nem acréscimos.
Oferta confirmada pelo usuário: a Cinnarae tem a mesma oferta "2 achetés = 1 offert".

Adaptações:
1. "Elmora" virou "Cinnarae" (produto do usuário); o sachê em cena é o sachê Cinnarae.
2. Correção de transcrição: o Whisper escreveu "qu'on n'est jamais fait"; a forma falada e correta é "qu'on ait jamais fait".
3. Faixa do topo igual à referência: "2 ACHETÉS = 1 OFFERT 🚨 / DANS LA LIMITE DES STOCKS".

⚠ = risco (Code de la consommation L121-2/L121-4, política da Meta): prazo de oferta e "menor preço" precisam ser verdadeiros.

| Take | Imagem | ~s | Fala (FR) |
|------|--------|----|-----------|
| T01 | H1 | 7 | C'est votre dernier avertissement pour prendre le bisglycinate de magnésium Cinnarae au prix le plus bas qu'on ait jamais fait. ⚠ |
| T02a | B1 | 4 | Une promo comme ça, ça n'arrive pas souvent. |
| T02b | B1b | 8 | Si vous ne faites pas vite, ça va partir avant même que vous vous en rendiez compte. |
| T03a | B2 | 8 | Il ne reste plus que quelques heures et vous allez regretter de ne pas en avoir profité. ⚠ |
| T03b | B2b | 6 | Cliquez sur le lien juste en dessous et prenez-le tout de suite. |

Total: 34 s de takes brutos no Veo 3.1 Lite (clipes de 4/6/8 s); final esperado ~20 s (pausas cortadas na montagem).

## Notas de produção

- Modelo trocado (pedido do usuário): Omni 1.2 Flash 360p deformava o texto pequeno do rótulo; os takes são gerados com **Veo 3.1 Lite 720p** (`takes_config_veo.json`, US$ 0,05/s), que só aceita 4, 6 ou 8 s. Por isso T02 e T03 foram divididos em a/b numa pausa natural; a fala não muda. O T01 em Omni (`T01_360p_v1`) foi descartado.
- "She says" no prompt fazia o Veo pôr uma mulher na cena; `lote_takes.py` agora aceita `"say"` no config ("The unseen off-screen narrator says:").
- B1 (sachê na caixa): mesmo assim o Veo pôs uma apresentadora atrás da caixa em 2 tentativas. T02a e T02b usam só a voz desses takes sobre a B1_v2 nítida com zoom lento (`tools/prancheta_zoom.py`): `takes/T02a_zoom_v1.mp4`, `takes/T02b_zoom_v1.mp4`.
- T01 (Veo): o sachê cai/borra depois de 7,2 s; a fala acaba em 7,0 s, o corte do silêncio remove o trecho.
- T03b parte do último frame de T03a (`imagens/cenas/B2_fimT03a.png`).

- Voz em off feminina, rápida e enfática, mesma seed nos 3 takes. Nenhuma pessoa em cena, só a mão.
- Faixa do topo: PNG local, overlay `patch` no vídeo todo. Legenda sem cobrir o rótulo do sachê (ajustar `caption_y` se preciso).
- Rótulo: B1 parado, colar sachê nítido (`colar_produto.py`). H1/B2: se o rótulo deformar, `prancheta_zoom.py` com a voz do take.
