# Texto — Criativo 32 (FR)

Réplica do anúncio 2632439360559908 (ver [analise.md](analise.md)). Tradução de volta em [comparativo_roteiro.md](comparativo_roteiro.md).

## Adaptações

1. **Sem preço**: "$39.99 / $13.33 each" virou « Trois sachets pour le prix de deux. » O preço em euro não foi informado. Quando o dono informar, entra no `imagem.json` (custo 0).
2. **"Buy 2, Get 1 FREE"** → « 2 achetés. 1 offert. », a forma que a Cinnarae já usa.
3. **"The Winter Edition"** → « Édition hiver » (só enquadramento sazonal).
4. Saíram do texto por não estarem confirmados no `PRODUTOS.md`: "equivalente a 3.000 mg", recarga a cada 30 dias (assinatura), "não vendido na Amazon" e "sem ardor".
5. Rodapé da imagem: preço e assinatura trocados por « Une capsule par jour ».

## Texto da imagem (`imagem.json`)

- ÉDITION HIVER
- 2 achetés. 1 offert.
- Trois sachets pour le prix de deux.
- SATISFAIT OU REMBOURSÉ 30 JOURS · UNE CAPSULE PAR JOUR

## Post

```
2 achetés, 1 offert. Trois sachets de Piment de Cayenne Cinnarae pour le prix de deux. C'est toute la pub.

Du piment de cayenne en capsule molle, dans de l'huile. Avec betterave, aubépine, pépins de raisin, curcuma, poivre noir et vitamines D3 + K2. Une capsule par jour. Satisfait ou remboursé 30 jours.
```

- Título do link: « 2 achetés = 1 offert »
- Descrição do link: « Trois sachets pour le prix de deux · Satisfait ou remboursé 30 jours »
- Botão: « Acheter »

## Frases que dependem do dono (troca pronta)

| Situação | Troca |
|----------|-------|
| preço confirmado | imagem: « Trois sachets. XX € chacun. »; rodapé: « XX € · SATISFAIT OU REMBOURSÉ 30 JOURS · UNE CAPSULE PAR JOUR »; post: « Trois sachets pour XX €, soit XX € le sachet. » |
| "sem ardor" confirmado | depois de « dans de l'huile »: « , donc ça ne brûle pas. » |
| assinatura existe | « Recharge tous les 30 jours, sans engagement. » |
| "não vendido na Amazon" confirmado | « Pas vendu sur Amazon. » no fim |
| garantia diferente de 30 dias com reembolso | trocar « Satisfait ou remboursé 30 jours » nas duas peças |

## Notas de produção

- 2026-11-25: S1_v1 (sachê Cinnarae FR, US$ 0,04, aprovado, copiado para `Referências/Cinnarae Cayenne - Sachê FR.png`). B1_v1 (três sachês na prateleira, US$ 0,04). Texto e rótulo nítido compostos por `tools/compor_imagem.py` (custo 0): `final_v1` com o rótulo colado só até o título; `final_v2` até a grade de ingredientes. **Entra o `final_v2.png`.** A linha "Vitamines D3 + K2" segue um pouco borrada (fica atrás das pimentas, ilegível no celular de todo jeito).
- Gasto: US$ 0,075.
- 2026-11-25, pedido do dono ("o mais perto do realismo possível"): B1_v2 com prompt de foto real (lente 85 mm, luz de janela, granulação, sachês maiores e juntos, US$ 0,034). Rótulo nítido colado só na grade de ingredientes (o resto já saiu legível). **Entra o `final_v3.png`.** Gasto total: US$ 0,109.
