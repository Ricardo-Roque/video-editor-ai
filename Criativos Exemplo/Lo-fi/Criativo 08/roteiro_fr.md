# Roteiro FR — Criativo 08 (decupagem por take)

Base: transcrição da referência (`referencia/transcript.txt`), traduzida para o francês falado, mesma ordem, sem cortes nem acréscimos.
Decisão do usuário: copy idêntica à referência, com todas as alegações e sem a menção "Image virtuelle", assumindo o risco.

Adaptações (só o que não existe ou não faz sentido na França):
1. "SP Nutrition" virou "Cinnarae" (produto do usuário); o pacote no balcão é o sachê Cinnarae.
2. "Gummies" virou "gommes" (mesmo termo da embalagem).
3. "3 a.m." virou "3 h du matin".
4. "Link is below if you want to try it" virou "Le lien est juste en dessous si vous voulez essayer" (registro "vous").

⚠ = alegação de risco (Reg. UE 1924/2006, DGCCRF, política da Meta). Mantidas por decisão do usuário.

| Take | Imagem | ~s | Fala (FR) |
|------|--------|----|-----------|
| T01 | B1 | 12 | Avant, je me réveillais toutes les nuits vers 3 h du matin. Le cœur qui s'emballe, la tête qui tourne à cent à l'heure, impossible de me rendormir, peu importe ce que j'essayais. ⚠ |
| T02 | B1 | 10 | Ma sœur est neurologue. Elle m'a dit que mon cortisol grimpait en flèche au milieu de la nuit. Ma réponse au stress était, en gros, complètement détraquée. ⚠ |
| T03 | B1 | 8 | Elle m'a conseillé d'essayer les gommes de bisglycinate de magnésium Cinnarae, deux avant de dormir, tous les soirs. |
| T04 | B1 | 12 | Dès la première semaine, ma tête était plus calme. La deuxième semaine, je dormais toute la nuit. Fini les réveils à 3 h du matin. Ça fait deux mois maintenant. ⚠ |
| T05 | B1 | 10 | Mon anxiété a disparu. Mon énergie tient toute la journée. Je ne m'énerve plus contre mes enfants. Je me réveille et j'ai enfin l'impression de revivre. ⚠ |
| T06 | B1 | 9 | Si une neurologue m'a dit d'en prendre, je ne vais pas arrêter. Le lien est juste en dessous si vous voulez essayer. |

Total estimado: ~61 s de takes brutos; final esperado ~46 s (pausas cortadas na montagem).

## Notas de produção

- Pacote Cinnarae em pé no balcão o vídeo todo. Se o modelo de vídeo deformar o texto do pacote, colar o pacote nítido da B1 por cima na montagem (recorte fixo, custo 0).
- O modelo deformou o texto pequeno do sachê em todos os takes; o sachê nítido da B1 é colado por cima (`tools/colar_produto.py`, overlay `patch` em 676,1096). Posição conferida nos 6 takes.
- Legenda subida para y=1000 (`caption_y`) para não cobrir o sachê; "3h" na legenda (campo `text`).
- Montagem v1: `Vídeos Prontos/Criativo 08 - FR.mp4`, 47,8 s.
