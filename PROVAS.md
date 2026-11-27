# Provas sociais (lojas de demonstração)

Peças de prova social feitas por IA para a página de produto de uma **loja de demonstração** (loja de exemplo, sem venda real): foto de uma pessoa com o produto ou vídeo curto de depoimento. O dono pede na tela "Provas sociais" do painel, aprova cada etapa ali e baixa os arquivos aprovados da biblioteca da tela.

## Por que só em loja de demonstração

Uma foto ou um depoimento de "cliente" gerado por IA, posto numa loja que vende de verdade, é avaliação falsa: engana quem compra, vai contra as regras da Meta e da Shopify e, nos EUA, contra a regra da FTC de 2024 sobre avaliações falsas (que cita conteúdo gerado por IA). Por isso:

- o painel só aceita o pedido em marca marcada como **loja de demonstração** (Marcas e ofertas › Editar a marca);
- o Claude também confere: se a marca vende de verdade (ex.: Cinnarae, que tem anúncio rodando e venda), não gera, e sugere o caminho real (avaliações de clientes, pedido de avaliação pós-compra, UGC com consentimento);
- todo arquivo final leva o selo **"ilustrativo · IA"** no idioma da peça (`tools/selo_ia.py`). O selo não sai, nem a pedido: é o que impede a peça de passar por cliente real se for parar numa loja de verdade.

## Etapas

| Tipo | Etapas no painel | O que o Claude entrega |
|---|---|---|
| Foto com o produto | Fila → Imagem → Aprovada | `final/PS##.jpg` com selo |
| Vídeo de depoimento | Fila → Texto → Imagem → Vídeo → Aprovada | fala (idioma + PT), quadro inicial, `final/PS##.mp4` com selo |

Cada card diz com quem está a vez. "Faça as provas sociais" (ou "continue a esteira" incluindo provas) = rodar `python -I -X utf8 tools/painel.py provas` e trabalhar o que está com o Claude. Pedido de ajuste aparece como `AJUSTE PEDIDO`: refazer só o que foi pedido.

## Como o Claude produz

Pasta: `Provas Sociais/PS##/` na raiz (`imagens/`, `video/`, `final/`, `prompt.md`). Mídia sobe para o R2 no `prova-entregar`.

1. **Antes de gastar**: ler o pedido, a persona e a marca (`painel.py provas`); confirmar que a marca é de demonstração; achar a foto do produto (pedir ao dono se não houver; o rótulo vem dela, nunca inventado). Informar o custo estimado e esperar o "pode".
2. **Texto (só vídeo)**: fala em primeira pessoa, 15 a 25 s (~3 palavras/s em francês), no idioma da peça, com a tradução em português. Linguagem de experiência ("voltei a dormir a noite toda"), nunca promessa de cura, número inventado ("perdi 8 kg") ou alegação de saúde que não esteja no `PRODUTOS.md` do produto. Entregar: `painel.py prova-entregar PS## --etapa texto --custo 0 --texto "..." --texto-pt "..."`.
3. **Imagem**: personagem nova (nunca rosto de pessoa real nem de foto de referência), cenário da persona, produto real na mão ou na mesa, luz de celular. `gerar_imagem.py --ref <foto do produto> --aspect 4:5` para foto (ou 1:1, se o pedido disser) e `--aspect 9:16` para o quadro do vídeo. Modelo padrão, ~US$ 0,04 por imagem. Olhar a imagem antes de entregar (mãos, rótulo, texto deformado). Foto: aplicar o selo (`selo_ia.py imagens/PS##_v1.png final/PS##.jpg --idioma <idioma>`) e entregar `--etapa imagem`. Vídeo: entregar `--etapa imagem` (o quadro aprovado é a base do take).
4. **Vídeo**: `gerar_take.py --image <quadro aprovado> --size 360x640 --duration <fala + 1 s>` com o Omni 1.2 Flash (~US$ 0,023/s: 20 s ≈ US$ 0,46), fala no prompt. `checar_takes.py` e olhar os frames. Aplicar o selo (`selo_ia.py video/PS##_v1.mp4 final/PS##.mp4 --idioma <idioma>`) e entregar `--etapa video --custo <US$ real>`.
5. Ao aprovar a última etapa, a prova vai para a Biblioteca da tela, agrupada por produto, com o arquivo final para baixar.

## Comandos

```
python -I -X utf8 tools/painel.py provas
python -I -X utf8 tools/painel.py prova-entregar PS01 --etapa texto|imagem|video --custo 0.04 [--texto "..." --texto-pt "..."] [--nota "..."]
python -I -X utf8 tools/selo_ia.py <entrada> <saída> --idioma fr
```

Banco: tabela `provas_sociais` (migração `0010_garimpo_provas.sql`), histórico em `esteira_eventos` com o código `PS##`, coluna `marcas.demonstracao`.
