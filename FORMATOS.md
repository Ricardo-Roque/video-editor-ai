# Formatos criativos

Os formatos que o time usa vêm do quadro do Trello **"Formatos Criativos de Conteúdo"** (área de trabalho Grupo RME), que tem os vídeos de referência e os prompts de roteiro de cada formato. Este arquivo resume o quadro para o processo de produção com IA: o que é cada formato, se já temos exemplo pronto e como produzi-lo aqui.

A ideia do quadro: o algoritmo favorece **formatos**, não perfis. Quem acha um formato que funciona e o repete viraliza a maioria dos vídeos. Para anúncios vale o mesmo: quando um criativo vende, repetimos o formato e a copy (ex.: copy do 05 virando Palestrinha no 13).

## Os 16 formatos

| # | Formato | O que é | Exemplo nosso | Como produzir aqui |
|---|---------|---------|---------------|--------------------|
| 01 | Tela dividida | metade de cima com imagens do que é falado, metade de baixo com a pessoa falando (ou o contrário) | — | take da pessoa (Omni) + imagens nas palavras certas; precisa de um modo de overlay "metade da tela" no `montar.py` |
| 02 | Tela verde | só o corpo da pessoa, com imagens do assunto trocando atrás dela; fala acelerada, sem respiros | — | takes com fundo liso + recorte da pessoa e fundo trocado na montagem (ferramenta ainda não existe) |
| 03 | Palestrinha | a pessoa explica apoiada num quadro, slide, TV ou notebook; o visual prova o ponto e dá autoridade | [13](Criativos%20Exemplo/Palestrinha/) | ver [FORMATO.md](Criativos%20Exemplo/Palestrinha/FORMATO.md) |
| 04 | Narrado | voz em off sobre imagens, cortes a cada ~3 s, tom de conversa | [05, 11, 12](Criativos%20Exemplo/Narrado/) | ver [FORMATO.md](Criativos%20Exemplo/Narrado/FORMATO.md) |
| 05 | Cine | vídeo com faixas pretas em cima e embaixo, foge do padrão do feed; fala de conversa, música que reforça a emoção | — | qualquer take + letterbox na montagem (opção a criar no `montar.py`) |
| 06 | Storytelling visual | cada frase vira uma ação ou objeto em cena (encenação exagerada ou desenho) | — | várias imagens curtas, uma por frase; muitos takes curtos ou imagens com zoom; caro em takes |
| 07 | Experimento social | entrevista na rua com desconhecidos, respostas espontâneas e opostas | — | difícil com IA: várias pessoas e cenário de rua; testar Veo com personas diferentes |
| 08 | Conflito situacional | abre com uma cena forte que parece real (briga, queda, batida) e depois vira o conteúdo | (08 tem um gancho visual parecido) | take de ação sem fala no hook (`"silent": true`, como no 08) + body em outro formato |
| 09 | Dinamismo | câmera parada, a pessoa se move o tempo todo (perto, longe, entra, sai) | — | uma imagem de partida por posição e jump cuts entre takes |
| 10 | Trivial | fala para a câmera fazendo uma tarefa do dia a dia (café, cozinhar, se arrumar) | — | igual ao Lo-fi, com a ação descrita na persona do take |
| 11 | Diálogo | a mesma pessoa encena dois personagens, o "errado" e o "certo" | — | duas personas (roupa e voz diferentes) e takes alternados |
| 12 | Caixinha de perguntas | uma pergunta polêmica na tela e a resposta da pessoa | — | caixinha como PNG (overlay `patch`) + take Lo-fi |
| 13 | Comparação | tela dividida com o jeito errado de um lado e o certo do outro (ou antes × depois) | (hook do 01 e cards do 07) | dois takes ou imagens lado a lado (overlays com `width`/`x`/`y`, como no 07) |
| 14 | The Office | cenas normais alternadas com "confessionário" olhando para a câmera | — | dois cenários/enquadramentos da mesma personagem |
| 15 | Lo-fi | simples e "imperfeito" de propósito, fala como com uma amiga | [01, 04, 06, 07, 08, 09, 10](Criativos%20Exemplo/Lo-fi/) | ver [FORMATO.md](Criativos%20Exemplo/Lo-fi/FORMATO.md) |
| 16 | Bastidores | mostra como foi feito antes do resultado | — | pouco útil para anúncio de produto |

Formato sem exemplo: na análise, dizer qual é, propor a produção com base nesta tabela e avisar se precisa de ferramenta nova antes de gastar.

## Estruturas de roteiro

Toda análise identifica qual estrutura a referência usa; o roteiro traduzido mantém a mesma.

| Estrutura | Etapas | Quando aparece |
|-----------|--------|----------------|
| AIDA | atenção (tema + curiosidade ou conflito) → interesse (argumento, história, estudo) → desejo (a moral da história) → ação (CTA direto ou indireto) | anúncio clássico: 06, 09 |
| I.H.C. | identificação ("isso é comigo") → história com conflito, virada e consequência → conteúdo (a ideia que fica) | depoimento: 04 |
| Jeito errado × jeito certo | conflito → tentativa errada → virada → jeito certo → mudança | reclamação que vira recomendação: 07 |
| Ele, eu, você e futuro | história de outra pessoa → como isso me tocou → trazer o público para dentro → o que pode acontecer com ele | depoimento com terceiro (10: a irmã neurologista) |
| Análise estratégica | o que todo mundo pensa → resultado impressionante → 3 motivos → moral da história | — |

## Elementos que prendem a atenção

Usar como checklist na análise da referência e na revisão do roteiro:

- **Relevância emocional**: o tema precisa fazer sentir algo já na primeira frase.
- **Linguagem familiar e imagem mental**: palavras do dia a dia que fazem a pessoa enxergar a cena. Na tradução, preferir a expressão cotidiana do país à tradução literal.
- **Tema e moral da história**: o tema chama atenção (um conflito que todos conhecem); a moral é a ideia que se quer vender.
- **Conflito e mudança**: sem conflito não há história; depois de cada conflito, algo muda.
- **Curiosidade e efeito "ahá"**: abrir uma pergunta e só responder depois. Sem resposta, a pessoa se sente enganada.
- **Contraste**: opostos lado a lado (antes × depois, amor × raiva) intensificam a emoção.

## Música

O quadro recomenda trilha escolhida pela emoção do vídeo e, quando possível, uma música que o público já conhece. Nossas montagens hoje saem só com a voz. Se a referência tiver música, registrar na análise; adicionar trilha é uma melhoria ainda não feita no `montar.py`.
