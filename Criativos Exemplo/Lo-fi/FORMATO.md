# Formato: Lo-fi

Formato 15 do quadro do Trello (ver [FORMATOS.md](../../FORMATOS.md)). Vídeo simples e "imperfeito" de propósito: uma pessoa fala para a câmera do celular, em selfie ou com o celular apoiado, como se falasse com uma amiga. O que prende é o tema (algo que todo mundo vive), a linguagem do dia a dia e a promessa de descobrir algo se ficar até o fim.

É o formato de 7 dos 11 criativos feitos até agora. Aparece em duas variações de ângulo:

- **Depoimento**: uma pessoa comum conta o próprio problema e como resolveu. A força está na identificação ("eu também acordo às 3h").
- **Autoridade**: uma profissional de saúde (enfermeira, farmacêutica, terapeuta) explica problema, mecanismo e solução. A credibilidade vem do jaleco, do cenário e do tom didático.

## Exemplos

| Criativo | Ângulo | Variação | Duração | Custo | Ver primeiro |
|----------|--------|----------|---------|-------|--------------|
| [C01](Criativo%2001/) | autoridade | hook de antes/depois do marido (formato Comparação) + senhora de medicina chinesa em selfie | 3:59 | US$ 8,66 | **exemplo completo de todas as etapas**; "depois" editando o "antes"; cards O1/O2; divisão Ta/Tb (T10, T27) |
| [C02](Criativo%2002/) | depoimento | sentada, câmera fixa, lista de sintomas; dois hooks com o mesmo body | 48,3 s + cortes de 21,9 e 26,5 s | US$ 1,30 | reaproveitar o body em vários hooks (`montagem_hookA.json`, `montagem_hookB.json`) |
| [C04](Criativo%2004/) | autoridade | enfermeira em pé no quarto de hospital, 5 dicas + CTA de advertorial | 114,9 s | US$ 4,42 | uma imagem só para todos os takes, gesto por persona; takes no Omni 1.1 (3 a 10 s) |
| [C05](Criativo%2005/) | depoimento | selfie na mão, "reclamação falsa" que vira recomendação, cards de antes/depois | 73,5 s (+ versão Sono 71,0 s) | US$ 2,31 (+ 0,70) | cards lado a lado (`width`/`x`/`y`) e versão nova reaproveitando takes (`roteiro_fr_sono.md`) |
| [C06](Criativo%2006/) | depoimento | senhora de 72 anos levanta do chão sozinha e fala (gancho visual) | 13,4 s | US$ 2,40 (08+09+10) | hook de ação sem fala (`"silent": true`) |
| [C07](Criativo%2007/) | autoridade | farmacêutica em selfie na frente das prateleiras | 13,0 s | (no lote do 06) | formato curto: dado → recomendação → benefício → CTA |
| [C08](Criativo%2008/) | depoimento | sentada no balcão da cozinha, sachê parado em cena o vídeo todo | 47,8 s | (no lote do 06) | rótulo nítido colado por cima (`colar_produto.py`, overlay `patch`, `caption_y`) |

## Estrutura típica

| Bloco | Depoimento | Autoridade |
|-------|------------|------------|
| Hook (0–6 s) | sintoma ou situação concreta em primeira pessoa; às vezes uma ação física (08) ou uma reclamação (07) | dado chocante ou sintoma visível ("70% das pessoas...", "se o seu peito está assim...") |
| Prova / apresentação | resultado mostrado: antes/depois (07), a própria ação (08) | quem é e por que sabe disso ("enfermeira e mãe de dois", 06) |
| Body | o que descobriu, como usa, o que mudou semana a semana (10) | mecanismo (cortisol, falta de magnésio) e dicas ou diferenciação do produto (01, 06) |
| CTA | curto: link, oferta ou escassez (07); o 02 não tem CTA | link, muitas vezes para um advertorial (06) |

Estruturas de roteiro do Trello que aparecem aqui: **Jeito Errado × Jeito Certo** (07: reclamava, descobriu, mudou), **I.H.C.** (04, 10: identificação pelo sintoma, história, conteúdo) e **AIDA** (06, 09).

## Como escrever o roteiro

Quando a copy não vem pronta da referência (roteiro novo ou variação de hook):
- Primeira frase é uma **tese que incomoda** ou um sintoma concreto em primeira pessoa; quem vive aquilo precisa pensar "é comigo".
- Tom de **amiga jogando a real**: expressões do dia a dia do país, nada de termo técnico sem tradução na mesma frase.
- Falar em voz alta a objeção de quem assiste ("talvez você pense...") e responder.
- Um efeito a-há no meio (a causa que a pessoa não conhecia) e a moral curta no fim, antes do CTA.
- Autoridade: termo técnico sempre traduzido ("o cortisol, o hormônio do estresse"); lista que empilha sintomas do invisível ao que se vê no espelho.

## Receita de produção

- **Personagem**: pessoa nova com o visual da referência (idade, cabelo, roupa, cenário). Nunca copiar o rosto, nem quando pedirem "a mesma modelo" (pode ser pessoa real). Se o dono mandar uma foto de estilo, seguir o estilo (o 02 virou uma avó francesa numa cozinha rústica).
- **Cenário**: para usar o cenário da referência sem a pessoa, cobrir a pessoa num frame e passar como `--ref` (06, `sala_mascarada.png`). Apagar textos em outro idioma que o modelo inventar (o "You Got This!" do 04).
- **Imagens**: P1 + uma cena base (B1). O 04 usou uma única imagem para 16 takes; os gestos (apontar, mão no peito) vão nas personas do `takes_config.json`, com a mesma seed e voz.
- **Takes**: Omni 1.2 Flash 360p. Selfie: "Handheld front-camera selfie video, slight natural shake". Câmera fixa: "phone on a tripod, static framing".
- **Montagem**: legenda padrão (y=1420). Card ou produto na altura da legenda: subir com `caption_y` ou diminuir o card (no 05, 470 px cobria a boca; 380 px em y=985 resolveu). Cards de imagem (O1, O2) entre o queixo e a legenda (01).

## Cuidados

- **Política**: depoimento é fabricado (personagem de IA) e autoridade é fictícia; antes/depois de corpo e alegação de emagrecimento ou de saúde são o maior risco. Avisar uma vez na análise.
- Fatos do produto que a copy afirma ("fabriqué en France", "testado por terceiros") só entram se estiverem em [PRODUTOS.md](../../PRODUTOS.md). No 04, "fabriqué en France" saiu.
- Frases que o modelo bloqueia: "n'achetez pas" falhou cerca de 15 vezes; "ne prenez surtout pas" passou com o mesmo sentido (06).
- O modelo às vezes acrescenta interjeição ("Hein ?") ou repete frase: cortar na montagem, sem gerar de novo (07).
- Hook sem fala: take curto (3 s) com `"silent": true`; o corte seco para a fala esconde a troca (08).
- Produto parado em cena: o modelo deforma o rótulo em todos os takes; planejar o `colar_produto.py` já na análise (10).
- O francês falado sai mais longo que o inglês (87 s viraram 114,9 s no 04). Prever no custo.
- Valores juntos na legenda: "1400€", "70%", "3h" no campo `text` (06, 09, 10).
