# Conceito — Criativo 29

Processo: **Modelagem** ([MODELAGEM.md](../MODELAGEM.md), etapa M2).
Anúncio base: Criativo 05 ([quebra.md](../Criativos%20Exemplo/Narrado/Criativo%2005/quebra.md)), 2 vendas em 2026-11-24.
Marca: Cinnarae. Idioma: francês. País: França.
Biblioteca lida em: 2026-11-24 (`Variáveis/Cinnarae.md`).

## Teste

```
Teste: CIN-T002 — Criativo 29 — "Si..." com sintomas de sono sem glicemia
Vencedoras empilhadas: nenhuma provada; constantes do 05: CIN-V001 (prancheta + narradora), CIN-V014 (anáfora), CIN-V015 (callback), CIN-V018 (marca aos 48%), CIN-V003 (ritmo), CIN-V004 (prova social), CIN-V005 (oferta), mesma voz (seed 505)
Variável em teste: dor de entrada do hook: xixi 3x + boca seca + não dormir (glicemia/insulina) → cãibras e pernas que mexem + despertar às 3 h + acordar cansada (músculos, sistema nervoso, cansaço)
Hipótese: o que vende no 05 é a forma (sintoma noturno concreto em "Si..." com callback), não a glicemia; com sintomas de sono e mecanismos autorizados, o CPA fica igual ou melhor e o risco de reprovação cai
Vence se: CPA igual ou menor que o do 05 no mesmo período, com gasto de pelo menos 2x o CPA do 05
Perde se: CPA 30% acima do 05 com o mesmo gasto, ou hook rate 5 pontos abaixo
Métricas: hook rate (barra: acima de 50%), CTR, CPA
Tipo: Deliberado
Formato e produção: Narrado (igual ao 05). Prancheta 1 nova + 2 variações da varinha + prancheta 2 com o callback novo (4 imagens, ~US$ 0,16); takes T01–T03 e T05 novos (~45 s, ~US$ 1,05); T04, T06, T07 e T08 reaproveitados do 05. Total ~US$ 1,20
```

**Escolhido**: CIN-T002, em 2026-11-24 (o dono pediu as três variações: 29, 30 e 31).

## Padrão reutilizável

Os 9 passos da seção 8 da quebra do 05. Este criativo segue todos; só a variável em teste muda.

## Constantes do teste

Prancheta, varinha, mesa de madeira, título, cores dos painéis, voz (seed 505), T04 a T08 (áudio e imagens), prova social, oferta, legenda, duração (~63 s).

## Produção

- Formato: Narrado (formato 04), receita do 05. Guia: `Criativos Exemplo/Narrado/FORMATO.md`.
- Texto na tela: pranchetas com `prancheta_zoom.py` (tabela "Texto na tela" do `PROCESSO.md`), texto nítido da imagem, nunca do modelo de vídeo.
- Imagens: Q1a, Q1b, Q1c (edição da Q1a/b/c do 05 com o texto novo) e Q2a, Q2b, Q2c (edição das do 05, só o painel de baixo). 6 × ~US$ 0,04 = ~US$ 0,24.
- Takes: T01, T02, T03, T05b, Omni 360p, persona `board` do 05 (seed 505). ~36 s × US$ 0,023 = ~US$ 0,85.
- Reaproveitado do 05 (custo 0): áudio de T04, T05a, T06; segmentos T07 e T08; vídeo da R1.
- Total: ~US$ 1,10.

## Política e perguntas abertas

- Riscos: "dormirez enfin d'une traite" e "pourrez enfin vous rendormir" prometem sono (não é alegação autorizada; mesmo nível do 05). "120 000 femmes" sem fonte (constante do 05). A glicemia sai.
- Fatos que faltam: oferta -20% ainda vale? "120 000 femmes" é verdadeiro?
