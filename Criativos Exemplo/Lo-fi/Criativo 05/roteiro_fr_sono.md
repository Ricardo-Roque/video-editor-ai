# Roteiro FR — Criativo 05, versão Sono (decupagem por take)

Base: versão original do Criativo 05 (`roteiro_fr.md`), mesmo formato "falsa reclamação" e mesma oferta.
Pedido do usuário: tirar tudo de emagrecimento e trocar a promessa por sono, aproveitando o máximo de takes já gerados.

Mudanças em relação à versão original:
1. Saiu "j'ai perdu presque 9 kilos" (T02 cortado em "dernier") e entrou o take novo T20 (dormir a noite inteira).
2. Saiu "J'ai le visage moins gonflé le matin" (T03 usado só a partir de "ça fait des semaines").
3. Saiu "et qui m'a fait perdre mon ventre" (T08 cortado em "matin") e entrou o take novo T21 (adormecer rápido e acordar descansada).
4. Saiu "et de stocker du gras sur mon ventre. Pas de régime de fou" (T11 cortado em "matin") e entrou o take novo T22 (sem sonífero, sem chá milagroso, sem rotina complicada).
5. Saíram os overlays O1 (barriga de jeans) e O2a/O2b (rosto antes/depois).

⚠ = alegação de risco (Reg. UE 1924/2006, DGCCRF, política da Meta). Sono e cortisol não estão entre as alegações autorizadas para magnésio na UE.

| Take | Imagem | ~s | Fala (FR) |
|------|--------|----|-----------|
| T01 | B1a | 9 | Putain, j'en ai marre des gummies au magnésium de Cinnarae. Les filles, n'achetez surtout pas les gummies au magnésium de Cinnarae avant d'avoir vu ça. |
| T02 | B1 | 3 | Bon, j'ai commencé à en prendre le mois dernier. |
| T20 | B1 | 4 | Et franchement ? Je dors enfin d'une traite, toute la nuit. ⚠ |
| T03 | B1 | 4 | Et ça fait des semaines que je ne me suis pas réveillée à 3 h du matin. ⚠ |
| T04 | B1 | 3 | Donc non, mes résultats, c'est pas le problème. |
| T05 | B1b | 6 | Le problème, c'est que je viens de voir qu'ils font moins 20 %, et la livraison gratuite en plus. |
| T06 | B1a | 5 | Moi, j'ai payé plein pot le mois dernier. Non mais vous vous foutez de moi, Cinnarae ? |
| T07 | B1 | 5 | Mais franchement, je suis quand même contente de l'avoir pris, même plein pot. |
| T08 | B1 | 4 | C'est le premier truc qui a vraiment arrêté mes réveils à 3 h du matin. ⚠ |
| T21 | B1 | 5 | Je m'endors vite, et le matin je me lève reposée, plus du tout crevée. ⚠ |
| T09 | B1c | 4 | Tout ce que je fais, c'est prendre deux petits gummies tous les soirs. |
| T10 | B1c | 6 | Le bisglycinate de magnésium fait redescendre mon cortisol, mon hormone du stress, pendant la nuit. ⚠ |
| T11 | B1c | 3 | Du coup, il arrête de me réveiller à 3 h du matin. ⚠ |
| T22 | B1c | 4 | Pas de somnifères, pas de tisane miracle, pas de routine compliquée. ⚠ |
| T12 | B1a | 4 | Alors ouais, je suis un peu vénère d'avoir payé plein pot. |
| T13 | B1b | 10 | Mais si vous l'avez pas encore essayé, faites pas la même erreur que moi. Ils le fabriquent en petites séries, donc il part très vite. Profitez de l'offre tant que vous pouvez. |

Origem de cada take:
- T01: reaproveitado inteiro
- T02: reaproveitado, 0–2,6 s
- T20: **novo**
- T03: reaproveitado, a partir de 4,4 s
- T04: reaproveitado inteiro
- T05: reaproveitado inteiro
- T06: reaproveitado (sem o "Hein ?")
- T07: reaproveitado inteiro
- T08: reaproveitado, 0–4,1 s
- T21: **novo**
- T09: reaproveitado inteiro
- T10: reaproveitado inteiro
- T11: reaproveitado, 0,4–3,0 s
- T22: **novo**
- T12: reaproveitado inteiro
- T13: reaproveitado (T13a + T13b)

Takes novos: T20 (4 s), T21 (5 s), T22 (4 s) = 13 s a 360p, mesma imagem e seed 707 da versão original.
Final esperado: ~60 s.

## Overlays na montagem (custo 0)

- Nenhum obrigatório. Opcional: B-roll da mulher dormindo tranquila (O3, tela cheia) sobre "Je dors enfin d'une traite" (T20), no lugar da prova visual que a barriga de jeans fazia.

## Notas de produção

- Reaproveitados com corte: o trecho usado será recortado do take original para um arquivo novo (ex.: `T03b_360p_v1.mp4`), como já foi feito no T13. Nenhum take original é sobrescrito.
- Saída prevista: `Vídeos Prontos/Criativo 05 - FR Sono.mp4`, com `takes_config_sono.json` e `montagem_sono.json` separados dos da versão original.
- 2026-11-19: Omni 1.2 Flash fora do ar no OpenRouter ("Video generation failed" em toda tentativa, sem cobrança). Por decisão do usuário, T20–T22 gerados no Veo 3.1 Lite 720p (`takes_config_sono_veo.json`, arquivos `_veo720_v1`): US$ 0,70.
- Cortes dos takes antigos: T02a = T02 0–2,64 s; T03b = T03 a partir de 4,25 s (começa com "Et ça fait..."); T08a = T08 0–4,2 s; T11a = T11 0–3,2 s.
- T20: o Veo falou "Et franchement, quoi, ..." (legenda ajustada no `montagem_sono.json`). T22: "tisane miracle" sai um pouco embolado (o Whisper medium ouve "teaser de miracle", o small ouve "Tisane Miracle"); mantido para aprovação do usuário. T21: "reposé/crevé" é homófono, ok.
- Montagem v1: 71,0 s, 1080x1920, `Vídeos Prontos/Criativo 05 - FR Sono.mp4`, sem overlays.
