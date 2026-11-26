# Formato: Comparação

Formato 13 do quadro do Trello (ver [FORMATOS.md](../../FORMATOS.md)). **Ainda sem criativo nosso como formato inteiro**; o hook do [Criativo 01](../Lo-fi/Criativo%2001/) (antes e depois) e os cards do [Criativo 05](../Lo-fi/Criativo%2005/) usam a mesma ideia.

## O que é

A tela é dividida: de um lado o jeito errado, do outro o certo. Variações: erro × acerto, pessoa 1 × pessoa 2, antes × depois.

## Por que prende

- **Contraste** no roteiro e no visual: o cérebro entende sem esforço.
- Quem assiste se pergunta de que lado está.
- Cena parada, dois lados, corte limpo: simples de reproduzir.

## Como escrever o roteiro

- Pouca fala ou nenhuma; o visual conta a história.
- Situações do dia a dia, lado a lado, em sequência (3 a 5 pares).
- Último par com o produto do lado certo.

## Como produzir aqui

- Hoje: pares de **imagens** lado a lado como overlays (`width` 540, `x` 0 e 540), como os cards do 05; ou uma imagem única já dividida.
- Dois **vídeos** lado a lado ainda não são suportados pelo `montar.py`: seria uma ferramenta nova (`hstack`/`vstack` do FFmpeg).
- Antes × depois da mesma pessoa: gerar o "depois" editando o "antes" (`--ref`), como no 01.

## Ângulo de anúncio (exemplo)

Cinnarae: noite da mulher que rola na cama × noite da que dorme; manhã cansada × manhã disposta; o sachê na mesa de cabeceira do lado certo.

## Custo e riscos

Barato se for só imagem. Antes × depois de corpo é risco de política alto (Meta/TikTok); antes × depois de sono ou humor é mais seguro.
