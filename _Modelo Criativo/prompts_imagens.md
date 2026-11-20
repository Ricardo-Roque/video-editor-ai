# Prompts de imagem — Criativo NN

Adaptações para o país de veiculação (cenário, bandeiras, rua vista pela janela, interiores):
- ...

Estilo geral: foto de celular (UGC), luz natural, sem aspecto de estúdio, sem texto na imagem, 9:16.
Ordem: personagens (P1, P2...) primeiro; cenas depois, sempre passando o personagem aprovado como `--ref`.
Cada seção abaixo precisa de um bloco de código com o prompt (o script de geração lê o primeiro bloco após o título).

---

## P1 — Personagem principal (referência de personagem)

```
Photorealistic smartphone photo, 9:16. Portrait of ... Neutral background, soft natural light, head and shoulders, looking at camera. Realistic skin texture, no text.
```

## H1 — Cena do hook

Referências: P1.

```
Photorealistic vertical smartphone selfie video frame, 9:16 ... no text.
```

## B1 — Cena base do body

Referências: P1 (+ cena do hook aprovada, se for o mesmo cenário).

```
Photorealistic vertical smartphone selfie, 9:16, front camera held at arm's length ... no text.
```

## O1 — Card/overlay (opcional)

```
Photorealistic close-up photo, 1:1 ... no text.
```
