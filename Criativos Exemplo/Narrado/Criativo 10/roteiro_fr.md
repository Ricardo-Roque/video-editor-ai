# Roteiro FR — Criativo 10 (decupagem por take)

Base: transcrição da referência (`referencia/transcript.txt`). A referência já é em francês, para a França; a fala é mantida palavra por palavra, mesma ordem, sem cortes nem acréscimos.
Oferta confirmada pelo usuário: a Cinnarae tem a mesma oferta "2 achetés = 1 offert".

Adaptações:
1. "Elmora" virou "Cinnarae" (fala e faixa do topo); o sachê em cena é o sachê Cinnarae.
2. Faixa: "On a produit trop d'Elmora 😭" virou "On a produit trop de Cinnarae 😭" ("d'" só antes de vogal).
3. Correção de transcrição: "qu'on n'est jamais faite" virou "qu'on ait jamais faite" (forma falada e correta).

⚠ = risco (Code de la consommation L121-2/L121-4, política da Meta): história de excesso de estoque, "melhor promoção" e prazo precisam ser verdadeiros.

| Take | Imagem | ~s | Fala (FR) |
|------|--------|----|-----------|
| T01 | H1 | 6 | Je dois m'excuser publiquement auprès de tous ceux qui ont acheté Cinnarae avant, parce que j'ai menti. ⚠ |
| T02 | B1 | 6 | Je vous ai dit que vous n'auriez jamais un meilleur prix, et puis on a trop produit. ⚠ |
| T03a | B2 | 6 | Alors c'est la dernière chance de profiter de la meilleure promo qu'on ait jamais faite. ⚠ |
| T03b | B2b | 8 | Allez en profiter à fond, tout de suite, parce qu'une fois que ce surstock est parti, c'est fini. ⚠ |
| T04 | B3 | 6 | Je ne referai pas ça avant longtemps. Les liens sont en dessous. |

Total: 36 s de takes brutos no Veo 3.1 Lite (clipes de 4/6/8 s); final esperado ~21 s (pausas cortadas na montagem).

## Notas de produção

- Modelo trocado (pedido do usuário): Omni 1.2 Flash 360p deformava o texto pequeno do rótulo; os takes são gerados com **Veo 3.1 Lite 720p** (`takes_config_veo.json`, US$ 0,05/s), que só aceita 4, 6 ou 8 s. Por isso T03 foi dividido em a/b numa pausa natural; a fala não muda. T01 aprovado no teste: `T01_veo720_v1`. O T01 em Omni (`T01_360p_v1`) foi descartado.
- T03b parte do último frame de T03a (`imagens/cenas/B2_fimT03a.png`); o T03a termina com o sachê de volta na caixa, então o T03b mostra a mão tirando o sachê de novo (lê como outro sachê sendo mostrado).
- T03b corrigido a pedido do usuário: no take do Veo o sachê "flutuava" ao sair da caixa (e o logo virava "Cinnarac"). Usa só a voz do take sobre a B2 nítida com zoom lento: `takes/T03b_zoom_v1.mp4` (custo 0). Continua direto do T03a, que também parte da B2.
- T02 (corredor): depois de ~4 s o fundo vira um atacado; a fala acaba em 3,4 s, o corte do silêncio remove o trecho.

- Voz em off feminina, tom de confissão, mesma seed nos 4 takes. Nenhuma pessoa em cena, só a mão.
- Overlays: faixas do topo + círculo vermelho "2 ACHETÉS = 1 OFFERT", PNG local, overlay `patch` no vídeo todo.
- Rótulo: se deformar com a mão em movimento, `prancheta_zoom.py` com a voz do take.
