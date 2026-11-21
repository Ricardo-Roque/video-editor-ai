# Formato: Narrado

Formato 04 do quadro do Trello (ver [FORMATOS.md](../../FORMATOS.md)). Uma voz em off conta a história enquanto as imagens passam; ninguém fala na tela. O que prende: contraste (problema e solução se alternando), cortes rápidos (nunca mais de ~3 s na mesma cena) e narração com tom de conversa, sem pausas.

Para nós é o formato mais barato e previsível: sem sincronia labial, o take do modelo serve só pela voz e o visual pode ser feito localmente.

**O Criativo 05 fez a primeira venda do projeto.** A copy dele está sendo reaproveitada em outros formatos (ver [Palestrinha](../Palestrinha/FORMATO.md)).

## Exemplos

| Criativo | Variação | Duração | Custo | Ver primeiro |
|----------|----------|---------|-------|--------------|
| [05](Criativo%2005/) | infográficos numa prancheta apontados com varinha + mulheres com o sachê + B-roll | 62,6 s | US$ 2,35 | `prancheta_zoom.py` nas pranchetas; montagem local das fotos de prova social (T07) |
| [11](Criativo%2011/) | POV: mão segura o sachê num armazém, faixas de oferta, "último aviso" (urgência) | 22,4 s | US$ 4,06 (11+12) | `takes_config_veo.json`; voz do Veo sobre a imagem parada (`T02a_zoom_v1`) |
| [12](Criativo%2012/) | mesmo POV, "eu menti, produzimos demais" (superestoque) | 23,0 s | (no lote do 11) | faixas + círculo vermelho (`faixas_oferta.py --style surstock`) |

As referências do 11 e do 12 eram anúncios da concorrente (Elmora) já em francês: a fala ficou palavra por palavra, só a marca mudou.

## Estrutura

Infográfico (05):

| Bloco | Tempo | O que acontece |
|-------|-------|----------------|
| Hook | 0–27 s | 3 problemas, cada um num painel apontado pela varinha |
| Produto | 27–29 s | o sachê aparece |
| Body | 29–44 s | como usar e o resultado |
| Prova social | 44–50 s | "mais de 120 000 mulheres": mulheres segurando o sachê |
| CTA | 50–58 s | garantia de 30 dias e oferta |

Promoção (11, 12), 20 a 25 s: hook de urgência ("dernier avertissement") ou confissão ("j'ai menti") → motivo da oferta (estoque acabando / sobrando) → "2 achetés = 1 offert" e CTA. Faixas fixas no topo o vídeo todo. A confissão do 12 usa **curiosidade e efeito "ahá"** do Trello: abre a pergunta "mentiu sobre o quê?" e só fecha depois.

## Como escrever o roteiro

Quando a copy não vem pronta da referência:
- Abrir com **gancho visual + conflito** na mesma frase (a imagem mostra o problema enquanto a voz o nomeia).
- Encadear conflito → mudança várias vezes: cada problema resolvido abre o próximo. Nunca mais de ~3 s na mesma imagem.
- Voz de conversa, como um áudio de WhatsApp para uma amiga; sem pausas.
- Fechar com **contraste visual de antes e depois** e a moral ligando ao produto.
- Promoção (11, 12): a confissão ou o alerta abre uma pergunta que só fecha na oferta.

## Receita de produção

- **Voz**: mesma persona e seed em todos os takes. Escrever `"say": "The unseen off-screen narrator says:"` e, na cena, que ninguém aparece. O padrão "She says" faz o modelo pôr uma mulher falando.
- **Infográfico (05)**: pranchetas Q1, Q2... já com o texto no idioma final; as variações da varinha saem **editando** a prancheta base. O take serve só pela voz (o texto sai ilegível em 360p); o visual é a imagem nítida com zoom lento até o painel falado (`prancheta_zoom.py`, custo 0). 14 imagens custaram US$ 0,54; uma imagem pode servir a dois takes.
- **Prova social (05)**: fotos com zoom lento alternado (aproxima/afasta), corte nas pausas das frases, montado localmente com a voz do take (`T07_montagem_v1.mp4`).
- **POV com produto (11, 12)**: imagens H1 (mão segurando o sachê), B1 (sachê sobre a caixa com os ursinhos), B2 (mão tocando o rótulo), sempre com o sachê de [Referências/](../../Referências/) como ref e "red raspberry gummy bears". Takes em **Veo 3.1 Lite 720p** (o Omni deformava o rótulo): só 4, 6 ou 8 s e fala rápida (~3,3–3,6 palavras/s), então dividir em a/b numa pausa já no roteiro. Partir de [_Modelo Criativo/takes_config_veo.json](../../_Modelo%20Criativo/takes_config_veo.json). O take b parte do último frame do take a.
- **Faixas de oferta**: PNG local com `faixas_oferta.py`, overlay `{"mode": "patch", "x": 0, "y": 0}`. Nunca pedir texto de oferta ao modelo.

## Cuidados

- Números falados: por extenso no prompt se o modelo errar ("cent vingt mille"); na legenda, `120\h000`.
- Frase inventada depois do fim da fala (05 T08): cortar numa pausa real.
- Produto parado: mesmo proibindo, o Veo pôs uma apresentadora atrás da caixa duas vezes. Sachê "flutuando" ou logo errado ("Cinnarac"): usar só a voz do take sobre a imagem nítida (`prancheta_zoom.py`).
- O fundo pode mudar depois de ~4 s; se a fala já acabou, o corte de silêncio remove o trecho.
- Confirmar a oferta com o dono antes do roteiro (ver [PRODUTOS.md](../../PRODUTOS.md)). Legenda não pode cobrir o rótulo: `caption_y`.
- Copy agressiva do 05 (glicemia/insulina, "120 000 femmes") mantida por decisão do dono.
