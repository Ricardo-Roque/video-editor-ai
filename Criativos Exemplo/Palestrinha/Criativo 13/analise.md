# Análise — Criativo 13 (copy do Criativo 05 no formato "palestrinha")

Copy: a mesma do [Criativo 05](../../Narrado/Criativo%2005/roteiro_fr.md), que fez a primeira venda. Está em francês, com "vous" e "gommes", agressiva e aprovada.
Referência de formato: `Vídeo Bruto/Criativo #10.mp4` (116,7 s, 360x640, japonês). Não é a referência da pasta `Criativo 10`, que usa o arquivo com nome de hash.
Arquivos da análise: `referencia_formato/` (transcrição, cortes, folhas de frames).
Produto: **Cinnarae** (gomas de bisglicinato de magnésio, ursinhos vermelhos de framboesa). País: França. Idioma: francês.

## O formato "palestrinha" (referência #10)

Um apresentador fala **direto para a câmera**, de pé na frente de um quadro branco, como numa mini-aula.

- **Câmera:** tripé fixo, plano médio (da cabeça até a coxa) e vertical. O quadro branco ocupa o fundo inteiro; atrás dele há uma parede escura de ripas.
- **Apresentador:** camiseta branca lisa e canetões vermelho e verde na mão. Ele gesticula na altura do peito e de vez em quando se vira e aponta para o que está escrito no quadro.
- **Quadro:** tem letra de mão grande, poucas palavras e desenhos simples (comprimidos, xícara de café, canela, um rosto enjoado, fogo com "açúcar"), em duas colunas comparativas (X vs Y). Ele **cresce ao longo do vídeo**: no corte seco de 76 s aparecem linhas novas embaixo (o mecanismo, uma linha por ativo).
- **Edição:** só há 1 corte seco (76,3 s). Os outros 11 são jump cuts no mesmo plano, quando o apresentador muda de posição. Não há B-roll.
- **Produto:** o apresentador segura o pote na frente do peito duas vezes: na apresentação (60–67 s) e no CTA final (108–116 s).
- **Legenda:** pequena, branca, com a palavra-chave em amarelo, a ~73% da altura. É o nosso padrão do `montar.py`.

Conteúdo da referência, traduzido para o português, só para você entender o formato (não vamos usar):

| Tempo | Fala (resumo em PT) | Quadro |
|-------|---------------------|--------|
| 0–19 | "Metformina vs canela-do-ceilão, a metformina natural. Metformina: um comprimidão de manhã, outro à noite, a caixa sempre na bolsa. Canela: uma cápsula com o café. Só isso." | 2 colunas já escritas |
| 19–34 | Efeitos colaterais da metformina: enjoo, barriga inchada, diarreia, correr ao banheiro no restaurante e, anos depois, formigamento nos pés por falta de B12. | aponta a lista da esquerda |
| 34–60 | Canela: energia o dia todo, sem a moleza das 15h, sem vontade de beliscar, queima o açúcar. Metformina 500 → 1000 → 2000 mg e a barriga não muda; canela é 1 por dia, sempre a mesma dose. | aponta as duas colunas |
| 60–76 | "Vou mostrar como a canela da Kenzendo funciona" (segura o pote). Diabetes e peso são o mesmo problema. | — |
| 76–108 | Mecanismo: MHCP abre as células, cinamaldeído freia o açúcar da refeição, proantocianidinas estabilizam a glicemia. | escreve 3 linhas novas |
| 108–116 | "100% natural, a metformina natural. Veja as avaliações, o link está abaixo." (segura o pote) | — |

## Como a copy do 05 entra nesse formato

A fala é **a mesma do 05, palavra por palavra** (`roteiro_05_base.md`). Mudam só o visual e quem fala: sai a narradora em off com a prancheta e entra uma apresentadora falando para a câmera na frente do quadro branco.

| Take | Fala (resumo em PT) | Visual proposto | Estado do quadro |
|------|---------------------|-----------------|------------------|
| T01 | "Se a glicemia te faz mijar 3x por noite…" | apresentadora aponta a linha 1 | **Q-A**: título + 3 problemas, cada um com ícone e uma seta para a solução |
| T02 | "Se acorda com a boca seca como um deserto…" | aponta a linha 2 | Q-A |
| T03 | "Se não consegue dormir a noite inteira…" | aponta a linha 3 | Q-A |
| T04 | "E eu uso as gomas da Cinnarae. Sem açúcar e suaves para o estômago." | **segura o pacote** na frente do peito | Q-A |
| T05 | "Tome duas antes de dormir… Agora durmo a noite toda. Chega de banheiro, chega de boca seca." | aponta a parte nova | **Q-B**: Q-A + bloco novo embaixo ("2 avant le coucher", lua, ✓/✗ dos resultados) |
| T06 | "Acordo descansada, com energia o dia todo." | gesto aberto, sorrindo | Q-B |
| T07 | "Mais de 120.000 mulheres já tomam… e sempre esgota." | segura o pacote (ou as fotos F1–F4 do 05, veja a pergunta 2) | Q-B |
| T08 | "Se não sentir diferença em 30 dias, devolvemos. Clique no link, 20% off…" | segura o pacote e aponta para baixo (link) | Q-B |

Esse corte em dois estados (Q-A e Q-B) imita o quadro que cresce na referência.

## Desafio técnico: texto do quadro legível

O texto do quadro deformou no take do 05 em 360p e você reprovou. Aqui há um rosto falando, então não dá para trocar o take por imagem parada. Plano:

1. **Quadro com poucas palavras e letras grandes**, como na referência: 3 a 4 palavras por linha, ícones desenhados.
2. **Apresentadora abaixo do texto:** o texto fica no terço de cima do quadro, acima da cabeça dela. Na montagem eu colo a faixa nítida do quadro (a imagem aprovada) por cima do take (`"mode": "patch"`, custo 0). A apresentadora gesticula abaixo dessa faixa. Para apontar, ela levanta o canetão até a borda da faixa, sem entrar no texto.
3. **Teste antes do lote:** um take com Omni 360p (~US$ 0,28) e, se o rosto/boca não ficar bom, um com Veo 3.1 Lite 720p (~US$ 0,40, o mesmo do 11/12).

## Imagens necessárias

1. **P1**: apresentadora francesa de ~40 anos (a copy é feminina: "reposée", "je dors"), camiseta branca lisa, cabelo castanho preso, visual natural. Fundo neutro.
2. **Q-A**: quadro branco + parede de ripas com o estado 1 escrito, **sem pessoa**. É a base de todas as cenas.
3. **Q-B**: Q-A editada, acrescentando o bloco 2. Também sem pessoa.
4. **Cenas** (P1 + quadro), cada uma editada da anterior para manter luz e enquadramento:
   - C1 apontando a linha 1, C2 a linha 2, C3 a linha 3 (com Q-A)
   - C4 segurando o pacote Cinnarae (com Q-A; ref. do pacote em `Referências/`)
   - C5 apontando o bloco 2, C6 gesto aberto sorrindo, C7 segurando o pacote (com Q-B)
   - O T08 reaproveita a C7.

Total: ~10 imagens × US$ 0,04 ≈ **US$ 0,40** (com refações, ~US$ 0,55).

## Custo estimado

| Item | Custo |
|------|-------|
| Imagens (~10–14) | US$ 0,40–0,55 |
| Teste de take (Omni 360p; Veo só se precisar) | US$ 0,28–0,70 |
| Takes (~75 s brutos) | Omni 360p ≈ US$ 1,75 · Veo 720p ≈ US$ 4,00 |
| Montagem | 0 |
| **Total** | **~US$ 2,50 (Omni)** ou **~US$ 5,00 (Veo)** |

Duração final esperada: ~62 s, igual ao 05.

## Alerta de política

No 05 as alegações vinham de uma voz em off. Aqui **uma pessoa real na tela** diz em primeira pessoa que usa e que funcionou, com alegações de glicemia e insulina. Para a Meta, isso é um depoimento fabricado somado a alegações de saúde, um risco de reprovação maior que o do 05. A decisão é sua: a copy fica igual.

## Decisões (2026-11-20)

1. Apresentadora: uma mulher de 50+.
2. Prova social do T07: 4 clipes UGC novos (U1–U4) com mulheres de 50+ e o pacote, de 3 s cada, sem áudio, com a voz da apresentadora por cima. Custo extra: 4 imagens (US$ 0,16) + 12 s de take (~US$ 0,28).
