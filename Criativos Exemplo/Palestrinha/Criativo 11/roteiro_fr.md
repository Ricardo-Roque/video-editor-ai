# Roteiro FR — Criativo 11 (copy do 03, formato palestrinha)

Base: a fala do [Criativo 03](../../Narrado/Criativo%2003/roteiro_fr.md), aprovada em 2026-11-18. **Nenhuma palavra muda.** Só muda o visual. Uma apresentadora francesa de 50+ fala para a câmera na frente de um quadro branco. A prova social (T07) vira clipes curtos de UGC.

Adaptações em relação ao 03:
1. A narradora em off virou apresentadora na tela, com sincronia labial. A fala continua no feminino ("reposée"), que combina com ela.
2. A prancheta virou um quadro branco escrito à mão com canetão, com poucas palavras. Ele tem dois estados: o Q-A (os problemas) e o Q-B (Q-A mais a rotina e o resultado).
3. As fotos paradas F1–F4 viraram 4 clipes UGC (U1–U4), mulheres de 50+ filmando a si mesmas com o pacote, sem som. A voz da apresentadora segue por cima.

⚠ = alegação de risco (Reg. UE 1924/2006, DGCCRF, política da Meta). Mantidas por decisão do usuário. Agora quem diz é uma pessoa na tela.

| Take | Imagem | ~s | Fala (FR) |
|------|--------|----|-----------|
| T01 | C1 | 11 | Si votre glycémie vous fait pisser 3 fois par nuit, prenez du bisglycinate de magnésium pour aider l'insuline à sortir le sucre du sang, et vous dormirez enfin d'une traite. ⚠ |
| T02 | C2 | 12 | Si vous vous réveillez la bouche sèche comme le désert tous les matins, prenez du bisglycinate de magnésium pour stabiliser votre glycémie, et votre corps arrêtera d'évacuer l'eau pendant votre sommeil. ⚠ |
| T03 | C3 | 11 | Si vous n'arrivez pas à dormir d'une traite, quoi que vous essayiez, prenez du bisglycinate de magnésium pour calmer le système nerveux, et votre corps pourra enfin se reposer. ⚠ |
| T04 | C4 | 7 | Et moi, j'utilise les gommes au bisglycinate de magnésium de Cinnarae. Elles sont sans sucre et douces pour l'estomac. |
| T05 | C5 | 10 | Prenez-en deux avant de vous coucher pour une bonne nuit de sommeil. Maintenant, je dors d'une traite. Fini les allers-retours aux toilettes. Fini la bouche sèche. ⚠ |
| T06 | C6 | 5 | Je me réveille vraiment reposée, avec de l'énergie pour toute ma journée. ⚠ |
| T07 | C7 | 9 | Plus de 120 000 femmes en prennent déjà tous les soirs dans leur routine du coucher, et elles partent toujours très vite. ⚠ |
| T08 | C7 | 10 | Si vous ne sentez pas la différence en 30 jours, on vous rembourse. Cliquez sur le lien en dessous pour avoir 20 % de réduction sur votre première commande. |

Clipes UGC, sem fala (3 s cada, `--no-audio`), que entram por cima do T07:

| Clipe | Imagem | Entra em (proposta) |
|-------|--------|---------------------|
| U1 | U1 | "femmes en prennent déjà" |
| U2 | U2 | "tous les soirs dans leur routine du coucher" |
| U3 | U3 | "et elles partent" |
| U4 | U4 | "toujours très vite" |

O T07 começa com a apresentadora ("Plus de 120 000") e volta para ela no T08.

## Texto do quadro (escrito à mão, francês)

**Q-A** (T01–T04), no terço de cima:
- Título (vermelho, sublinhado): **Bisglycinate de magnésium**
- 🚽 Pisser 3x / nuit → sucre ↓ · insuline ✓
- 🌵 Bouche sèche → glycémie stable
- 🌙 Nuits coupées → nerfs calmes

**Q-B** (T05–T08): o Q-A mais duas linhas em verde, logo abaixo:
- 🐻🐻 2 gommes au coucher
- ✓ nuit complète · ✓ énergie

## Notas de produção

- A apresentadora usa a mesma persona e a mesma seed em todos os takes. Agora há sincronia labial a conferir.
- "120 000" deve ser falado "cent vingt mille". Na legenda, `120\h000`, como no 03.
- Imagens aprovadas em 2026-11-20: P1, C1–C7 e U1–U4 (US$ 0,50). A C3 é a primeira cena gerada, que saiu apontando a linha 3. A C5 está na v2, com ela no canto direito para não tapar as linhas novas.
- Teste T01 v1 (C1, mãos no peito): aprovado na voz e no rosto, US$ 0,28. O usuário pediu que **ela aponte para o quadro sempre que falar do que está escrito**, como na referência. Novas imagens de partida: C1_v2 (linha 1), C2_v3 (linha 2; na v2 o canetão tinha ficado na linha 3) e C6_v2 ("✓ énergie"), US$ 0,15. As personas `point1/2/3/5/6` do `takes_config.json` descrevem o gesto.
- T01 v2 (US$ 0,28): depois de "traite." (8,44 s), o modelo inventou "Mes saucères du synate.". O take foi cortado em 8,7 s, numa pausa real, e o arquivo da montagem é `T01a_360p_v2.mp4`.
- O gesto de apontar do T01 v2 foi aprovado. O lote T02–T08 foi gerado em 360p por US$ 1,53, todos sem corte de fala. As diferenças de texto são só de grafia da transcrição (bisglicinate, essayez, Sinaré, reposé, en-dessous).
- UGC U1–U4: o Omni 1.2 não aceita `--no-audio` (HTTP 400, sem custo). Foram gerados com áudio, que é descartado na montagem: 4 × US$ 0,07 = US$ 0,28.
- Quadro com erros no take (em 360p o modelo escreveu "glycémie sinble", "nerfs colmes" e "Muits"). Corrigido localmente com o novo `tools/quadro_nitido.py`, que cola o texto nítido da imagem quadro a quadro e mantém do take a mão, o canetão e o cabelo, a partir da cor de pele. Saída em 1080x1920: `T0x_quadro_v1.mp4`.
  - T01–T03 usam `_quadro_v2`, feitos a partir da C1_v1, que tem o quadro limpo, sem mão sobre o texto. A C2_v3 tinha a mão sobre "Nuits", e esse trecho ficava com o "Muits" do take.
  - Regiões (em pixels do take 360x640): de 4,55 a 356,228 nos takes de T01 a T04; até 305 em T05 e T06; até 290 em T07 e T08 (o pacote).
- T07: `T07_montagem_v1.mp4` foi montado localmente com o áudio do T07 e estes trechos de imagem:
  - 0–2,36 s: apresentadora ("Plus de 120 000")
  - U1: "femmes en prennent déjà"
  - U2: "tous les soirs… coucher"
  - U3: "et elles partent"
  - U4: "toujours très vite"
- Texto do quadro: o take pode deformar as letras. Na montagem, a faixa de cima da própria imagem da cena (nítida) entra por cima do take inteiro (`"mode": "patch"`). A câmera é fixa, então a faixa encaixa.
