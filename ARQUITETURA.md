# Arquitetura: core, ofertas e fontes de referência

> **Status: proposta (2026-11-24).** Nada daqui foi implementado ainda. As decisões em aberto estão no fim. Depois de aprovado, este documento vira a referência para a migração, para o bot de mineração e para a interface gráfica.

## O problema

Hoje tudo mora na mesma pasta e no mesmo repositório (público): o método (PROCESSO, MODELAGEM, FORMATOS, Copy), as ferramentas, os fatos do produto (PRODUTOS.md), a biblioteca de variáveis, as quebras e os criativos entregues. Com uma oferta (Cinnarae) e uma concorrente (Elmora) isso funciona. Com várias ofertas, vários produtos e várias bibliotecas de referência, aparecem quatro problemas:

1. **Mistura de camadas.** O método é igual para qualquer oferta; os dados da oferta não. Hoje um arquivo como `PRODUTOS.md` mistura fatos de produto, oferta comercial, padrões de criativo e números de negócio.
2. **Contexto da oferta incompleto.** O processo começa pela referência. Não há um passo obrigatório que garanta que o sistema conhece a página de venda, a pre-sell, o funil e a oferta atual antes de escrever uma linha. Resultado possível: criativo bom, mas incongruente com a página para onde ele manda.
3. **Referências entram no projeto.** Vídeos vão para `Vídeo Bruto/`, imagens de anúncio vão para `referencia/` de cada criativo. Com várias bibliotecas (pastas do time, Drive, bot de mineração), copiar tudo para dentro duplica arquivos e perde a origem.
4. **Retrabalho.** Não há como perguntar "esse anúncio já foi analisado?". A identificação está espalhada (número do criativo, número do Drive, nome do arquivo de referência, ID da Biblioteca de Anúncios) e algumas numerações já colidiram (referências #08/#09 viraram criativos 11/12).

Além disso, o repositório é público: preços, URL da loja, concorrente, resultados de teste e copy dos criativos estão expostos.

## A proposta em uma frase

**Um core que só tem método e ferramentas, um espaço de trabalho por oferta com os dados do negócio, e fontes de referência que o sistema só lê, ligadas por um registro com IDs estáveis.**

```
┌──────────────────────────── CORE (repo público) ────────────────────────────┐
│ método: PROCESSO, MODELAGEM, FORMATOS, Copy/, FORMATO.md de cada formato     │
│ ferramentas: tools/, skills, modelos (_Modelo Criativo/)                     │
│ regras: CLAUDE.md                                                            │
│ NÃO contém: produto, preço, URL, concorrente, resultado, copy de criativo    │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ lê e escreve
┌───────────────▼──────────── ESPAÇO DA OFERTA (privado) ──────────────────────┐
│ marca.md · ofertas/<id>/oferta.md · funil (páginas capturadas com data)      │
│ variaveis.md · quebras/ · criativos/ · testes · resultados                   │
│ registro (índice de tudo que já foi visto, quebrado, modelado, entregue)     │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ só lê (nunca copia, nunca escreve)
┌───────────────▼──────────── FONTES DE REFERÊNCIA ────────────────────────────┐
│ pastas do time · pasta no Drive · saída do bot de mineração · Ad Library     │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Camada 1: core

O que é igual para qualquer oferta e qualquer pessoa do time.

| Fica no core | Sai do core |
|---|---|
| `PROCESSO.md`, `MODELAGEM.md`, `FORMATOS.md`, `Copy/` | `PRODUTOS.md` (vira `marca.md` + `oferta.md`) |
| `Criativos Exemplo/<formato>/FORMATO.md` (guia do formato, lições genéricas) | os criativos entregues em si (vão para o espaço da oferta) |
| `tools/`, `.claude/skills/`, `_Modelo Criativo/`, `assets/` | `Variáveis/<Marca>.md`, `Quebras/<Marca>/` |
| `CLAUDE.md` (regras do processo) | `CRIATIVOS.md` (catálogo passa a ser por oferta, gerado pelo registro) |

O core descobre onde estão os dados por configuração local, como já faz com a chave:

```
# .env (cada pessoa, fora do Git)
OPENROUTER_API_KEY=...
DADOS_DIR=C:\...\Ofertas            # raiz dos espaços de oferta
FONTES_DIR=C:\...\Bibliotecas        # opcional: raiz das bibliotecas locais
```

As lições de formato que hoje citam a Cinnarae continuam no `FORMATO.md`, escritas de forma genérica ("narradora em off + prancheta fez a primeira venda"), com o link para o criativo pelo ID, não pelo caminho.

## Camada 2: espaço da oferta

### Marca, produto, oferta

- **Marca**: quem vende (Cinnarae). Tem tom, padrões visuais, o que nunca dizer, concorrentes conhecidos e a biblioteca de variáveis.
- **Produto**: o que se vende (gomas de bisglicinato de magnésio, ursinhos vermelhos, sachê).
- **Oferta**: produto + mercado + funil + preço num período. A mesma marca pode ter várias ofertas (FR com -20%, FR Black Friday, DE no futuro). **A oferta é a unidade de trabalho**: todo criativo, quebra de Modelagem e teste pertence a uma oferta.

### Estrutura

```
<DADOS_DIR>/
└─ cinnarae/
   ├─ marca.md                     tom, padrões de criativo, proibições, concorrentes, prefixo de IDs (CIN)
   ├─ produtos/
   │  └─ gomas-magnesio.md         fatos confirmados com data (o que hoje está no PRODUTOS.md)
   ├─ ofertas/
   │  └─ CIN-FR-01/
   │     ├─ oferta.md              briefing da oferta (campos abaixo)
   │     └─ funil/
   │        ├─ presell_2026-11-22.md   texto capturado da pre-sell, com URL e data
   │        └─ pdp_2026-11-22.md       texto capturado da página de produto
   ├─ variaveis.md                 biblioteca de variáveis (formato fixo de hoje, sem mudança)
   ├─ quebras/                     quebras avulsas (formato de hoje)
   ├─ criativos/
   │  └─ C14/                      pasta do criativo (formato de hoje) + criativo.md com o cabeçalho de registro
   └─ registro/                    índice gerado (ver "Registro")
```

Mídia (vídeos, imagens, takes) continua fora do Git, na pasta compartilhada do time, espelhando a mesma estrutura.

### O briefing da oferta (`oferta.md`)

O sistema não começa nenhum trabalho de criativo sem ler este arquivo. O cabeçalho é estruturado (para a interface e o banco de dados); o corpo é livre.

```yaml
---
id: CIN-FR-01
marca: cinnarae
produto: gomas-magnesio
status: ativa                    # ativa | pausada | encerrada
mercado: { pais: FR, idioma: fr, tratamento: vous }
promessa: "dormir a noite inteira sem acordar às 3 h"   # a big idea da oferta
mecanismo: { problema: "...", solucao: "..." }          # UMP e UMS
avatar: "mulheres 50-65, sono e barriga na menopausa"
consciencia: problema            # nível de consciência dominante do público frio
funil:
  - { etapa: anuncio }
  - { etapa: presell, url: null, captura: null }        # null = não usa
  - { etapa: pdp, url: "https://...", captura: funil/pdp_2026-11-22.md }
  - { etapa: checkout }
oferta_atual: { texto: "-20% na 1ª compra + frete grátis", desde: 2026-11-18 }
precos: { capturado_em: 2026-11-22, fonte: funil/pdp_2026-11-22.md }
garantia: "30 dias, dinheiro de volta"
proibido: ["fabriqué en France", "brindes", "Image virtuelle"]
negocio: { cpa_breakeven: null, roas_alvo: null, controle: null }
atualizado: 2026-11-24
---
```

### Portão de contexto (antes de qualquer criativo)

Primeiro passo de todo processo (Réplica, Modelagem, Nativo, quebra de Modelagem), antes da referência:

1. Identificar a oferta. Sem oferta: perguntar ou abrir uma.
2. Ler `marca.md`, o produto e o `oferta.md`.
3. Conferir os campos obrigatórios: mercado, promessa, avatar, URL da página de venda, oferta atual, garantia, proibições, e se há pre-sell. Faltou algum: **perguntar ao dono, não inventar.**
4. Conferir se as capturas do funil estão frescas (sugestão: até 14 dias, e sempre antes de citar preço). Velha ou inexistente: capturar de novo com o Claude in Chrome (texto da página, sem imagens) e gravar em `funil/` com a data.
5. Ler a biblioteca de variáveis da marca.
6. Só então abrir a referência.

O roteiro passa a ter um item a mais no checklist: **congruência com o funil** (a promessa do anúncio é a mesma da pre-sell ou da PDP; a oferta citada é a que está no ar; o CTA leva à etapa certa).

Quebra avulsa de um anúncio de terceiros não exige oferta (ela é sobre o anúncio), mas é gravada sob a marca para a qual está sendo estudada.

## Camada 3: fontes de referência (só leitura)

Toda biblioteca de referência é uma **fonte**: uma pasta do time, uma pasta no Drive, a saída do bot de mineração, ou a própria Biblioteca de Anúncios. O sistema lê a fonte e grava **só o que derivou dela** (quebra, evidências em texto, variáveis) no espaço da oferta, sempre apontando para a origem.

### Cadastro de fontes (`<DADOS_DIR>/fontes.md`)

```
| Fonte | Tipo | Local | Marcas | Concorrente | Dono | Notas |
| F-elmora-adlib | adlibrary | página Elmora (ID da página) | cinnarae | Elmora | bot | minerada |
| F-time-swipes | pasta | <FONTES_DIR>/swipes-magnesio | cinnarae | vários | time | vídeos baixados |
```

### Identidade de cada referência

Cada anúncio de referência ganha uma **chave estável**, que não depende do nome do arquivo nem da numeração do projeto:

| Origem | Chave |
|---|---|
| Biblioteca de Anúncios | `meta:<ID do anúncio>` (ex.: `meta:1655441989385274`) |
| arquivo de vídeo ou imagem | `arq:<12 primeiros caracteres do SHA-1 do arquivo>` |
| outra URL | `url:<URL normalizada>` |

O mesmo vídeo com dois nomes diferentes tem a mesma chave `arq:`; isso resolve o caso dos arquivos renomeados.

### Regras

- O sistema nunca move, renomeia nem apaga arquivos de uma fonte.
- Quando uma ferramenta precisa do arquivo (ex.: `analisar_referencia.py`), ela lê do local original e grava a saída (frames, transcrição, `evidencias.md`) na pasta da quebra ou do criativo, como hoje. `Vídeo Bruto/` vira só uma caixa de entrada para quem não tem a referência numa fonte cadastrada.
- Texto de anúncio de terceiros continua sem ser copiado (regra atual): fica a chave, o link e o resumo trecho a trecho.

## Registro: nunca refazer o que já foi feito

O registro responde, antes de qualquer gasto de tempo: **essa referência já foi vista? Já foi quebrada? Já virou criativo? Como ele performou?**

### Entidades e IDs

| Entidade | ID | Exemplo | Liga com |
|---|---|---|---|
| Marca | slug + prefixo | `cinnarae` / `CIN` | — |
| Oferta | `<PREFIXO>-<PAÍS>-NN` | `CIN-FR-01` | marca, produto |
| Fonte | `F-<slug>` | `F-elmora-adlib` | — |
| Referência | chave estável | `meta:1655441989385274` | fonte |
| Quebra | `<PREFIXO>-Q###` | `CIN-Q001` | referência(s) |
| Variável | `<PREFIXO>-V###` (já existe) | `CIN-V014` | quebra ou criativo |
| Teste | `<PREFIXO>-T###` (já existe) | `CIN-T001` | criativo, variáveis |
| Criativo | `C<NN>` (numeração única do projeto, já existe) | `C19` | oferta, referência(s), quebra, teste |
| Entrega | número do Drive | `Criativo Nativo #11` | criativo |
| Resultado | criativo + período | `C19 2026-11-25..2026-12-01` | criativo, teste |

### Formato agora: cabeçalho nos arquivos + índice gerado

> **Substituído pelo Supabase** (ver "Decisões"): o registro mora nas tabelas, e o `buscar` virou função de `tools/dados.py` sobre a visão `v_historico_referencia`. O texto abaixo fica como registro do desenho original.

Cada `quebra.md` e cada `criativo.md` ganha um cabeçalho YAML com os IDs acima (referência, oferta, processo, formato, status, custo, número no Drive). O cabeçalho é a fonte da verdade; o resto do arquivo continua como é hoje.

Uma ferramenta nova, `tools/registro.py`, faz duas coisas:

- `registro.py indexar`: varre o espaço da oferta e gera `registro/indice.json` (e um `registro/REGISTRO.md` legível, que substitui o `CRIATIVOS.md`).
- `registro.py buscar <link | arquivo | ID>`: calcula a chave e diz se ela já existe e onde ("`meta:1655441989385274`: quebrada em CIN-Q004, virou C19, entregue como Criativo Nativo #11, teste CIN-T003 inconclusivo").

O passo "já vi?" entra no processo logo depois do portão de contexto. Se a referência já foi quebrada, a quebra é reaproveitada, não refeita.

### Por que não um banco de dados já

Markdown com cabeçalho estruturado funciona hoje, no Git, sem servidor, e o Claude lê direto. Como cada registro já tem ID e campos fixos, a migração para um banco é uma importação mecânica: cada cabeçalho vira uma linha. O índice gerado é o ensaio do esquema do banco.

## Evolução por fases

| Fase | O que muda | Depende de |
|---|---|---|
Revisado em 2026-11-24, com o Supabase desde já:

| Fase | O que muda | Depende de |
|---|---|---|
| **A. Banco no ar** | projeto Supabase criado; esquema `0001` rodado (tabelas, visões, pgvector); chaves no `.env` | dono cria o projeto |
| **B. Ponte do core** | `tools/dados.py`: ler e gravar no banco, `buscar` ("já vi?" por link ou arquivo), `parecidos` (busca vetorial), `capturar` (funil), embeddings locais | fase A |
| **C. Migração da Cinnarae** | marca, produto e fatos (do `PRODUTOS.md`), oferta CIN-FR-01 com funil e captura da PDP, concorrente Elmora, fontes, referências, criativos 01 a 28 com textos, variáveis, teste CIN-T001; os criativos entregues e os dados de negócio saem do repo público | fase B |
| **D. Processo novo** | portão de contexto e "já vi?" no PROCESSO, MODELAGEM, CLAUDE.md e nas skills; checklist com congruência com o funil; entrega grava no banco | fase C |
| **E. Garimpo (bot de mineração)** | grava referências e quebras avulsas no banco, sob uma fonte `F-...`; usa `buscar` para não minerar duas vezes | fase D |
| **F. Interface (Vercel)** | lê e escreve no banco; telas: ofertas, fontes, referências (com "já vista?" e "parecidos"), quebras, variáveis, testes, criativos, resultados | fase D |
| **G. Resultados automáticos** | números do Gerenciador (API da Meta) entram em `resultados`; Winner e Loser saem dos números | fase D |

**Feito em 2026-11-26 (adiantando F e G em versão local):** migração `0003_painel_meta.sql` (`anuncios_meta`, `metricas_meta` diário por anúncio, `anotacoes`, `avaliacoes`, `criativo_variaveis`, visões `v_criativo_totais` e `v_variavel_desempenho`); `tools/meta.py` (verificar, sincronizar, ligar, publicar pausado); `tools/painel.py` + `painel/` (biblioteca, player com takes e anotação por tempo, fila de refação, métricas vs média, retenção, comparação, ranking por variável, anúncios). O painel roda local porque a refação precisa dos arquivos e do FFmpeg; a versão Vercel pode reaproveitar as mesmas tabelas e a mesma API JSON. Inspiração: a "esteira de produção" mostrada por um player do mercado (anotação no frame que volta para produção, métricas por criativo, comparação, pontuação por variável).

## Esteira (decidida em 2026-11-26)

O painel vira uma esteira em quatro telas. O card anda da esquerda para a direita e sempre mostra com quem está a vez ("aguardando você" ou "com o Claude"). Qualquer usuário do painel aprova (hoje, o dono e o sócio).

```
GARIMPO ──aprovar──▶ PRODUÇÃO ──entregar──▶ BIBLIOTECA ──publicar──▶ CAMPANHAS
(referências)        (criativos sendo feitos)  (acervo pronto)        (Meta)
     ▲                                                                   │
     └────────── métricas alimentam Variáveis (o que ganha) ◀────────────┘
```

| Tela | O que faz | Estado |
|---|---|---|
| **Garimpo** | quadro de referências por fonte (Novas · Em quebra · Aprovadas · Reprovadas). **Aprovar** abre pop-up com oferta, Réplica ou Modelagem e prioridade, e cria o `C##` na Fila da Produção. **Reprovar** pede o motivo (fora do nicho, política, já temos, fraco); a chave estável impede que a referência volte. Entrada manual primeiro (link da Biblioteca de Anúncios ou vídeo), depois o bot. | a fazer (fase 2) |
| **Produção** | quadro por etapa. O card abre o criativo com a barra da esteira (Aprovar, Pedir ajuste, Mover, Descartar) e as abas Copy e roteiro (`ficha.json`), Takes e imagens, Documentos e Histórico. A fila de refação virou parte do quadro. | feito |
| **Biblioteca** | só entregue, no ar, pausado e descartado. A mesma página do criativo, com tudo que foi produzido. | feito |
| **Campanhas** | escolher criativos da Biblioteca + modelo de campanha → cria tudo **pausado** pela API; ativar (gastar) sempre com confirmação explícita no painel. A aba Anúncios entra aqui. | a fazer (fase 4) |

Menu: Esteira (Produção, Biblioteca), Análise (Métricas, Variáveis), Meta (Anúncios), Configuração (Marcas e ofertas, Equipe; Fontes entra com o Garimpo).

Banco: `esteira` (etapa e vez de cada criativo em produção, sem chave estrangeira para aceitar criativo ainda sem oferta) e `esteira_eventos` (histórico com autor e custo), migração `0005_esteira.sql`. O Garimpo vai acrescentar a decisão da triagem em `referencias` (decisão, motivo, quem, quando, oferta alvo, prioridade, nota do bot); Campanhas, as tabelas `campanhas` e `conjuntos` ligadas a `anuncios_meta`.

Ordem: (1) Produção + Biblioteca só com acervo + menu novo, feito em 2026-11-26; (2) Garimpo com entrada manual + tela de Fontes; (3) bot de garimpo (minera as fontes, ordena por dias no ar e número de variações); (4) Campanhas na Meta.

## Decisões

Tomadas em 2026-11-24:

- **Dados do negócio numa pasta no Drive**, sincronizada no computador de cada pessoa (o `DADOS_DIR` aponta para ela). Sem repositório Git próprio: muda com frequência e o mais simples vence.
- **Criativos entregues saem do core** e ficam no espaço da oferta. O core guarda só o contexto para o sistema funcionar (método, guias de formato, ferramentas).
- **Banco de dados: Supabase.**
- **Três níveis: marca > produto > oferta.** A oferta é a unidade de trabalho.
- **Validade da captura do funil: 14 dias**, e sempre recapturar antes de citar preço ou oferta.

- **Supabase desde já** (substitui a pasta no Drive para os dados do negócio): o sistema web vai ser Vercel + Supabase, então os dados nascem no banco. **Mídia fica no Google Drive**, com o link no banco. A estrutura de pastas descrita em "Camada 2" vale como modelo lógico; o esquema real está em [supabase/migrations/](supabase/migrations/).

## Supabase desde já

O sistema web vai ter banco próprio (Supabase) e interface na Vercel. Em vez de passar por uma pasta e migrar depois, os dados do negócio podem nascer no Supabase:

| Peça | Onde fica |
|---|---|
| Registro e dados estruturados (marcas, produtos, ofertas, fontes, referências, quebras, variáveis, testes, criativos, resultados) | Postgres do Supabase, uma tabela por entidade da seção "Registro" |
| Textos longos (quebra, roteiro, análise, captura do funil, copy final) | coluna de texto em Markdown na própria linha |
| Mídia (vídeos, imagens, takes) | Google Drive (já usado pelo time, sem custo) com o link na linha; ou Supabase Storage (exige plano pago com volume de vídeo) |
| Criativo em produção | pasta local de trabalho, como hoje (FFmpeg e os scripts precisam dos arquivos no disco); na entrega, textos e links sobem para o banco |
| Interface | Vercel, lendo e escrevendo no mesmo banco |
| Motor de produção (Claude Code, geração de imagens e takes, montagem) | local, ou num servidor próprio mais tarde; a Vercel não roda tarefas longas como montagem de vídeo |

O Claude lê e grava no banco por uma ferramenta do core (`tools/dados.py`, com a URL e a chave do Supabase no `.env`). A chave de serviço nunca vai para a interface.
