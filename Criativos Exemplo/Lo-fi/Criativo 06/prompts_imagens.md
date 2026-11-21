# Prompts de imagem — Criativo 06 (versão França)

Adaptações para a França: quarto de hospital francês (leito com grade, suporte de soro, monitor de sinais vitais, quadro branco sem texto legível, paredes claras, luz fria de teto). Sem texto em inglês, sem marca legível.
Personagem: mesmo visual da referência (mulher de ~50 anos, cabelo castanho na altura do ombro com mechas e franja lateral, scrub azul royal), com rosto novo, sem copiar a pessoa da referência.

Estilo geral: foto de celular (UGC) no tripé, câmera na altura do peito, luz de hospital, sem aspecto de estúdio, sem texto na imagem, 9:16.
Ordem: P1 primeiro; depois B1 com P1 como ref; H1, B1b e B1c são edições de B1 (`--ref B1`).

---

## P1 — Profissional de saúde (referência de personagem)

```
Photorealistic smartphone photo, 9:16. Portrait of a French woman around fifty, oval face with soft cheekbones, light olive skin with natural fine lines around the eyes, hazel-green eyes, warm friendly smile. Shoulder-length layered chestnut-brown hair with subtle caramel highlights, a long side-swept fringe, slightly tousled. Small gold hoop earrings, natural light makeup. She wears royal blue medical scrubs: a short-sleeved V-neck scrub top with a small chest pocket. A white silicone wristband on her left wrist. Plain light-grey neutral background, soft natural light, framed from the waist up, looking at the camera. Realistic skin texture, no text, no logos.
```

## B1 — Base no quarto de hospital (T03, T04, T11, T12, T14, T16)

Referências: P1 (identidade) + `referencia/sala/sala_mascarada.png` (frame da referência com a mulher coberta, só para o cenário). Salvar como `imagens/cenas/B1_v1.png`.
Pedido do usuário: mesmo cenário da referência e personagem mais longe da câmera (a P1 de perto ficou com cara de falsa).

```
Image 1 is the woman: use it only for her identity, face and hair. Image 2 is the room: a hospital room seen from the same camera position; the grey rectangle is just a mask, ignore it and fill that area with the room. Do not copy any person from image 2. Create a photorealistic vertical smartphone video still, 9:16, recorded on a phone propped on a tripod about two metres away at chest height, slight wide-angle phone lens. The woman from image 1 stands in the centre of this same hospital room, full figure from the top of her head down to just above her knees, her head near the top of the frame with little headroom, her body filling about three quarters of the frame height. She wears royal blue short-sleeved V-neck scrubs with a tiny white square logo patch on the chest, matching royal blue scrub trousers with a grey drawstring tied at the waist, a white hospital-style wristband and a couple of thin bracelets on her left wrist, small gold hoop earrings. Room exactly as in image 2: cream-beige walls, a wall-mounted whiteboard on the left with a dark frame and nothing written on it, a grey metal door handle below it, a metal IV pole with infusion pumps and a vital-signs monitor on a wall arm on the right, the edge of a hospital bed with white sheets and metal side rails at the right edge, beige linoleum floor, flat cool fluorescent ceiling light. Hands relaxed and loosely clasped in front of her waist, friendly confident expression, mouth slightly open as if starting to speak. Real amateur phone footage look: slightly flat exposure, mild noise, soft focus on the background, no studio lighting, realistic skin texture. No readable text anywhere.
```

## H1 — Hook: mão mostrando 5 (T01)

Referências: B1_v2. Salvar como `imagens/cenas/H1_v1.png`.

```
Edit the attached image. Keep the same woman, face, hair, scrubs, wristband, hospital room, framing and lighting exactly the same. Change only her pose: her right hand is raised beside her shoulder, open palm facing the camera showing five spread fingers, and her left hand rests on her hip. Bright engaged expression, mouth open mid-word. No text.
```

## B1b — Dedo indicador levantado (T05, T06, T08, T09, T13)

Referências: B1_v2. Salvar como `imagens/cenas/B1b_v1.png`.

```
Edit the attached image. Keep the same woman, face, hair, scrubs, wristband, hospital room, framing and lighting exactly the same. Change only her pose: her right hand is raised in front of her chest with the index finger pointing up, as if making a point, left arm relaxed at her side. Confident, explaining expression, mouth slightly open. No text.
```

## B1c — Mão no peito (T02, T07, T10, T15)

Referências: B1_v2. Salvar como `imagens/cenas/B1c_v1.png`.

```
Edit the attached image. Keep the same woman, face, hair, scrubs, wristband, hospital room, framing and lighting exactly the same. Change only her pose: her right hand rests flat on her upper chest, below the collarbone, left arm relaxed at her side. Sincere, warm expression, slight smile, mouth slightly open as if speaking. No text.
```
