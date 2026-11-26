# Formato: Imagem (anúncio estático com texto na imagem)

**Fora dos 16 formatos do Trello** (que são de vídeo) e diferente do [Nativo](../Nativo/FORMATO.md). No Nativo, a foto é amadora e sem texto, e quem vende é a história longa do post. Aqui **a imagem é a peça**: título, oferta e selo escritos nela, e o post é curto (70 a 200 palavras). No Drive do time, entra como `Criativo de Imagem #NN`.

As primeiras referências vieram da Vitalia (mesmo produto da Cinnarae Cayenne), na Biblioteca de Anúncios.

## Exemplos

| Criativo | Tipo de imagem | Aspecto | Custo | Ver primeiro |
|----------|----------------|---------|-------|--------------|
| [32](Criativo%2032/) | oferta pura: "2 achetés. 1 offert." em serifa sobre três sachês numa prateleira, visual de catálogo creme e dourado | 1:1 | US$ 0,11 (sachê aprovado + 2 fotos) | `imagem.json`, rótulo nítido colado só na grade de ingredientes |
| [33](Criativo%2033/) | foto POV do travesseiro (pés de meia de lã, sachê no criado-mudo) entre faixa de título vermelha e faixa de oferta | 4:5 | US$ 0,29 (com a refação passo a passo) | notas de produção: refação "uma coisa por vez" |
| [34](Criativo%2034/) | carta tipográfica em fundo preto ("DERNIÈRE SÉRIE."), assinatura manuscrita | 4:5 | US$ 0,036 (só a assinatura) | aviso de escassez real (Code de la consommation L121-4) |

## Por que prende

- **Oferta como peça inteira** (32): visual calmo, de catálogo, destoa das promoções gritadas; a conta pronta ("três pelo preço de dois") responde antes do clique. Funciona para quem já conhece o produto.
- **O problema visto de dentro** (33): a pessoa vê os próprios pés, do ângulo de quem está deitado. O título diz idade, lugar e causa em poucas palavras.
- **Contraste de feed** (34): quadrado preto com duas palavras enormes, parece documento interno, não anúncio.

## Receita de produção

1. **Foto sem texto** no Nano Banana, com o sachê aprovado como `--ref` (`Referências/Cinnarae Cayenne - Sachê FR.png`). Pedir "real photograph / smartphone photo, natural light, grain, not a 3D render": o dono pediu o máximo de realismo.
2. **Cena complexa: uma coisa por vez** (33). Primeiro só o essencial (pés + sachê), aprovado; depois edições em cadeia acrescentando um elemento por vez (colcha, janela, abajur, cápsula e copo). Cuidado: cada edição degrada um pouco a textura do que já estava na imagem (as meias ficaram "cozidas" no 5º passo). O dono preferiu a última edição como saiu, sem retoque.
3. **Todo o texto local** com `tools/compor_imagem.py` e um `imagem.json` por criativo: faixas, selo, título, rodapé, em fontes do Windows (Georgia, Impact, Arial, Consolas). Trocar preço, frase ou assinatura custa 0.
4. **Rótulo nítido** (opcional): a camada `rotulo` cola o rótulo do sachê aprovado por cima, em faixas retangulares sobrepostas e com uma correção de cor por sachê. Evitar as bordas onde há objetos na frente (pimenta, beterraba, copo).
5. **Assinatura manuscrita**: gerada no Nano Banana em tinta branca sobre preto e colada com `"blend": "lighten"` (34).

## Cuidados

- **Preço**: o euro ainda não foi informado; os três saíram com "trois sachets pour le prix de deux". Preço confirmado entra no `imagem.json`.
- **Escassez** (34): só se for verdade. Escassez falsa é prática comercial enganosa na França.
- **Alegação de causa** (33, "C'est la circulation."): "circulação" de plantas é alegação "on hold" na UE; a versão suave está no roteiro.
- **Assinatura de pessoa**: sem fundador(a) real confirmado(a), assina « L'équipe Cinnarae ».
