# Prompts de imagem — Criativo 13 (palestrinha, França)

Modelo: `google/gemini-nano-banana-2.1` (~US$ 0,04 por imagem). Formato 9:16.
Pacote: sempre anexar `Referências/Sachê de Gomas de Magnésio Premium.png` quando ele aparecer. As gomas são **ursinhos vermelhos** (gummy bears).

Adaptações para a França: interiores parisienses (piso de tábua, janelas altas com venezianas, varanda de ferro trabalhado). Nada americano.

Regra de enquadramento das cenas C (para a montagem colar a faixa nítida do quadro): **todo o texto do quadro fica nos 40% de cima da imagem**, acima da cabeça da apresentadora. A apresentadora aparece da cintura para cima, com o topo da cabeça a ~42% da altura. A câmera fica fixa e o enquadramento é idêntico em todas as cenas C.

Ordem: P1 → C1 → C2/C3 (editadas da C1) → C4 → C5 (Q-B) → C6/C7 → U1–U4.

---

## P1 — Apresentadora (50+)

Salvar como `imagens/personagens/P1_v1.png`.

```
Candid real photo taken with an iPhone, 9:16, not a studio or stock photo. An ordinary French woman aged about 55, real everyday person (not a model), slim-average build, shoulder-length chestnut-brown hair with visible natural grey strands, slightly imperfect, tucked behind one ear, very light makeup, small gold stud earrings, hazel eyes, real wrinkles and smile lines, slight skin texture and pores, a few sun spots. She wears a plain white crew-neck cotton T-shirt, slightly creased. Plain light-grey wall behind her, ordinary indoor light from a window, head and shoulders, looking at the camera with a friendly natural half smile. Natural phone-camera sharpness and slight noise, no retouching, no beauty filter, no text.
```

## C3 — Quadro Q-A, apontando a linha 3 (T03) — base de todas as cenas

Gerada com este prompt pedindo a linha 1, mas ela saiu apontando a linha 3. Aprovada pelo usuário em 2026-11-20 ("ficou perfeito") e renomeada para `C3_v1.png`. As outras cenas C são editadas a partir dela.
Referências: **P1 aprovada** + `referencia_formato/frame_076.57s.jpg` (frame da referência, só como base de enquadramento, luz e realismo).

```
Real, unedited frame from a smartphone video on a tripod, 9:16, eye level, fixed camera, exactly the same realistic home-video look, camera angle, distance, framing, lighting, whiteboard and dark slatted wall as the second attached image. Use the second image ONLY for that: do not copy the man, his clothes or any of its Japanese writing. The woman from the first attached photo (same face, hair and white crew-neck T-shirt, dark trousers) stands centred in front of a large white magnetic whiteboard with a thin aluminium frame, mounted against a wall of dark charcoal vertical wooden slats. The whiteboard fills the whole background. She is framed from the waist up; the top of her head sits at about 42% of the image height, so the whole upper part of the whiteboard above her head is clearly visible. She holds a red and a green dry-erase marker in her left hand, and with her right arm raised she points the cap of a marker at the edge of the first line of writing, looking at the camera mid-sentence, friendly teacher energy. Soft even indoor light.
Handwritten dry-erase marker writing on the whiteboard, large, neat and clearly legible, ALL of it in the top 40% of the image, above her head:
- Top title in red marker, underlined twice: "Bisglycinate de magnésium"
- Line 1 in blue marker: a small simple drawing of a toilet, then "Pisser 3x / nuit", then a green arrow "→" and in green "sucre ↓ insuline ✓"
- Line 2 in blue marker: a small drawing of a cactus, then "Bouche sèche", then a green arrow "→" and in green "glycémie stable"
- Line 3 in blue marker: a small drawing of a crescent moon, then "Nuits coupées", then a green arrow "→" and in green "nerfs calmes"
The rest of the whiteboard below the writing is blank white. All text in French, spelled exactly as written above with correct accents (é, è). No other text, no subtitles, no logo.
```

## C1 — Q-A, falando para a câmera (T01, hook)

Referências: **C3 aprovada**. Salvar como `imagens/cenas/C1_v1.png`.

```
Use the attached image as the base. Keep everything exactly identical: the whiteboard and every handwritten word and drawing on it, the wall, the framing, the camera position, the lighting, the woman's face, hair and clothes. Change only her pose: both arms are now down at chest height, the red and green markers held loosely in her right hand, her left hand slightly open in a natural explaining gesture, facing the camera directly and speaking with a serious, engaged expression, like a teacher starting a lesson. Nothing covers the writing. Do not change, move or redraw any text.
```

## C2 — Q-A, mostrando o quadro com a mão aberta (T02)

Referências: **C3 aprovada**. Salvar como `imagens/cenas/C2_v1.png`.

```
Use the attached image as the base. Keep everything exactly identical: the whiteboard and every handwritten word and drawing on it, the wall, the framing, the camera position, the lighting, the woman's face, hair and clothes. Change only her pose: she has turned her body slightly to her left, her left arm extended sideways at shoulder height with the open palm presenting the writing above her (below the text, not covering it), the markers in her right hand at her waist, her face turned back toward the camera, speaking. Do not change, move or redraw any text.
```

## C1p — Q-A, apontando a linha 1 (T01, v2)

O usuário pediu que ela aponte para o quadro sempre que falar de algo escrito nele, como na referência. Esta imagem substitui a C1 no T01.
Referências: **C3 aprovada**. Salvar como `imagens/cenas/C1_v2.png`.

```
Use the attached image as the base. Keep everything exactly identical: the whiteboard and every handwritten word and drawing on it, the wall, the framing, the camera position, the lighting, the woman's face, hair and clothes. Change only her right arm: she raises it higher and points the cap of the green marker at the first line of writing, right next to the words "Pisser 3x/nuit", like a teacher pointing at the board, while she keeps looking at the camera and speaking. Her hand may overlap the board slightly but must not hide the words of that line. Do not change, move or redraw any text.
```

## C2p — Q-A, apontando a linha 2 (T02, v2)

Referências: **C3 aprovada**. Salvar como `imagens/cenas/C2_v3.png`.
Na v2 o canetão ficou na linha 3. Na v3 a referência é a C1_v2, que aponta a linha 1, para ela baixar o braço uma linha só.

```
Use the attached image as the base. Keep everything exactly identical: the whiteboard and every handwritten word and drawing on it, the wall, the framing, the camera position, the lighting, the woman's face, hair and clothes. Change only her raised right arm: lower it slightly so that the cap of the green marker now touches the board immediately to the left of the cactus drawing, at exactly the same height as the words "Bouche sèche" (the second line), not the first and not the third line. Her hand stays to the left of the words so "Bouche sèche" is fully readable. She keeps looking at the camera and speaking. Do not change, move or redraw any text.
```

## C6p — Q-B, apontando "✓ énergie" (T06, v2)

Referências: **C5 aprovada (v2)**. Salvar como `imagens/cenas/C6_v2.png`.

```
Use the attached image as the base. Keep everything exactly identical: the whiteboard and every handwritten word and drawing on it, the wall, the framing, the camera position, the lighting, the woman's face, hair and clothes. Change only her pose: with her right arm she now points the cap of the green marker at the words "✓ énergie" on the board, right next to them, without hiding them, and smiles at the camera with a rested, happy expression. Do not change, move or redraw any text.
```

## C4 — Q-A, segurando o pacote (T04)

Referências: **C3 aprovada** + `Referências/Sachê de Gomas de Magnésio Premium.png`. Salvar como `imagens/cenas/C4_v1.png`.

```
Use the first attached image as the base. Keep everything exactly identical: the whiteboard and every handwritten word and drawing on it, the wall, the framing, the camera position, the lighting, the woman's face, hair and clothes. Change only her pose: she now holds the product pouch from the second attached image with both hands in front of her chest, label facing the camera, upright and sharp, the markers tucked in one hand, smiling proudly at the camera. The pouch must match the reference exactly (same colours, logo "Cinnarae" and French label text). Do not change, move or redraw any text on the whiteboard.
```

## C5 — Quadro Q-B, apontando o bloco novo (T05)

Referências: **C3 aprovada**. Salvar como `imagens/cenas/C5_v2.png`.
Na v1, as linhas novas ficaram atrás da cabeça dela. Na v2, ela dá um passo para a direita do quadro e as linhas novas ficam na metade esquerda, livres.

```
Use the attached image as the base. Keep everything exactly identical: the whiteboard and all the existing handwritten words and drawings, the wall, the camera position, the framing, the lighting, the woman's face, hair and clothes. Change her position: she has stepped to the right side of the frame, so her body and head now occupy only the right third of the image and the left two thirds of the whiteboard below the existing writing are clearly visible and empty of people. On that visible left part of the board, directly under the existing writing, add two new handwritten lines in green dry-erase marker, same handwriting style and size as the existing lines, fully visible and not covered by her:
- a small drawing of two red gummy bears, then "2 gommes au coucher"
- "✓ nuit complète  ✓ énergie"
Her pose: she turns slightly toward the board and points the marker toward the new green lines with her right arm, without covering any text, looking at the camera and speaking. Do not change or redraw the existing text. All text in French with correct accents.
```

## C6 — Q-B, gesto aberto sorrindo (T06)

Referências: **C5 aprovada**. Salvar como `imagens/cenas/C6_v1.png`.

```
Use the attached image as the base. Keep everything exactly identical: the whiteboard and every handwritten word and drawing on it, the wall, the framing, the camera position, the lighting, the woman's face, hair and clothes. Change only her pose: both hands open at chest height in a relaxed, happy gesture, markers in one hand, a big genuine rested smile, looking at the camera. Do not change, move or redraw any text.
```

## C7 — Q-B, segurando o pacote (T07, T08)

Referências: **C5 aprovada** + `Referências/Sachê de Gomas de Magnésio Premium.png`. Salvar como `imagens/cenas/C7_v1.png`.

```
Use the first attached image as the base. Keep everything exactly identical: the whiteboard and every handwritten word and drawing on it, the wall, the framing, the camera position, the lighting, the woman's face, hair and clothes. Change only her pose: she holds the product pouch from the second attached image in her right hand in front of her chest, label facing the camera, upright and sharp, and looks at the camera with a confident smile. The pouch must match the reference exactly (same colours, logo "Cinnarae" and French label text). Do not change, move or redraw any text on the whiteboard.
```

---

## Clipes UGC (prova social, T07)

Mulheres francesas de 50+, todas diferentes entre si e diferentes da P1. Estética de vídeo caseiro de celular, luz natural. Referência em todas: `Referências/Sachê de Gomas de Magnésio Premium.png`.

## U1 — Cozinha, selfie de manhã

Salvar como `imagens/cenas/U1_v1.png`.

```
Photorealistic vertical 9:16 frame from a front-camera smartphone selfie video, arm's length, slightly high angle. A French woman aged about 58, short silver-grey bob haircut, thin tortoiseshell glasses, light-blue striped Breton shirt, standing in a bright Parisian kitchen in the morning (white cabinets, white metro tiles, wooden worktop, a moka coffee pot). With her free hand she holds the product pouch from the attached image up next to her face, label toward the camera, and smiles warmly. Natural home video look, realistic skin with age signs. The pouch must match the reference exactly (colours, "Cinnarae" logo, French label). No other text.
```

## U2 — Quarto à noite, tomando as gomas

Salvar como `imagens/cenas/U2_v1.png`.

```
Photorealistic vertical 9:16 frame from a smartphone video propped on a bedside table, evening. A French woman aged about 62, wavy shoulder-length white-blonde hair, soft pink satin pyjamas, sitting on her bed with white linen bedding, a warm bedside lamp on. She holds the open product pouch from the attached image in one hand and two red raspberry gummy bears in the palm of the other hand, about to take them, smiling calmly at the camera. Cosy bedtime routine, realistic skin with age signs, warm lamp light. The pouch must match the reference exactly (colours, "Cinnarae" logo, French label). No other text.
```

## U3 — Varanda parisiense

Salvar como `imagens/cenas/U3_v1.png`.

```
Photorealistic vertical 9:16 frame from a front-camera smartphone selfie video. A French woman aged about 54, dark brown curly hair with grey roots pulled back, natural look, cream linen shirt, on a small Paris balcony with a wrought-iron railing, red geraniums and Haussmann buildings behind her, daylight. She holds the product pouch from the attached image close to the camera with one hand, label facing the camera, and gives a happy nod. Natural home video look, realistic skin with age signs. The pouch must match the reference exactly (colours, "Cinnarae" logo, French label). No other text.
```

## U4 — Sala, polegar para cima

Salvar como `imagens/cenas/U4_v1.png`.

```
Photorealistic vertical 9:16 frame from a smartphone selfie video. A French woman aged about 65, short pixie-cut grey hair, small pearl earrings, soft burgundy knit cardigan, sitting on a sofa in a bright Parisian living room with tall windows and herringbone parquet. She holds the product pouch from the attached image in one hand, label toward the camera, and gives a thumbs up with the other hand, laughing. Natural home video look, realistic skin with age signs. The pouch must match the reference exactly (colours, "Cinnarae" logo, French label). No other text.
```
