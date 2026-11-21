# Formato: Cine

Formato 05 do quadro do Trello (ver [FORMATOS.md](../../FORMATOS.md)). **Ainda sem criativo nosso.**

## O que é

Vídeo com faixas pretas em cima e embaixo, como cinema, que não ocupa a tela inteira e por isso foge do padrão do feed. Variações: só a fala com imagens ilustrando, a fala com letreiros fortes, ou cru como uma chamada de vídeo (só com roteiro muito bom).

## Por que prende

- O visual diferente para o dedo no feed.
- Tom de conversa íntima: um conselho, um desabafo, uma reflexão.
- **Música** que reforça a emoção (de preferência conhecida do público).

## Como escrever o roteiro

- Frase de abertura que é uma tese emocional e incômoda ("ninguém vai te dar permissão para descansar").
- Frases curtas e declarativas, alternando conflito e mudança.
- Contraste entre passado e presente ("quando éramos crianças... quando crescemos...").
- Fechar com a moral em uma frase que dá vontade de salvar ou mandar para alguém.

## Como produzir aqui

Possível hoje com um ajuste simples:
- **Faixas pretas**: PNG transparente 1080x1920 com faixas pretas em cima e embaixo, aplicado como overlay `{"mode": "patch", "x": 0, "y": 0}` no vídeo todo (gerar com PIL; uma ferramenta pequena pode ser criada se o formato for usado).
- **Enquadramento**: a imagem de partida precisa ter o rosto na faixa central (a área visível fica entre ~y=420 e ~y=1500).
- **Legenda**: dentro da faixa de baixo ou logo acima dela (`caption_y` ~1560), em fonte menor se necessário.
- **Música**: o `montar.py` ainda não mistura trilha. É a principal melhoria pendente para este formato.

## Ângulo de anúncio (exemplo)

Cinnarae: reflexão de uma mulher de 50+ sobre parar de se culpar pelo cansaço e cuidar do próprio sono, com o produto entrando só no fim e de forma leve.

## Custo e riscos

Igual a um Lo-fi. Sem riscos próprios além da copy.
