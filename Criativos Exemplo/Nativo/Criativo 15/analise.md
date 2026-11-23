# Análise — Criativo 15

Fonte: anúncio da Biblioteca de Anúncios da Meta, ID 29332992999645403 (https://www.facebook.com/ads/library/?id=29332992999645403). Não é vídeo: é um **anúncio nativo estático** (uma foto + texto longo no post + link para um advertorial).
Texto completo em francês: `referencia/texto_anuncio_fr.txt`. Imagem: `referencia/imagem_anuncio.png` (483x600, 4:5).
Anunciante: **Elmora** (concorrente da Cinnarae, ver `PRODUTOS.md`), postando pela página "Communauté Bien-être & Santé". No ar desde 2026-11-09, ativo em 2026-11-21, Facebook + Instagram + Audience Network + Messenger.
Link: `elmora.fr/pages/top-magnesium-homme` (advertorial voltado a **homens**). Título do link: "J'ai fait ça pour réparer mon sommeil après 26 ans" ("Fiz isto para consertar meu sono depois de 26 anos"). Botão: "Saiba mais".

Pedido do dono: modelar o anúncio. Fazer uma imagem parecida (pessoa nova, mesmo visual) e **alterar um pouco a história**, mantendo o mesmo impacto e a mesma intenção de venda. Por isso o texto segue a Etapa 2b do `PROCESSO.md` (mesmo esqueleto, história nova), não uma tradução.

Premissas a confirmar: produto Cinnarae, país França, texto em francês (a referência já está em francês), tratamento "vous" quando fala com o leitor.

## Formato e estrutura

- **Formato criativo**: nenhum dos 16 do Trello, que são todos de vídeo. É o **anúncio nativo de história** ("long-form story ad"): parece post pessoal de um homem comum, sem cara de anúncio, com uma selfie amadora. A imagem segue a lógica do [Lo-fi](../../Lo-fi/FORMATO.md), ângulo **depoimento** (selfie imperfeita, pessoa comum, identificação). Ao entregar, decidir com o dono se cria a pasta `Criativos Exemplo/Nativo/` (primeiro criativo estático).
- **Fluxo de produção** (adaptado, sem takes nem montagem): análise → texto (Etapa 2b) → imagem → entrega (imagem 4:5 + texto + título do link). Custo só da imagem.
- **Estrutura de roteiro**: **Ele, eu, você e futuro** com **jeito errado × jeito certo** dentro:
  hook com promessa de segredo → quem eu sou e a dor do ofício → tudo que tentei (jeito errado) → o jovem que aguenta mais (ele) → zombo dele → a morte do amigo (consequência extrema) → noite de crise, pesquisa, mecanismo (a-há) → compro (jeito certo) → evolução por noites e semanas → os outros notam → espalho para os colegas → médico confirma → moral ("não é coisa de caminhoneiro") → você ("se for você, ou o homem que dorme ao seu lado") → link.
- **Tema**: o desgaste invisível de 20 anos de trabalho pesado e noites quebradas, contado por um homem duro que nunca admitiria. **Moral**: "não é a idade nem o ofício; o estresse queima o magnésio, e o que tem na prateleira o corpo não absorve".
- **Música**: não se aplica (estático).

## A imagem

| Item | Referência | O que prende |
|------|-----------|--------------|
| Pessoa | homem de ~55 anos, bigode grisalho, barba por fazer, boné escuro, camiseta preta, cara de cansado, sem sorrir | [Identificação + Gancho visual: o público-alvo se vê; o cansaço está no rosto, combina com a história] |
| Enquadramento | selfie com o braço esticado (o braço aparece no canto direito), de baixo para cima, 4:5 | [Linguagem familiar visual: foto amadora de celular, não parece anúncio] |
| Cenário | cabine de caminhão (teto cinza, cortina preta da cama atrás do banco), janela com área de serviço de autoestrada, cobertura verde de posto, carretas brancas estacionadas, céu nublado claro | [Imagem mental: ancora o ofício antes de ler a primeira linha] |
| Produto | não aparece | [público frio: não mostrar o produto logo de cara (COPY.md, seção 3)] |
| Texto na imagem | nenhum | — |

Para o nosso: homem novo com o mesmo visual (nunca o rosto da referência), mesma pose de selfie, mesmo cenário, sem logos legíveis (posto, caminhão), céu de França. Não passar a imagem da referência como `--ref` (o modelo copiaria o rosto); descrever no prompt.

## Roteiro anotado

O texto tem cerca de 2.100 palavras em ~180 linhas curtas. A anotação vai por bloco (cada bloco tem a mesma função e os mesmos elementos), em português.

| # | Bloco (resumo em PT) | Elementos |
|---|----------------------|-----------|
| 1 | "Há 26 anos dirijo caminhão. No outono passado, um jovem com quem fiz dupla numa viagem longa pela Europa trouxe para a minha cabine uma coisa em que não paro de pensar." | [Familiaridade + Curiosidade: seleciona o público (homem de ofício pesado) e abre "que coisa?" sem responder] |
| 2 | "Não estou exagerando. Quase o expulsei do caminhão rindo na cara dele quando me disse o que era. Agora não faço mais nenhuma carga sem." | [Contraste + Curiosidade: zombou → não vive sem; promessa de virada] |
| 3 | "Vou começar do início." | [Ritmo: pausa, sinal de história longa] |
| 4 | Dias de 11 h que viram 14 nas docas; noites na cama da cabine com o motor do frigorífico gritando ao lado; entregas às 3 h da manhã; "sabe aquelas carretas no estacionamento do Carrefour à 1 h? Sou eu dormindo." | [Imagem mental + Familiaridade + Linguagem familiar: detalhes concretos e o Carrefour que todo francês conhece] |
| 5 | "Duas semanas fora, três dias em casa. A gente assina para isso. O que não assina é o que isso faz com o corpo depois de vinte anos. Ninguém fala disso." | [Conflito universal + Contraste: o preço escondido do trabalho] |
| 6 | "Tenho 52 anos. Costas destruídas pelo banco. Joelhos estalando como torrada. Anos sem uma noite inteira de sono." | [Identificação + Imagem mental: lista do corpo, do que dói ao invisível] |
| 7 | "Depois de vinte anos acordado pelos horários, o sistema nervoso nunca desliga de verdade. Nem em casa, na minha cama." | [Mecanismo leigo + Conflito: semente do a-há (o corpo não desliga)] |
| 8 | A esposa conta que fica acordada ouvindo ele ranger os dentes, e que às vezes ele para de respirar e ela põe a mão no peito dele para conferir. "Eu não fazia ideia." | [Relevância emocional (medo) + Identificação da esposa: segundo público, a mulher que lê] |
| 9 | Tentei de tudo: melatonina, sonífero que me deixava zonzo até Valence, cortar café e cerveja, cobertor pesado que a filha deu no Natal. Uma coisa funcionava uma semana. | [Jeito errado + Familiaridade: todas as tentativas que o leitor já fez; fecha a saída "já tentei"] |
| 10 | Volta às 3 h da manhã, coração disparado sem motivo, repassando a viagem do dia seguinte. "Achava que era o ofício." | [Imagem mental + Identificação: o sintoma-chave (acordar às 3 h com o coração batendo)] |
| 11 | "Aprenderia do jeito difícil em novembro, e isso custaria tudo a um amigo." | [Curiosidade + Relevância emocional: promessa de tragédia; segura até o bloco 17] |
| 12 | A empresa o põe em dupla com Kévin, 27 anos, discreto, cuja mãe foi enfermeira 25 anos. "Kévin aguenta mais que todo mundo." | [Personagem + Curiosidade: o "ele" da estrutura; a mãe enfermeira prepara a credibilidade] |
| 13 | Sequência de outubro: Lyon-Toulouse pela A75 na nevasca, descarga às 4 h com 5 horas de espera, volta direto para outra carga. Ele mal tira as botas; Kévin faz 10 horas sem erro e ainda o chama para tomar café. | [Contraste + Imagem mental: mesmo trabalho, recuperação oposta; rotas reais dão verdade] |
| 14 | "Achei que era a idade. 27 contra 52." Mas: Kévin dorme 5 h num caminhão em movimento e acorda como se fossem 8; ele dorme 8 em casa e acorda "arrastado atrás da carreta". | [Debate mental + Contraste: derruba a desculpa da idade] |
| 15 | Num restaurante de estrada perto de Montauban, Kévin tira um saquinho da geladeira portátil. "Que porcaria é essa, bala?" "Gomas de magnésio. Minha mãe que me indicou." | [Efeito a-há parcial + Humor: revela o "que coisa" do bloco 1; o produto entra como coisa boba] |
| 16 | "Eu já tinha tentado magnésio, não fez nada." Kévin: "A forma importa. A maior parte do que tem na prateleira o corpo nem absorve. Atravessa direto. O meu funciona. Durmo a noite toda em qualquer cama." Ele zomba; os colegas no rádio PX tiram sarro "do novato e das gomas da mamãe". | [Objeção respondida + Mecanismo único (forma) + Ridículo: a objeção "magnésio não funciona" é dita pelo próprio narrador] |
| 17 | Didier, 19 anos de estrada, dois filhos, treinador do time de futebol do filho. Mesmo problema. Saiu da estrada na A20 perto de Limoges às 4h40, reta, noite limpa, sem marca de freio. "Provavelmente nem acordou." Ele carregou o caixão. | [Consequência extrema + Relevância emocional: fecha a promessa do bloco 11; uma pessoa com nome, não estatística] |
| 18 | Carregando o caixão, lembra que uma semana antes saiu para o acostamento às 4 h. "Quase fui eu." O filho de Didier pergunta se o caminhão do pai vai voltar para casa. Ninguém disse "cansaço", todos pensavam. | [Identificação + Medo de perder a vida: o leitor se põe no lugar] |
| 19 | Uma semana depois, na cama da cabine, peito apertado, mandíbula travada; um metro abaixo, Kévin dorme pesado. "Ele recupera. Eu enferrujo." "O que um garoto de 27 anos tem que eu não tenho?" | [Contraste + Curiosidade: a pergunta que move o leitor também] |
| 20 | Pesquisa no celular: "por que acordo às 3 h com o coração disparado". Uma hora de fóruns e estudos. "Sempre voltava a uma coisa: o estresse queima o magnésio." | [Efeito a-há: a causa que ninguém contou] |
| 21 | Sem magnésio, o hormônio do estresse não baixa à noite; o magnésio é o botão de desligar; "o corpo fica acelerado a noite toda, em ponto morto, como um caminhão que não dá para desligar". "O corpo não está quebrado. Está sem combustível." | [Mecanismo + Analogia do ofício: explicação em linguagem de caminhoneiro; tira a culpa] |
| 22 | Por que o magnésio antigo não funcionou: forma que o corpo não absorve; "como encher o tanque com a tampa ainda presa no gargalo. A bomba gira. O ponteiro não mexe." | [Mecanismo único + Analogia: fecha a objeção do bloco 16] |
| 23 | No dia seguinte pergunta a Kévin. Kévin põe o saquinho no balcão: "É o que o centro do sono fez todo o setor da minha mãe tomar. Enfermeiras de 30 anos de plantão noturno. Tem em toda mesa de cabeceira." Compra pelo celular antes da torrada chegar. **Nome da marca aqui.** Custou menos que a melatonina e o sonífero da última semana. | [Credibilidade (autoridade + prova social) + Proposta fácil: preço baixo, compra imediata] |
| 24 | "Me senti bobo. 26 anos e 5 milhões de km comprando gomas porque um novato mandou." Toma duas antes de dormir, não conta a ninguém. | [Identificação + Humor: autoironia, deixa o leitor à vontade para comprar] |
| 25 | Primeira noite: dorme em 10 minutos, 7 horas seguidas, acorda antes do despertador; mandíbula solta, costas sem dor. Noite seguinte igual; quarta noite dorme em minutos; segunda semana acabam os despertares das 3 h; fim do primeiro mês "a estrada parou de me seguir na cama". | [Mudança + Intensificação em cenas: evolução noite a noite, cada volta com detalhe novo] |
| 26 | O humor melhora; a filha diz que ele "voltou a falar como ele mesmo"; Kévin sorri no cais de Fos-sur-Mer: "Encomendou, né? Eu disse." O chefe de 11 anos: "Você parece 10 anos mais novo." | [Prova social + Mudança vista pelos outros] |
| 27 | Conta para o amigo Alain (23 anos de estrada, dois divórcios), que zomba e uma semana depois pede o link. Em dois meses, oito motoristas do depósito tomam todas as noites. "Brutamontes de bife e cerveja jurando pelas gominhas." Costas, quadril, pressão melhoram. | [Prova social + Humor + Contraste: o cético convertido] |
| 28 | Exame médico da carteira de caminhão: pressão mais baixa, cortisol normal pela primeira vez em 9 anos. O médico não ri: a maioria dos pacientes tem falta sem saber, e "não é coisa de caminhoneiro, é qualquer homem sob pressão por tempo suficiente: policial, enfermeiro, quem faz 60 h no escritório com três filhos". | [Credibilidade (autoridade) + Ampliação do público: abre para todo homem estressado] |
| 29 | "Perdemos gente demais, cedo demais. Infarto aos 52. E caras como Didier." O caminhão de Didier ficou 3 semanas no pátio; ele estaciona ao lado da vaga vazia. "É por ele que escrevo isto." | [Relevância emocional + Motivo para contar: justifica o post sem parecer venda] |
| 30 | "Não digo que uma goma resolve este ofício." Mas aos 52 se sente melhor que aos 40, dorme a noite toda. Três saquinhos: um no caminhão, um na cabeceira, um de reserva. | [Credibilidade (admite limite) + Benefício positivo como imagem final] |
| 31 | "Não precisa dirigir caminhão para ser o seu problema. Piloto, socorrista, trabalhador de turno. Se for você, ou o homem que dorme ao seu lado, leia o artigo no link." | [CTA indireto + Identificação ampliada: fala com a esposa também] |
| 32 | "A marca exata está lá. Garanta que é a verdadeira. As cópias não funcionam." + link | [CTA + Urgência/escassez de autenticidade: bloqueia a busca pelo genérico] |

O texto novo precisa manter cada um desses elementos no mesmo bloco e na mesma ordem.

## Diagnóstico de copy (COPY.md, seção 2)

- **Nível de consciência**: consciente do problema, beirando inconsciente. Ele sente o cansaço, mas acha que "é o ofício" ou "é a idade" (o texto diz isso duas vezes e depois derruba).
- **Sofisticação do mercado**: 4 a 5 (magnésio e sono na França). Vende por **identificação** (o ofício, o homem duro) e **mecanismo** (o estresse queima o magnésio; a forma importa), nunca por promessa maior.
- **Tipo de lead**: **história** (o mais indireto). Só a palavra "magnésio" aparece no bloco 15, depois de ~40% do texto.
- **Crença única**: "Recuperar o sono e a energia depois de anos de pressão não é questão de idade nem de força; é repor o magnésio que o estresse queima, numa forma que o corpo realmente absorve."
- **Regra do Um**: uma história (o caminhoneiro), uma emoção (medo de acabar como Didier → alívio), um benefício (dormir a noite toda e recuperar), uma ação (ler o artigo).
- **4 pés**: ideia forte, promessa forte, prova anedótica (colegas, chefe, médico), credibilidade construída pelo detalhe (rotas, docas, Carrefour) e pela autoironia. O pé mais fraco é a **prova**: tudo é relato; nada verificável.
- **Perguntas de Evaldo respondidas, na ordem**: quem é o culpado (o ofício, depois o estresse) → o que me impede (já tentei de tudo) → por que agora (Didier) → como funciona (estresse queima magnésio + forma) → como sei que é real (colegas, médico) → o que ganho (dormir, humor) → como começo (link).
- **Nota de Bencivenga**: problema 25 (urgente: dormir ao volante) + promessa 15 + prova 15 + proposta 25 (só "leia o artigo", fácil de aceitar) + 20 (o mecanismo vale mesmo para quem não compra) = **100, A+**.
- **Mecanismo único**: "a forma importa: a maior parte do magnésio de prateleira o corpo não absorve". A Elmora não nomeia a forma no post. A Cinnarae é bisglicinato (`PRODUTOS.md`), então pode nomear, **se** a afirmação de absorção for confirmada (ver perguntas).

## Ideias para a história nova (Etapa 2b, passo 2)

Mesmo esqueleto dos 32 blocos, mesma duração (~2.000 palavras), mesmos elementos. Muda o personagem, os detalhes e os nomes. Escolha uma:

1. **Mesmo ofício, outra história (recomendada)**. Caminhoneiro de 54 anos, 28 de estrada, frigorífico para Rungis. O jovem é outro (ex.: "Yanis", 26 anos, mãe aide-soignante de noite numa clínica), as rotas e as cenas mudam (A7 no mistral, fila no porto de Calais, aire em Bourgogne), as tentativas mudam (chá de tília, aplicativo de meditação, tampões de ouvido). O amigo que morre vira outro nome e outro trecho. É a menor mudança e a que mais preserva o que já está vendendo. Imagem: selfie na cabine numa aire, como a referência.
2. **Padeiro**. 56 anos, 32 anos acordando às 2 h no fournil. O aprendiz de 22 anos aguenta tudo (mãe enfermeira de noite). O amigo padeiro dormiu ao volante voltando da feira às 5 h. A analogia do mecanismo vira "como um forno que não desliga" e "fermento que não cresce". Imagem: selfie no fournil, avental de farinha, madrugada. Muito francês e reconhecível, mas muda mais.
3. **Operário em 3x8**. 53 anos, 25 anos alternando turnos numa fábrica. O colega jovem do turno da noite aguenta tudo. O amigo saiu da estrada voltando do turno da noite. Imagem: selfie no carro, colete refletivo, estacionamento da fábrica ao amanhecer. Público mais amplo (turnos), menos imagem forte que o caminhão.

Nas três, a morte do amigo pode ficar (é o pico emocional da referência) ou virar um quase acidente que ele sobrevive (menos pesado, menos impacto). Recomendo manter, como na referência, salvo decisão do dono.

## Texto na tela e solução

Nenhum texto na imagem. Logos de posto e de caminhão devem sair ilegíveis ou sem marca (pedir no prompt e conferir).

## Imagens necessárias e custo

- **Uma imagem só**, 4:5 (`--aspect 4:5`), gerada direto como cena (sem folha de personagem P1: não há outra imagem que precise manter o rosto). Nome: `imagens/B1_v1.png`.
- Custo estimado: US$ 0,04 por tentativa; até 3 tentativas = **até US$ 0,12**.
- Takes e montagem: não há. Custo do texto: 0.

## Política de anúncios (aviso único)

Riscos da referência que passam para o nosso se o texto for mantido no mesmo tom:
- **Depoimento fabricado**: o post se apresenta como relato real de um caminhoneiro, e a foto seria de uma pessoa gerada por IA. A Meta pode tratar como enganoso; o `COPY.md` pede persona de IA nunca apresentada como cliente real.
- **Autoridade fictícia**: "o centro do sono fez todo o setor tomar" e "o médico disse que a maioria dos pacientes tem falta".
- **Alegações de saúde fora das permitidas na UE** (regulamento 1924/2006): para o magnésio, a UE só autoriza frases como "contribui para reduzir o cansaço e a fadiga", "para o funcionamento normal do sistema nervoso", "para funções psicológicas normais" e "para a função muscular normal". O texto afirma: consertar o sono (título do link), parar de respirar à noite (apneia), cortisol de volta ao normal, pressão mais baixa, menos infarto, melhora de costas e quadril, dormir 7 horas já na primeira noite.
- **Medo**: morte do amigo ao volante e "infarto aos 52".
- **Página**: a Elmora posta como "Communauté Bien-être & Santé", uma página que não parece a marca.

A decisão é do dono e fica registrada aqui: manter fiel (como nos criativos 05 e 07) ou suavizar as alegações de saúde.

Decisão do dono (2026-11-21): respondeu "pode seguir com a criação" sem escolher. O texto seguiu o tom da referência (padrão dos criativos 05 e 07), com as frases de risco marcadas ⚠ e uma alternativa suave para cada uma em `roteiro_fr.md`. A confirmar na aprovação do texto.

## Perguntas abertas

1. Produto **Cinnarae**, **França**, **francês**? A referência fala com homens (página "top magnésium homme"); a Cinnarae tem página ou advertorial para homens, ou qual link vai no anúncio?
2. Qual das 3 ideias de história (ou outra)? Manter a morte do amigo?
3. Podemos dizer que o bisglicinato da Cinnarae **é melhor absorvido** que o magnésio comum de prateleira? Não está em `PRODUTOS.md`. Sem confirmação, o texto diz só "a forma importa" sem comparar.
4. **Dose**: o personagem toma "duas gomas antes de dormir". Qual é a dose da Cinnarae no rótulo?
5. **Preço**: "custou menos que a melatonina da última semana". Sem o preço confirmado, a frase sai ou vira algo sem número.
6. Nome da página que publica e título do link: seguir o modelo da referência ("J'ai fait ça pour réparer mon sommeil après 26 ans") ou outro?
7. Política: manter as alegações como na referência ou suavizar?
