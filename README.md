# Editor de Vídeo com IA

Produção de criativos de vídeo (anúncios 9:16) a partir de um vídeo de referência: o roteiro é traduzido e adaptado para outro país, as imagens e os takes são gerados por IA via OpenRouter, e a montagem (cortes, legendas, overlays) é feita localmente com FFmpeg.

O trabalho é conduzido pelo [Claude Code](https://claude.com/claude-code) dentro desta pasta, seguindo um processo com aprovação em cada etapa e gasto mínimo de API.

| Documento | Para quê |
|-----------|----------|
| [PROCESSO.md](PROCESSO.md) | processo de **Réplica** (refazer a referência fiel) e a produção: da referência ao vídeo final |
| [MODELAGEM.md](MODELAGEM.md) | processo de **Modelagem**: quebrar anúncios em variáveis, empilhar as vencedoras e testar uma variável por criativo |
| [Variáveis/](Variáveis/) | biblioteca de variáveis por marca: vencedoras, perdedoras e testes de conceito |
| [Quebras/](Quebras/) | quebras de anúncios feitas sem produzir criativo |
| [FORMATOS.md](FORMATOS.md) | os 16 formatos criativos do Trello, como anotar e escrever roteiros, estruturas e elementos que prendem a atenção |
| [Criativos Exemplo/](Criativos%20Exemplo/) | uma pasta por formato com o guia `FORMATO.md` (roteiro, produção, custo, riscos) e os criativos entregues naquele formato |
| [Copy/COPY.md](Copy/COPY.md) | o método de copy tirado de 58 livros clássicos (Schwartz, Hopkins, Ogilvy, Caples, Halbert...): diagnóstico, hook, corpo, oferta, checklist. Resumos por livro em [Copy/livros/](Copy/livros/) |
| [CRIATIVOS.md](CRIATIVOS.md) | catálogo de todos os criativos, com custo e lições |
| [PRODUTOS.md](PRODUTOS.md) | fatos confirmados de cada produto (oferta, embalagem, o que não pode ser dito) |
| [CLAUDE.md](CLAUDE.md) | regras que o Claude segue em toda sessão |

## Instalação

Precisa de:
- **Python 3.13** (3.11 ou mais novo deve funcionar)
- **FFmpeg** no PATH (`ffmpeg -version` precisa responder)
- **Claude Code** (CLI, app desktop ou extensão do VS Code)
- **Node 24** só se for usar as skills do HyperFrames (opcional)
- Uma chave do **OpenRouter** com saldo

```
git clone https://github.com/Ricardo-Roque/video-editor-ai.git "Editor de Vídeo"
cd "Editor de Vídeo"
pip install -r requirements.txt
cp .env.example .env
```

Abra o `.env` e cole a sua chave em `OPENROUTER_API_KEY`. Cada pessoa usa a própria chave; o `.env` nunca vai para o Git.

No primeiro uso, o `faster-whisper` baixa o modelo de transcrição (algumas centenas de MB).

No Windows, rode os scripts sempre assim, a partir da raiz do projeto:
```
python -I -X utf8 tools/<script>.py ...
```

## Fazer um criativo

1. Coloque o vídeo de referência em `Vídeo Bruto/`.
2. Abra o Claude Code nesta pasta e diga, por exemplo:
   > Novo criativo: Criativo 12, referência `Vídeo Bruto/<arquivo>.mp4`, francês, França, Cinnarae.

   Ou digite `/novo-criativo`.
3. O Claude identifica o formato da referência (pelo `FORMATO.md` do exemplo mais próximo), analisa a referência, propõe o roteiro (com tradução de volta para o português), gera as imagens, os takes e monta o vídeo, parando para você aprovar cada etapa e mostrando o custo antes de cada geração paga.
4. O vídeo final sai em `Vídeos Prontos/`.

Dois processos: **Réplica** ("refazer", "traduzir") segue a referência o mais fiel possível; **Modelagem** ("modelar", "conceito novo") quebra a referência em variáveis e monta um conceito novo com as variáveis vencedoras da biblioteca, testando uma de cada vez. Para só analisar um anúncio, sem produzir: "quebra do anúncio <link ou arquivo>".

Para continuar um criativo começado por outra pessoa, diga "continuar o Criativo NN": o Claude descobre a etapa pelos arquivos da pasta.

## O que está e o que não está no repositório

No Git: ferramentas (`tools/`), documentação, skills do Claude (`.claude/skills/`), modelo de criativo (`_Modelo Criativo/`), fonte das legendas, foto do produto e os textos de cada criativo entregue, em `Criativos Exemplo/<formato>/` (análise, roteiro, comparativo, prompts, configurações).

Fora do Git (ver [.gitignore](.gitignore)): vídeos de referência, imagens, takes, intermediários de montagem e vídeos prontos. São arquivos grandes. Ficam no Cloudflare R2 do time ([R2.md](R2.md)), e o painel os mostra em qualquer computador. Para continuar um criativo antigo: `python -I -X utf8 tools/midia.py baixar C<NN>`.

## Regras do time

- Antes de criar a pasta de um criativo novo, rode `python -I -X utf8 tools/painel.py proximo --tipo video` (ou `nativo`, `imagem`) e avise no grupo o código que vai usar.
- Ao terminar um criativo, atualize [CRIATIVOS.md](CRIATIVOS.md) (e [PRODUTOS.md](PRODUTOS.md) se confirmou algo do produto) e faça commit dos textos.
- Nunca commite o `.env` nem cole a chave em arquivos, prompts ou mensagens.
