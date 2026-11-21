# Formato: Tela verde

Formato 02 do quadro do Trello (ver [FORMATOS.md](../../FORMATOS.md)). **Ainda sem criativo nosso.**

## O que é

Só o corpo da pessoa aparece, recortado, e atrás dela entram imagens ligadas ao que está sendo dito (como um apresentador na frente de um telão).

## Por que prende

- **Ritmo**: fala acelerada e sem respiros; corta-se até a última sílaba antes da próxima frase.
- **Gancho visual**: o fundo muda a cada ideia.
- Tema conhecido ou absurdo; muitas vezes a história de alguém famoso com a identidade revelada só no fim (efeito a-há).

## Como escrever o roteiro

- Primeira frase com conflito forte sobre uma pessoa ou situação ("essa mulher foi humilhada até...") sem dizer quem é.
- Escalar o conflito em 3 ou 4 frases curtas, cada uma com uma imagem de fundo.
- Revelação no fim (quem era, o que aconteceu), depois a moral e o CTA.
- Frases curtas, sem pausas; o `montar.py` já encurta pausas acima de 0,3 s.

## Como produzir aqui

Precisa de uma ferramenta nova (`tela_verde.py`, ainda não existe):
1. Imagem da personagem sobre **fundo verde puro** (#00FF00), do peito para cima.
2. Takes Omni 360p normais a partir dela (o fundo fica liso).
3. Recorte com o filtro `chromakey` do FFmpeg e composição sobre as imagens de fundo, trocando nas palavras certas.

Alternativa sem ferramenta, mais cara: uma imagem de partida por fundo (a personagem editada na frente de cada cenário) e um take por trecho.

## Ângulo de anúncio (exemplo)

Cinnarae: fundos com o problema (noite em claro, relógio às 3h, cansaço no trabalho) mudando a cada frase, e o sachê no fundo no fim.

## Custo e riscos

Takes como no Lo-fi + imagens de fundo (~US$ 0,04 cada). Testar o recorte num take antes do lote: cabelo e mãos podem sair com borda verde.
