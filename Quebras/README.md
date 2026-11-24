# Quebras avulsas

Quebras de anúncios feitas sem produzir criativo: swipes da Biblioteca de Anúncios, vencedores e perdedores nossos. Cada quebra alimenta a biblioteca da marca em [Variáveis/](../Variáveis/) e termina com 3 testes de conceito. Método: [MODELAGEM.md](../MODELAGEM.md) ("Quebra avulsa").

```
Quebras/<Marca>/<AAAA-MM-DD> <anunciante> - <tema>/
├─ quebra.md        modelo em _Modelo Criativo/quebra.md
└─ referencia/      evidências (tools/analisar_referencia.py; nativo: imagem + fonte.md)
```

- No Git vão só os textos (`quebra.md`, `evidencias.md`, transcrição, cortes, `fonte.md`). Vídeos, frames e imagens ficam fora (`.gitignore`), como nos criativos.
- O texto de anúncio de terceiros não é copiado para a pasta: fica o link em `fonte.md` e o resumo trecho a trecho na quebra.
- Quando uma quebra vira criativo de Modelagem, o `conceito.md` do criativo aponta para ela em vez de repetir a quebra.
- A mineração automática (próxima fase do projeto) vai gravar aqui, no mesmo formato.
