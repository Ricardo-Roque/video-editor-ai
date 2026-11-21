# Processo de criação de criativos

Este é o passo a passo para transformar um vídeo de referência num criativo novo, em outro idioma e país, usando IA para imagens e takes e montagem local.
O [Criativo 01](Criativos%20Exemplo/Lo-fi/Criativo%2001/) é o exemplo completo de todas as etapas. Os formatos de criativo são os do quadro do Trello "Formatos Criativos de Conteúdo", resumidos em [FORMATOS.md](FORMATOS.md). Os criativos entregues ficam em [Criativos Exemplo/](Criativos%20Exemplo/), separados por esses formatos, e cada formato tem um `FORMATO.md` (estrutura do anúncio, receita de produção, cuidados). O [CRIATIVOS.md](CRIATIVOS.md) lista todos, com custo e o que cada um ensinou. O [PRODUTOS.md](PRODUTOS.md) guarda os fatos confirmados de cada produto.

Regra geral: **nada avança sem aprovação**. Cada etapa termina com algo para validar, e a seguinte só começa depois do "ok".

## Visão geral

| Etapa | O que sai | Custo | Quem aprova |
|-------|-----------|-------|-------------|
| 0. Preparação | pasta do criativo, briefing, modelos no ar | 0 | — |
| 1. Análise da referência | `analise.md` (hook, body, CTA, cenas, imagens, estratégia visual, riscos) | 0 | dono do criativo |
| 2. Roteiro | `roteiro_<idioma>.md` traduzido e adaptado + `comparativo_roteiro.md` | 0 | dono, roteiro inteiro |
| 3. Imagens | personagens, depois cenas | ~US$ 0,04 por imagem | dono, imagem por imagem |
| 4. Teste de takes | 1 a 3 takes de teste | ~US$ 0,25 por take | dono |
| 5. Takes | todos os takes, um por vez (ou em lote, se liberado) | US$ 0,023/s (Omni 360p) ou 0,05/s (Veo 720p) | dono, take por take |
| 6. Montagem | vídeo final em `Vídeos Prontos/` | 0 (local) | dono, vídeo inteiro |

Custos reais: de US$ 0,70 (versão reaproveitando takes) a US$ 8,66 (3:59 de vídeo). Um criativo de 20 a 60 s costuma sair entre US$ 1,30 e 2,50. Detalhes em [CRIATIVOS.md](CRIATIVOS.md).

## Estrutura de pastas

```
Editor de Vídeo/
├─ README.md              instalação e primeiros passos
├─ PROCESSO.md            este documento
├─ FORMATOS.md            os 16 formatos do Trello, estruturas de roteiro e elementos que prendem
├─ CRIATIVOS.md           catálogo dos criativos e lições aprendidas
├─ PRODUTOS.md            fatos confirmados de cada produto
├─ CLAUDE.md              regras que o Claude segue em toda sessão
├─ .env                   chave do OpenRouter (cada pessoa tem a sua; nunca vai para o Git)
├─ Vídeo Bruto/           vídeos de referência que entram (fora do Git)
├─ Referências/           fotos do produto, logos
├─ Vídeos Prontos/        vídeos finais (fora do Git)
├─ assets/fonts/          fonte das legendas (Montserrat ExtraBold)
├─ tools/                 scripts de todas as etapas
├─ _Modelo Criativo/      modelos de arquivos para começar um criativo
├─ Criativos Exemplo/     uma pasta por formato do Trello (16), cada uma com o guia FORMATO.md
│  ├─ Lo-fi/          FORMATO.md + Criativo 01, 04, 06, 07, 08, 09, 10
│  ├─ Narrado/        FORMATO.md + Criativo 05, 11, 12
│  ├─ Palestrinha/    FORMATO.md + Criativo 13
│  └─ Tela dividida/, Cine/, Caixinha de perguntas/...   só o FORMATO.md (sem exemplo ainda)
└─ Criativo NN/           criativo em produção (vai para Criativos Exemplo/ ao ser entregue)
   ├─ referencia/         transcrição, cortes e frames da referência
   ├─ analise.md
   ├─ roteiro_fr.md       roteiro no idioma final (sufixo = idioma)
   ├─ comparativo_roteiro.md
   ├─ prompts_imagens.md
   ├─ imagens/personagens/   P1, P2...          (fora do Git)
   ├─ imagens/cenas/         H1, B1, O1...      (fora do Git)
   ├─ takes_config.json   imagens, personas, voz, modelo e resolução dos takes
   ├─ takes/              takes gerados + .words.json   (fora do Git)
   ├─ montagem.json       ordem dos clipes, legenda e overlays
   └─ montagem/           intermediários da montagem    (fora do Git)
```

Nomes usados em todos os criativos:
- **P1, P2...** personagens (folha de referência de rosto e roupa).
- **H1, H2...** cenas do hook. **B1, B1b, B1c...** cena base do body e variações. **O1, O2...** cards e overlays. Outras letras quando o formato pedir (ex.: Q = quadro/prancheta, F = fotos, C = cenas do quadro no 13), sempre explicadas no `analise.md`.
- **T01, T02...** takes, na ordem do roteiro. Take dividido vira **T10a / T10b**.
- Versões: `_v1`, `_v2`... **Nunca sobrescrever**; a aprovada é a que entra no config. Sufixo do take indica o modelo: `_360p_v1` (Omni), `_veo720_v1` (Veo), `_zoom_v1` / `_prancheta_v1` / `_quadro_v1` (feito localmente).
- Versão alternativa de um criativo (ex.: 07 Sono): arquivos com sufixo próprio (`roteiro_fr_sono.md`, `takes_config_sono.json`, `montagem_sono.json`), sem mexer nos da versão original.

## Como começar

1. Coloque o vídeo de referência em `Vídeo Bruto/`.
2. Abra o Claude Code na pasta do projeto e diga, por exemplo:
   > Novo criativo: Criativo 14, referência `Vídeo Bruto/<arquivo>.mp4`, francês, França, Cinnarae.
   Ou use `/novo-criativo`.
3. O Claude lê `CLAUDE.md`, este documento, `PRODUTOS.md` e `CRIATIVOS.md`, identifica o formato da referência, lê o `FORMATO.md` dele e segue as etapas, parando em cada aprovação.

O que o Claude pergunta se faltar: número do criativo, idioma, país, produto (e se a embalagem muda), se a copy é a mesma ou adaptada, e se o formato é o da referência ou outro (ex.: copy do 05 no formato "palestrinha").

---

## Etapa 0 — Preparação

1. Escolher o número: o próximo livre, contando a raiz e `Criativos Exemplo/` (não o número do arquivo de referência). Em equipe, avisar no grupo qual número vai usar antes de criar a pasta.
2. Criar `Criativo NN/` na raiz do projeto copiando `_Modelo Criativo/`. O criativo fica na raiz enquanto está em produção.
3. Conferir a chave no `.env` e o saldo no OpenRouter.
4. Conferir se os modelos estão no ar: `https://openrouter.ai/api/v1/models/google/gemini-omni-1.2-flash/endpoints` mostra a disponibilidade. O Omni 1.2 já ficou fora do ar por horas (2026-11-19); com ele fora, todo envio volta "Video generation failed" (sem cobrança).

## Etapa 1 — Análise da referência

```
python -I -X utf8 tools/analisar_referencia.py --video "Vídeo Bruto/<arquivo>.mp4" --out "Criativo NN/referencia" --language en
```

Gera transcrição com tempos, cortes de cena, folhas de frames e o frame de cada corte. Com isso, preencher `analise.md`:
- **Origem**: arquivo de referência na primeira linha (o nome do arquivo nem sempre bate com o número da pasta).
- **Hook, body e CTA** com tempos e o que acontece em cada um.
- **Cada cena**: cenário, enquadramento (tripé, selfie, POV, PiP), quem fala (em cena ou em off), overlays.
- **Estilo de edição**: legenda, B-roll, produto em cena, faixas fixas, música.
- **Formato**: dizer qual dos 16 formatos de [FORMATOS.md](FORMATOS.md) a referência segue e seguir o guia `Criativos Exemplo/<formato>/FORMATO.md` (receita, cuidados, exemplos quando houver). Se o guia diz que falta ferramenta, avisar antes de gastar.
- **Estrutura de roteiro, tema e moral da história** (ver [FORMATOS.md](FORMATOS.md)): AIDA, I.H.C., jeito errado × certo, ele-eu-você-futuro ou análise estratégica.
- **Roteiro anotado**: cada frase da referência, em português, com o elemento que segura a atenção nela entre colchetes ([Conflito + Curiosidade: ...]), pelo vocabulário de [FORMATOS.md](FORMATOS.md). É o mapa que a tradução precisa preservar.
- **Música**: se a referência tem trilha, registrar (hoje a montagem sai só com voz).
- **Estratégia para texto na tela** (ver tabela da Etapa 6): rótulo do produto, prancheta, quadro e faixas são deformados pelo modelo de vídeo. Decidir já aqui como cada um será feito, porque muda o modelo e o custo.
- **Imagens necessárias** e estimativa de takes e custo.
- **Pessoa da referência**: nunca copiar o rosto (pode ser pessoa real). Criar personagem nova com o mesmo visual (idade, roupa, cabelo, cenário).
- **Alertas de política**: antes/depois de corpo, depoimento fabricado, autoridade fictícia (médica, enfermeira, farmacêutica), alegações de saúde fora das permitidas no país, palavrão. O aviso é dado uma vez; a decisão é do dono e fica registrada no `analise.md`.
- **Perguntas abertas**: fatos do produto que a copy afirma e que não estão em [PRODUTOS.md](PRODUTOS.md) (ex.: onde é fabricado, "testado por terceiros"). Fato não confirmado sai do roteiro.

➡ **Aprovação:** o dono lê a análise e responde as perguntas abertas.

## Etapa 2 — Roteiro

1. Traduzir a transcrição para o idioma do país, **mesma ordem, sem cortar nem acrescentar**. Se a referência já está no idioma final, mudar só a marca.
2. Adaptar só o que não faz sentido no país (ex.: "American doctors" → "les médecins") e listar cada adaptação no topo do roteiro. Conferir frase a frase contra o roteiro anotado da análise: cada elemento (linguagem familiar, imagem mental, referência conhecida, contraste, curiosidade) precisa sobreviver. Gíria ou referência que só existe no país de origem vira o equivalente cotidiano do país de destino, não a tradução literal.
3. Quebrar em takes (`| Txx | imagem | segundos | fala |`), de 4 a 12 s, no máximo 15 s. Se o modelo escolhido tiver durações fixas (Veo: 4, 6 ou 8 s; Omni 1.1: 3 a 10 s), dividir em a/b numa pausa natural já no roteiro.
4. Marcar com ⚠ as falas de risco.
5. Cuidados que evitam refação:
   - Números por extenso quando a pronúncia importa ("120 000" → "cent vingt mille").
   - Evitar frases que o modelo bloqueia: "n'achetez pas" foi recusado ~15 vezes; "ne prenez surtout pas" passou.
   - Não incluir fato do produto que não esteja em [PRODUTOS.md](PRODUTOS.md).
6. Gerar `comparativo_roteiro.md`: original × tradução × tradução de volta para o português, com as diferenças explicadas. Assim quem não fala o idioma consegue validar.

➡ **Aprovação:** roteiro inteiro, incluindo os trechos ⚠.

## Etapa 2b — Roteiro novo a partir de um vencedor (quando pedido)

Quando o dono pede uma variação de um criativo que vendeu (outro hook, outro ângulo, copy nova em outro formato), em vez de traduzir uma referência:

1. Partir do roteiro anotado do vencedor (se não existir, anotar primeiro).
2. Propor 2 ou 3 ideias em poucas linhas, cada uma dizendo o tema novo, a estrutura e o formato. ➡ O dono escolhe.
3. Escrever o roteiro com o **mesmo esqueleto**: mesma estrutura, mesmos elementos nas mesmas posições, mesmo peso emocional, tema novo. Entregar anotado frase a frase e com a tradução de volta para o português.
4. Regras: número, estudo, pessoa real ou citação só com fonte verificável (link no roteiro); fato do produto só de [PRODUTOS.md](PRODUTOS.md); sem fonte, fica de fora. Seguir "Como escrever o roteiro" do `FORMATO.md` do formato escolhido.

Se a ideia é a mesma copy em outro formato (como o 13), a copy não muda: pular para a Etapa 3 com o guia do formato novo.

➡ **Aprovação:** roteiro inteiro, como na Etapa 2.

## Etapa 3 — Imagens

Ferramenta: Nano Banana via OpenRouter (`google/gemini-nano-banana-2.1`, ~US$ 0,04 por imagem, padrão do `gerar_imagem.py`).

1. Escrever os prompts em `prompts_imagens.md` (em inglês), já adaptados ao país: rua, interiores e embalagem locais, nenhuma bandeira de outro país.
2. **Personagens primeiro** (P1, P2...), fundo neutro:
   ```
   python -I -X utf8 tools/gerar_imagem.py --prompt "$(python -I -X utf8 tools/prompt_de.py "Criativo NN/prompts_imagens.md" P1)" --out "Criativo NN/imagens/personagens/P1_v1.png"
   ```
   ➡ **Aprovação dos personagens.**
3. **Cenas**, sempre com os aprovados como `--ref` (primeira ref = personagem principal; produto como ref quando aparece).
4. Gastar menos imagem:
   - **Editar em vez de gerar do zero**: o "depois" do antes/depois sai editando o "antes"; variações (gesto, posição da varinha, linha do quadro) saem editando a cena base.
   - **Gesto vai no prompt do take**, não numa imagem nova: no 06, uma única imagem serviu para todos os takes (personas `nurse_point`, `nurse_chest`...).
   - **Recorte local custa 0** (ex.: enquadrar do joelho para cima no 08).
   - **Reaproveitar** imagens entre takes e entre versões.
   - Cenário da referência sem a pessoa: cobrir a pessoa num frame da referência e passar como `--ref` só para o cenário (06, `sala_mascarada.png`).
5. Regras de conteúdo: produto sempre com a descrição de [PRODUTOS.md](PRODUTOS.md) (Cinnarae = "red raspberry gummy bears"); texto em outro idioma que o modelo inventar (ex.: "You Got This!" no quadro) deve ser apagado por edição.
6. Quando o dono manda uma foto de estilo ("nessa pegada"), criar personagem nova nesse estilo, sem copiar o rosto.
7. Se o dono preferir gerar as imagens na ferramenta dele, entregar os prompts em inglês prontos para colar, dizendo qual imagem anexar como ref.
8. Olhar cada imagem antes de mostrar e refazer o que saiu fora do pedido, avisando o motivo.

➡ **Aprovação:** imagem por imagem. Nada vira take sem aprovação.

## Etapa 4 — Teste de takes

Escolha do modelo:

| Modelo | Quando usar | Preço | Limites |
|--------|-------------|-------|---------|
| `google/gemini-omni-1.2-flash` 360x640 | **padrão**: talking head, voz em off, tudo sem texto pequeno em movimento | US$ 0,023/s | 3 a 15 s; deforma texto pequeno |
| `google/gemini-omni-1.1-flash` | Omni 1.2 fora do ar (mesmo prompt e seed) | ~US$ 0,034/s | só 3 a 10 s; falha mais (sem custo) |
| `google/veo-3.1-lite` 720x1280 | rótulo do produto em movimento (mão segurando o sachê), ou Omni fora do ar | US$ 0,05/s | só 4, 6 ou 8 s; fala rápido (~3,3–3,6 palavras/s); põe gente em cena se não for proibido |

Trocar de modelo muda o custo: pedir aprovação do dono antes. O modelo vai no `takes_config.json` (`"model"`) ou na variável `VIDEO_MODEL`. Para Veo, partir de `_Modelo Criativo/takes_config_veo.json`.

1. Montar `takes_config.json`: imagens aprovadas, persona de cada imagem (cena + voz), **seed fixa por persona** (mesma voz em todos os takes), `words_per_sec` do modelo (2,8 Omni; 3,3 Veo).
2. Voz em off: usar `"say": "The unseen off-screen narrator says:"` e escrever na cena que ninguém aparece (o padrão "She says:" faz o modelo pôr uma mulher falando).
3. Custo antes de gerar: `python -I -X utf8 tools/lote_takes.py --config "Criativo NN/takes_config.json" --from T01 --to T03 --dry-run`.
4. Gerar 1 a 3 takes de teste e conferir: voz, pronúncia (marca, números), sincronia labial, rosto, custo.
   ```
   python -I -X utf8 tools/checar_takes.py --config "Criativo NN/takes_config.json" --from T01 --to T03
   ```

➡ **Aprovação:** o dono assiste e decide se segue com essa configuração.

## Etapa 5 — Takes

A resolução final (1080x1920) é feita na montagem, sem custo. A duração de cada take vem das palavras (`words_per_sec` + `pad`), para não pagar silêncio.

- **Um take por vez**, com conferência e aprovação:
  ```
  python -I -X utf8 tools/lote_takes.py --config "Criativo NN/takes_config.json" --from T06 --to T06
  python -I -X utf8 tools/checar_takes.py --config "Criativo NN/takes_config.json" --from T06 --to T06
  ```
  `--only T08a,T08b` gera só alguns takes do intervalo.
- Lote liberado pelo dono ("pode seguir até o final"): no máximo 2 em paralelo (`--workers 2`, padrão) e em segundo plano. O OpenRouter recusa muitos vídeos ao mesmo tempo (recusa não é cobrada; o script espera e tenta de novo).
- Todo job enviado fica em `tools/jobs.log`. Se o processo cair: `python -I -X utf8 tools/gerar_take.py --resume <job_id> --out <arquivo>` (não paga de novo).
- "Video generation failed" não é cobrado: tentar de novo. Se falhar sempre com uma persona, tentar a persona base; se falhar sempre com uma frase, dividir o take para achar a frase e reescrever com o mesmo sentido.

Conferência (`checar_takes.py`) e frames: sinais e a correção mais barata.

| Sinal | Significado | Correção mais barata |
|-------|-------------|----------------------|
| `POSSIBLE CUT-OFF` | a fala acabou no limite do take | cortar numa pausa antes do trecho perdido (Ta) e gerar só o que faltou (Tb), a partir do último frame de Ta |
| `TEXT MISMATCH` por grafia | homófonos ("reposé/reposée", "Sinaré") ou número por extenso | nada: a pronúncia está certa |
| `TEXT MISMATCH`, palavra engolida | parte da fala sumiu | refazer só a frase (Ta/Tb) |
| frase inventada no fim | o modelo continua falando depois do roteiro (05 T08, 13 T01) | cortar numa pausa real depois da última palavra, arquivo novo `T08a_...` |
| frase repetida ou interjeição extra | "Profitez de l'offre" duas vezes, "Hein ?" | cortar na montagem (`text` do clipe termina antes; ou recorte Ta/Tb do mesmo take) |
| cenário muda no fim | o fundo deriva depois de ~4 s (Veo) | se a fala já acabou, o corte de silêncio da montagem resolve |
| pessoa aparece em cena de produto | Veo inventa apresentador | usar só a voz do take sobre a imagem (`prancheta_zoom.py`) |
| texto deformado (rótulo, quadro) | o modelo redesenha as letras | ver "Texto na tela" na Etapa 6 |
| rosto/roupa diferente | o modelo perdeu a referência | refazer com a mesma imagem e seed |

Toda divisão e correção vai em "Notas de produção" no fim do roteiro (o que foi cortado, em que segundo, qual arquivo entra na montagem e quanto custou).

➡ **Aprovação:** take por take (ou o lote todo, se liberado).

## Etapa 6 — Montagem

Tudo local, sem custo:
```
python -I -X utf8 tools/montar.py --config "Criativo NN/montagem.json"
```

O que o script faz:
1. Tempo de cada palavra (transcrição local, guardada em `.words.json`) alinhado ao texto do roteiro, para a legenda ter a grafia certa.
2. Corta o silêncio do começo e do fim de cada take e encurta pausas internas maiores que 0,3 s (jump cut).
3. Sobe para 1080x1920, 30 fps.
4. Legenda de 1 a 3 palavras, Montserrat ExtraBold branca com contorno, palavra-chave em amarelo-limão, a y=1420 (~74% da altura, acima da interface do Reels/TikTok).
5. Overlays nas palavras definidas.
6. Normaliza o áudio para redes sociais e exporta em `Vídeos Prontos/`.

Opções do `montagem.json`:

| Onde | Campo | Uso |
|------|-------|-----|
| raiz | `caption_y` | sobe a legenda quando algo fica na altura padrão (ex.: 1000 no 10, para não cobrir o sachê) |
| clipe | `take`, `file` | qual take e qual arquivo (versão aprovada) |
| clipe | `text` | texto da legenda quando difere do roteiro: corte de trecho (Ta/Tb), número junto ("3h", "70%", "1400€", `120\h000` com espaço que não quebra) |
| clipe | `"silent": true`, `start`, `end` | take sem fala (ação no hook, 08): entra inteiro, sem legenda |
| overlay | `image`, `clip_index`, `from_word`, `to_word` | card por cima, das palavras indicadas; `to_word` inexistente = até o fim do take |
| overlay | `width`, `aspect`, `x`, `y` | tamanho e posição (ex.: dois cards lado a lado de antes/depois, 07) |
| overlay | `"mode": "full"` | imagem em tela cheia (B-roll) |
| overlay | `"mode": "patch"`, `x`, `y` | PNG transparente fixo por cima do vídeo inteiro (rótulo nítido, faixas de oferta, texto do quadro) |

Para ajustar só legenda ou overlay sem refazer os segmentos: `--stage final`. Versões e cortes alternativos (ex.: hook A e hook B do 04) usam um `montagem_<nome>.json` próprio.

### Texto na tela

O modelo de vídeo redesenha letras pequenas, principalmente em 360p. Escolher a solução já na análise:

| Situação | Solução | Ferramenta | Exemplo |
|----------|---------|-----------|---------|
| produto parado, câmera fixa | colar o rótulo nítido da imagem aprovada por cima do take inteiro | `colar_produto.py` + overlay `patch` | 10 |
| prancheta / infográfico, sem pessoa falando | usar só a voz do take sobre a imagem nítida com zoom lento até o painel falado | `prancheta_zoom.py` | 05 |
| quadro atrás de apresentador, câmera fixa | trocar o texto do quadro pelo nítido, mantendo mãos e cabelo do take; ou patch da faixa de cima da imagem | `quadro_nitido.py` ou overlay `patch` | 13 |
| produto em movimento na mão | Veo 720p; se ainda deformar ou "flutuar", voz do take sobre a imagem com zoom | Veo + `prancheta_zoom.py` | 11, 12 |
| faixas fixas de oferta no topo | PNG local, nunca pelo modelo | `faixas_oferta.py` + overlay `patch` | 11, 12 |
| sequência de fotos (prova social) | fotos com zoom lento alternado, corte nas pausas | `prancheta_zoom.py` | 05 T07 |

### Conferência antes de entregar

Olhar frames do hook, dos cards e do body: legenda legível, nada cobrindo rosto ou boca (cards de 470 px cobriam a boca no 07; 380 px resolveu), rótulo nítido, sem palavra em outro idioma na tela.

➡ **Aprovação:** o dono assiste o vídeo inteiro e pede ajustes.

---

## Reaproveitamento

O jeito mais barato de fazer um criativo novo é reaproveitar o que já foi aprovado.

- **Nova versão de um criativo** (ex.: 07 Sono, sem alegação de emagrecimento): roteiro novo, takes antigos recortados em arquivos novos (`T03b_360p_v1.mp4`, nunca sobrescrevendo o original), só os takes que faltam são gerados. Custou US$ 0,70.
- **Vários hooks, mesmo body** (04): o body é gerado uma vez e entra em todos os cortes.
- **Copy vencedora em outro formato** (13, copy do 05): a copy é copiada sem mudança; só o formato muda.
- **Referência da concorrência no mesmo idioma** (11, 12): só a marca muda.

## Trabalho em equipe

- Cada pessoa usa a própria chave do OpenRouter no `.env` (nunca commitar). O limite de gasto é por chave.
- Antes de criar `Criativo NN/`, avisar o número no grupo para não haver duas pastas iguais.
- No Git vão só os textos (`.md`, `.json`) e as ferramentas. Imagens, takes e vídeos ficam na pasta compartilhada do time, na mesma estrutura de pastas.
- Ao entregar um criativo:
  1. Atualizar as "Notas de produção" do roteiro.
  2. Mover a pasta para `Criativos Exemplo/<formato>/` e trocar, no `montagem*.json`, os caminhos `../Vídeos Prontos/` e `../assets/` por `../../../Vídeos Prontos/` e `../../../assets/`. Primeiro criativo de um formato: acrescentar a tabela de exemplos e o que ele ensinou ao `FORMATO.md` da pasta.
  3. Acrescentar a linha dele em [CRIATIVOS.md](CRIATIVOS.md) (formato, custo, lições) e o que ele ensinou no `FORMATO.md`.
  4. Fato do produto confirmado vai em [PRODUTOS.md](PRODUTOS.md); ferramenta ou opção nova, neste arquivo.
  5. Commit e push dos textos.

## Regras que valem para todo criativo

- **Gastar o mínimo possível.** Informar o custo antes de gerar e o gasto real depois. Preferir 360p, durações justas, reaproveitar imagens e takes e corrigir só o pedaço com erro.
- **Aprovação em cada etapa.** Imagens antes de takes; takes antes da montagem.
- **Roteiro fiel.** Mesma copy da referência; qualquer diferença é listada e explicada.
- **Conferir antes de mostrar.** Transcrição de cada take comparada ao roteiro e frames olhados.
- **Política de anúncios.** Avisar os riscos antes de gastar; a decisão é do dono e fica registrada.
- **Nunca copiar o rosto de uma pessoa real.** Personagem nova com o mesmo visual.

## Problemas conhecidos e soluções

| Problema | Solução |
|----------|---------|
| `faster-whisper` falha ao abrir vídeo (erro do PyAV `metadata_errors`) | os scripts extraem o áudio com FFmpeg e passam o array; usar sempre os scripts de `tools/` |
| OpenRouter: `in-flight budget exhausted` | muitos vídeos ao mesmo tempo; `--workers 2` (o script espera e tenta de novo) |
| "Video generation failed" em todo envio | modelo fora do ar: ver disponibilidade em `/api/v1/models/<id>/endpoints`; trocar de modelo com aprovação |
| Comando passa de 10 min e o terminal mata | rodar lotes e montagem em segundo plano |
| Acento quebrado no Windows ou `UnicodeEncodeError` ao gravar log | rodar com `python -I -X utf8 ...` (`-I` ignora `PYTHONIOENCODING`) |
| Texto pequeno ilegível ou deformado no take | ver "Texto na tela" na Etapa 6 |
| Card cobrindo o rosto | o card fica entre o queixo e a legenda; diminuir `width` ou mudar `y` |
| Número e unidade em legendas separadas | campo `text` do clipe com "3h", "70%", "1400€" ou `\h` no lugar do espaço |

## Ferramentas (`tools/`)

| Script | Etapa | Função |
|--------|-------|--------|
| `analisar_referencia.py` | 1 | transcrição, cortes e folhas de frames da referência |
| `prompt_de.py` | 3 | lê o prompt de uma seção `## ID` de `prompts_imagens.md` |
| `gerar_imagem.py` | 3 | gera ou edita imagem com Nano Banana (aceita vários `--ref`) |
| `gerar_take.py` | 4–5 | gera um take a partir de uma imagem; `--resume` recupera job; `--no-audio` (o Omni 1.2 recusa com HTTP 400: gerar com áudio e descartar na montagem) |
| `lote_takes.py` | 4–5 | gera takes a partir do roteiro + `takes_config.json` (`--dry-run` mostra o custo; `--only`; `--workers`) |
| `checar_takes.py` | 4–5 | confere texto e corte de fala de cada take |
| `montar.py` | 6 | montagem final com legendas e overlays |
| `colar_produto.py` | 6 | recorte nítido da embalagem, alinhado e com a cor do take, para colar por cima (10) |
| `prancheta_zoom.py` | 5–6 | imagem nítida com zoom lento + voz do take, para cena com muito texto (05, 11, 12) |
| `quadro_nitido.py` | 5–6 | troca o texto redesenhado do quadro pelo nítido da imagem, mantendo mãos e cabelo do take (13) |
| `faixas_oferta.py` | 6 | faixas fixas de oferta em PNG transparente 1080x1920 (11, 12) |
