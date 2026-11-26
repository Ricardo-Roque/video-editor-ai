# Roteiro FR — Criativo 02 (decupagem por take)

Base: transcrição da referência (`referencia/transcript.txt`), traduzida para o francês falado, mesma ordem, sem cortes nem acréscimos.
Personagem: senhora francesa de ~70 anos na mesa da cozinha (H3_v2, B3b_v2), sem produto em cena, como na referência. Sem CTA (fiel à referência). Sem a menção "Image virtuelle" (padrão do usuário).

A referência tem duas passagens: hook A ("pas faim le matin") + corpo, depois hook B ("3 h du matin") + o mesmo corpo. É o formato de teste de hooks: o corpo é igual nas duas. Por isso o corpo é gerado **uma vez só** (T02–T04) e reaproveitado na segunda passagem da montagem.

Ordem na montagem: T01 · T02 · T03 · T04 · T05 · T02 · T03 · T04 (≈ 36 s, igual à referência).

Adaptações (só o que muda o sentido literal):
1. "3 a.m." virou "3 h du matin".
2. "Not feeling hungry in the morning" virou "Pas faim le matin ?" (forma natural do francês falado, sem sujeito, como no inglês).
3. "Hair thinning" virou "Les cheveux qui s'affinent" (cabelo que afina, não "queda").
4. "Stubborn belly fat" virou "la graisse du ventre qui ne part pas" ("gordura da barriga que não sai"), a expressão usual em francês.

⚠ = alegação de risco (Reg. UE 1924/2006, DGCCRF, política da Meta). Mantidas, copy fiel.

| Take | Imagem | ~s | Fala (FR) |
|------|--------|----|-----------|
| T01 | H3 | 4 | Pas faim le matin ? C'est peut-être un cortisol trop élevé. ⚠ |
| T02 | B3b | 5 | Des douleurs articulaires ou des inflammations sans raison ? Ça aussi, c'est le cortisol. ⚠ |
| T03 | B3b | 6 | Les cheveux qui s'affinent, la graisse du ventre qui ne part pas, une tension permanente dans le corps. ⚠ |
| T04 | B3b | 7 | La plupart des gens ne savent pas que ce sont tous des signes. Votre hormone du stress est hors de contrôle. ⚠ |
| T05 | B3b | 7 | Vous vous réveillez à 3 h du matin, l'esprit déjà en marche ? C'est peut-être un cortisol trop élevé. ⚠ |

Total estimado: ~29 s de takes brutos; vídeo final ~36 s com o corpo reaproveitado.

## Notas de produção

- Legenda: "3h" no campo `text` do T05.
- T02 e T03 falharam no primeiro envio ("Video generation failed", sem custo) e passaram na segunda tentativa.
- T04: o `gemini-omni-1.2-flash` ficou fora do ar no Google em 2026-11-19, por volta das 17h (0% de disponibilidade em 5 min, 12 falhas sem custo, inclusive um teste neutro). O take foi gerado em `google/gemini-omni-1.1-flash`, com o mesmo prompt e a mesma seed: US$ 0,27, um pouco mais caro.
- Montagem: completa (T01 · T02–T04 · T05 · T02–T04) e duas curtas, `montagem_hookA.json` e `montagem_hookB.json`.
