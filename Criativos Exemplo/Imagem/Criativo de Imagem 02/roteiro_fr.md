# Texto — Criativo de Imagem 02 (FR)

Réplica do anúncio 29494374796826540 (ver [analise.md](analise.md)). Tradução de volta em [comparativo_roteiro.md](comparativo_roteiro.md).
Decisão padrão (dono liberou a criação em 2026-11-25 sem escolher): **título fiel**, com a versão suave pronta abaixo.

## Adaptações

1. "Cold feet" → « pieds gelés », como o francês fala no dia a dia; "froids" soaria clínico.
2. **Sem preço** (euro não informado): a oferta é « 2 achetés = 1 offert : trois sachets pour le prix de deux ».
3. **Assinatura**: "Jane Kahn, Founder" → « L'équipe Cinnarae », e o bilhete passa de "eu" para "nós". Fundador(a) real não confirmado(a).
4. Saíram por falta de confirmação: "equivalente a 3.000 mg", "sem ardor", recarga a cada 30 dias, e "a maioria nota mãos e pés primeiro, nas primeiras semanas" (sem fonte).
5. Quarto francês na foto: colcha xadrez de casa de campo, janela de batente com cortina de linho.

## Texto da imagem (`imagem.json`)

- Faixa de cima: PIEDS GELÉS AU LIT APRÈS 55 ANS ? / C'EST LA CIRCULATION. ⚠
- « Les analyses sont bonnes », vos pieds disent le contraire ⚠
- Selo: 30 JOURS / SATISFAIT OU REMBOURSÉ
- Faixa de baixo: 2 ACHETÉS = 1 OFFERT · UNE CAPSULE PAR JOUR

## Post

```
La vue depuis l'oreiller, après 55 ans : la couette repliée, les chaussettes en laine, et les pieds toujours gelés. Une chaussette déjà à moitié enlevée, parce que la chaussette n'est pas la réponse.

C'est la circulation. ⚠ Avec l'âge, les petits vaisseaux des pieds se resserrent, et la chaleur est la première chose qui s'en va. Une chaussette peut garder la chaleur. Elle ne peut pas en fabriquer.

Le Piment de Cayenne Cinnarae agit de l'intérieur ⚠ : du piment de cayenne en capsule molle, dans de l'huile, avec betterave, aubépine, pépins de raisin, curcuma, poivre noir et vitamines D3 + K2.

Mode d'emploi : une capsule par jour, pendant un repas.

2 achetés = 1 offert : trois sachets pour le prix de deux. Satisfait ou remboursé 30 jours.

Un petit mot de notre part : gardez les chaussettes. Regardez juste si vous en avez encore besoin dans 30 jours. Si oui, on vous rembourse la commande.

— L'équipe Cinnarae
```

- Título do link: « La vue depuis l'oreiller, après 55 ans. »
- Descrição do link: « Pieds gelés au lit : c'est la circulation · 2 achetés = 1 offert »
- Botão: « Acheter »

## Frases ⚠ e alternativa suave (trocar uma não mexe no resto)

| Frase | Risco | Alternativa suave |
|-------|-------|-------------------|
| C'EST LA CIRCULATION. (imagem) | afirma a causa de um sintoma; "circulação" de plantas é alegação "on hold" na UE | ET SI C'ÉTAIT LA CIRCULATION ? |
| « Les analyses sont bonnes », vos pieds disent le contraire | põe o exame médico em dúvida | Les chaussettes en laine n'y font rien |
| C'est la circulation. (post) | idem | Et si c'était la circulation ? |
| Avec l'âge, les petits vaisseaux des pieds se resserrent | mecanismo sem fonte verificada | Avec l'âge, la chaleur a plus de mal à arriver jusqu'au bout des pieds. |
| agit de l'intérieur | promessa de efeito | se prend de l'intérieur |
| « c'est la circulation » (descrição do link) | idem | « Pieds gelés au lit après 55 ans ? » |

## Frases que dependem do dono

| Situação | Troca |
|----------|-------|
| preço confirmado | faixa de baixo: « 2 ACHETÉS = 1 OFFERT — XX € · UNE CAPSULE PAR JOUR »; post: « trois sachets pour XX €, soit XX € le sachet » |
| fundador(a) real | « Un petit mot de ma part : ... je vous rembourse la commande. — [Nom], fondatrice/fondateur de Cinnarae » |
| "sem ardor" confirmado | depois de « dans de l'huile »: « (ça ne brûle pas) » |
| assinatura existe | « Recharge tous les 30 jours, sans engagement. » |

## Notas de produção

- 2026-11-25: B1_v1 (POV do travesseiro, US$ 0,04, primeira tentativa). Faixas, selo e rótulo nítido por `tools/compor_imagem.py` (custo 0). `final_v1`: a colagem pelo contorno do sachê trouxe a beterraba da foto do sachê e deixou texto fantasma. `final_v2`: faixa retangular, mas a pílula "1 capsule par jour" saiu dobrada. `final_v3`: rótulo 4% maior e faixa de baixo sem as bordas. **Entra o `final_v3.png`.**
- Gasto: US$ 0,036.
- 2026-11-25, pedido do dono (realismo): B1_v2 como foto de celular tirada da cama, sachê grande em primeiro plano no criado-mudo (US$ 0,036). Rótulo nítido colado até a pílula, sem cobrir o copo. Selo menor, acima do sachê. **Entra o `final_v5.png`.** Gasto total: US$ 0,072.
- 2026-11-25, dono achou a v5 "muito ruim" e pediu para refazer uma coisa por vez: E1 só pés + sachê (E1_v1 saiu sem prompt por erro de título de seção, descartado; E1_v2 aprovado: "ficou melhor"), depois edições em cadeia E2 colcha xadrez, E3 janela com cortina, E4 abajur, E5 cápsula + copo. As edições em cadeia degradaram a textura das meias (azuladas, artificiais): as meias do E2 foram coladas localmente sobre o E5 (`E5_v1_meias.png`). Rótulo nítido colado em 3 faixas sobrepostas, com uma única correção de cor por sachê (sem emenda). Selo movido para a esquerda, sobre a janela, para não esconder o abajur. **Entra o `final_v9.png`.** Gasto desta refação: US$ 0,215 (US$ 0,035 perdidos no E1_v1).
- 2026-11-25, pedido do dono: usar a `E5_v1.png` sem mexer (sem as meias do E2 e sem o rótulo colado), só com faixas, selo e texto por cima. **Entra o `final_v10.png`.** O texto miúdo do sachê fica como o Nano Banana desenhou (logo e « PIMENT DE CAYENNE » legíveis; o resto ilegível no celular).
