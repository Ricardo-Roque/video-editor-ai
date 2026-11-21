# Editor de Vídeo — instruções do projeto

Este projeto produz criativos de vídeo (anúncios 9:16) a partir de um vídeo de referência, traduzidos e adaptados para outro país, com imagens e takes gerados por IA e montagem local. Várias pessoas usam o projeto, cada uma com a própria chave do OpenRouter.

**Antes de qualquer trabalho num criativo, leia [PROCESSO.md](PROCESSO.md) e siga as etapas na ordem.** Leia também [PRODUTOS.md](PRODUTOS.md) (fatos confirmados do produto) e identifique o formato da referência entre os 16 do Trello resumidos em [FORMATOS.md](FORMATOS.md). Leia o guia `Criativos Exemplo/<formato>/FORMATO.md` (todos os 16 têm um) e use os criativos daquela pasta como exemplo, quando houver ([CRIATIVOS.md](CRIATIVOS.md) tem o catálogo). O [Criativo 01](Criativos%20Exemplo/Lo-fi/Criativo%2001/) é o exemplo completo de cada etapa.

**Para escrever, analisar ou revisar qualquer copy** (análise, roteiro, hooks, variações, CTA), siga [Copy/COPY.md](Copy/COPY.md): o método tirado dos livros clássicos de copy (Schwartz, Hopkins, Ogilvy, Caples, Halbert, Sugarman, Great Leads, Evaldo, Hormozi e outros). Para aprofundar um conceito, o resumo de cada livro está em `Copy/livros/` (índice em [Copy/BIBLIOTECA.md](Copy/BIBLIOTECA.md)). Os PDFs ficam só na pasta local `Livros Copywriting/`, fora do Git.

## Regras

- Responda ao usuário em português. Quem usa o projeto não fala o idioma dos criativos: sempre mostre a tradução de volta para o português quando houver texto em outro idioma.
- **Aprovação em cada etapa**: análise → roteiro → imagens (uma a uma) → takes (um a um, salvo se o usuário liberar o lote) → montagem. Nunca gere takes de imagens não aprovadas.
- **Gastar o mínimo possível**: informe o custo estimado antes de qualquer geração paga e o gasto real depois. Padrão: imagens `google/gemini-nano-banana-2.1`; takes `google/gemini-omni-1.2-flash` em 360x640. Veo 3.1 Lite 720p só para rótulo em movimento ou com o Omni fora do ar, com aprovação. Corrija só o trecho com erro (divisão Ta/Tb) em vez de refazer o take inteiro. Reaproveite imagens e takes aprovados.
- **Conferir antes de mostrar**: rode `tools/checar_takes.py` em todo take e olhe os frames; olhe toda imagem gerada antes de apresentar.
- **Roteiro fiel à referência**: mesma ordem e conteúdo; liste e explique toda adaptação. Não afirme fato do produto que não esteja em `PRODUTOS.md`; pergunte.
- **Roteiro anotado**: na análise, anote cada frase da referência com o elemento que prende a atenção nela (vocabulário em `FORMATOS.md`); a tradução preserva esses elementos frase a frase. Roteiro novo a partir de um vencedor segue a Etapa 2b do `PROCESSO.md` (mesmo esqueleto, tema novo, nenhum fato sem fonte).
- **Copy**: na análise, registre nível de consciência, tipo de lead, crença única e os 4 pés (seção 2 do `COPY.md`); antes de aprovar um roteiro, passe pelo checklist da seção 9. Quando um livro e uma regra do projeto discordam, vale a regra do projeto.
- **Texto na tela** (rótulo, prancheta, quadro, faixas): decida a solução na análise, pela tabela "Texto na tela" do `PROCESSO.md`.
- **Pessoas reais**: nunca copie o rosto da pessoa da referência nem de uma foto de estilo; crie personagem nova com o mesmo visual.
- **Política de anúncios**: avise riscos (antes/depois de corpo, depoimento fabricado, autoridade fictícia, alegações de saúde do país) uma vez, antes de gastar; a decisão é do usuário e fica registrada no `analise.md`.
- **Criativo em produção** fica na raiz (`Criativo NN/`). **Ao entregar**, siga a lista "Ao entregar um criativo" do `PROCESSO.md`: notas de produção, mover para `Criativos Exemplo/<formato>/` (corrigindo os `../` do `montagem*.json`), `CRIATIVOS.md`, `FORMATO.md`, `PRODUTOS.md` e oferecer commit e push.

## Ambiente

- Rode os scripts Python com `python -I -X utf8 tools/<script>.py ...` a partir da raiz do projeto (`-I` ignora `PYTHONIOENCODING`, então use `-X utf8`).
- Chave do OpenRouter em `.env` (`OPENROUTER_API_KEY`); nunca exibir nem copiar a chave. O `.env` não vai para o Git.
- FFmpeg, Python 3.13 com as dependências de `requirements.txt`, Node 24 e HyperFrames (skills em `.claude/skills/`, opcional).
- Imagens, takes e vídeos não estão no Git: se faltarem num criativo antigo, peça ao usuário para copiá-los da pasta compartilhada do time.
- Lotes de takes e montagem completa podem passar de 10 minutos: rode em segundo plano. No máximo 2 takes em paralelo.
- Arquivos temporários vão no scratchpad da sessão, não nas pastas do criativo.
