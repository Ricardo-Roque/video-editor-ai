# Formato: Tela dividida

Formato 01 do quadro do Trello (ver [FORMATOS.md](../../FORMATOS.md)). **Ainda sem criativo nosso.**

## O que é

A tela é dividida em duas metades: numa, imagens do que está sendo dito; na outra, a pessoa falando. Variações: analisar uma pessoa ou marca conhecida, ilustrar a fala com imagens, ou narrar uma cena que passa em cima.

## Por que prende

- A metade de imagens é um **gancho visual** permanente: o olho tem sempre algo novo para ver.
- A imagem precisa casar com a frase falada naquele momento; quanto mais literal o encaixe, menos esforço para entender.
- Funciona com tema que todo mundo conhece (cultura pop, notícia, conflito universal).

## Como escrever o roteiro

- Abrir com um **conflito universal** ou uma cena forte já ilustrada em cima (a imagem do hook faz metade do trabalho).
- Contar a história em frases curtas, **uma imagem por frase**: cada frase precisa ser ilustrável.
- Usar "mas" para virar a história a cada 2 ou 3 frases (contraste) e segurar a revelação principal (efeito a-há) para o fim.
- Fechar trazendo a história para a vida de quem assiste (moral) e só então o produto.

## Como produzir aqui

Possível hoje, sem ferramenta nova:
- **Pessoa**: imagem com a personagem enquadrada na **metade de baixo** do quadro 9:16 (do peito para cima, cabeça abaixo do meio). Takes Omni 360p normais, como no Lo-fi.
- **Metade de cima**: uma imagem por frase (Nano Banana, ~US$ 0,04 cada). Entra como overlay em cada trecho com `"width": 1080, "aspect": 1.125, "x": 0, "y": 0` (1080x960) e `from_word`/`to_word`. O card sai com cantos arredondados; se incomodar, é um ajuste pequeno no `make_card` do `montar.py`.
- **Legenda** na divisa: `"caption_y": 990`.
- Imagens de cima sem texto pequeno; texto, se houver, em PNG local.

## Ângulo de anúncio (exemplo)

Cinnarae: história verificável e conhecida sobre sono ou estresse (estudo publicado, personagem público com fonte) em cima, e a apresentadora conectando com o problema de quem assiste e o produto. Toda afirmação factual precisa de fonte; nada inventado.

## Custo e riscos

Como um Lo-fi + 6 a 12 imagens (US$ 0,25 a 0,50 a mais). Cuidado com imagens de pessoas reais e marcas de terceiros na metade de cima.
