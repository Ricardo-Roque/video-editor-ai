# Catálogo de criativos

Todos os criativos feitos até agora, com formato, decisões e o que cada um ensinou.
Antes de começar um criativo novo, procure aqui um criativo do mesmo formato e use a pasta dele como exemplo.
Os textos (análise, roteiro, prompts, configs) estão no repositório. Imagens, takes e vídeos ficam na pasta compartilhada do time.

## Resumo

| Criativo | Referência (`Vídeo Bruto/`) | Formato | Duração final | Custo total | Situação |
|----------|-----------------------------|---------|---------------|-------------|----------|
| [01](Criativo%2001/) | `Criativo #01 [Hook #02].mp4` | antes/depois + talking head selfie (autoridade) | 3:59 | US$ 8,66 | aprovado |
| [04](Criativo%2004/) | `Criativo #04 (1).mp4` | talking head sentada, lista de sintomas, 2 hooks | 48,3 s + cortes A (21,9 s) e B (26,5 s) | US$ 1,30 | aprovado |
| [05](Criativo%2005/) | `Criativo #05.mp4` | narradora em off + infográficos em prancheta + mulheres com o sachê | 62,6 s | US$ 2,35 | **primeira venda** |
| [06](Criativo%2006/) | `Criativo #06 (1).mp4` | enfermeira de pijama cirúrgico no hospital, 5 dicas | 114,9 s | US$ 4,42 | 1º corte entregue |
| [07](Criativo%2007/) | `Criativo #07.mp4` | depoimento UGC ("reclamação falsa"), cards antes/depois | 73,5 s | US$ 2,31 | 1º corte entregue |
| 07 Sono | (mesma) | versão do 07 sem emagrecimento, foco em sono, reaproveitando takes | 71,0 s | US$ 0,70 | 1º corte entregue |
| [08](Criativo%2008/) | `46a88423….mp4` | senhora levanta do chão (take sem fala) e fala | 13,4 s | US$ 2,40 (08+09+10) | 1º corte entregue |
| [09](Criativo%2009/) | `91e91073….mp4` | farmacêutica, selfie na farmácia | 13,0 s | (no lote acima) | 1º corte entregue |
| [10](Criativo%2010/) | `16a0e279….mp4` | mulher no balcão da cozinha, sachê parado em cena | 47,8 s | (no lote acima) | 1º corte entregue |
| [11](Criativo%2011/) | `Criativo #08.mp4` | POV mão + sachê em armazém, narradora em off, faixas de oferta (urgência) | 22,4 s | US$ 4,06 (11+12) | 1º corte entregue |
| [12](Criativo%2012/) | `Criativo #09.mp4` | mesmo formato do 11 ("superestoque") | 23,0 s | (no lote acima) | 1º corte entregue |
| [13](Criativo%2013/) | `Criativo #10.mp4` (só formato) | "palestrinha": apresentadora na frente de quadro branco, copy do 05 | — | ~US$ 1,21 até agora | em produção (takes) |

Atenção à numeração: o número da pasta **não** é o número do arquivo de referência. Ex.: `Criativo #08.mp4` virou a pasta 11, e `Criativo #10.mp4` é a referência de formato do 13, não do 10. Registre sempre a origem na primeira linha do `analise.md`.

Custo médio: cerca de US$ 0,03 a 0,04 por segundo de vídeo final em Omni 360p; o dobro em Veo 720p.

## Formatos já resolvidos

Use o criativo indicado como modelo de configuração, prompts e montagem.

| Formato | Exemplo | Como foi feito |
|---------|---------|----------------|
| Talking head selfie (fala para a câmera) | 01, 09 | Omni 360p, 1 imagem base (B1) + variações de gesto; legenda padrão |
| Talking head sentada / em pé, câmera fixa | 04, 06 | Uma imagem base para todos os takes; o gesto de cada take vai na persona do `takes_config.json`, sem gerar imagem nova (06) |
| Antes/depois no hook | 01, 07 | "Depois" gerado **editando** o "antes" (`--ref`), para manter rosto, roupa e sala; cards lado a lado com `width`/`x`/`y` (07) |
| Hook de ação sem fala | 08 | Take curto (3 s) sem fala com `gerar_take.py`; no `montagem.json`, `"silent": true` |
| Vários hooks com o mesmo body | 04 | Body gerado uma vez e reaproveitado; um `montagem_hookX.json` por corte |
| Narradora em off sobre infográfico | 05 | Take só pela voz; o visual é a imagem nítida com zoom lento (`prancheta_zoom.py`) |
| Montagem de fotos (prova social) | 05 (T07) | Fotos com zoom lento alternado (aproxima/afasta), corte nas pausas das frases, tudo local |
| Produto parado em cena | 10 | Sachê nítido colado por cima do take inteiro (`colar_produto.py` + overlay `patch`); legenda subida (`caption_y`) |
| POV mão + produto, sem rosto | 11, 12 | Veo 3.1 Lite 720p (rótulo nítido), `"say"` em off, faixas fixas (`faixas_oferta.py`); onde o produto "flutua", voz do take sobre a imagem nítida com zoom |
| Apresentador + quadro branco | 13 | Board na faixa de cima da imagem; a apresentadora aponta para a linha falada (uma imagem de partida por linha); texto do quadro trocado pelo nítido com `quadro_nitido.py` ou overlay `patch` da faixa de cima |
| Nova versão de um criativo pronto | 07 Sono | Roteiro novo (`roteiro_fr_sono.md`), takes antigos recortados em arquivos novos, só os takes que faltam são gerados |
| Mesma copy em outro formato | 13 | Copy copiada sem mudança; só imagens, takes e montagem são novos |

## Lições por criativo

**01** (primeiro, referência de todas as etapas). 720p custou US$ 0,07/s: caro demais, daí o padrão 360p (US$ 0,023/s) e upscale local. Origem da divisão Ta/Tb: T10 e T27 tiveram fala cortada ou engolida, e só a frase que faltou foi refeita a partir do último frame. Legenda subida para y=1420 a pedido.

**04.** O dono trocou o visual da referência por uma foto de estilo própria ("nessa pegada"): fazer uma pessoa nova com esse estilo, nunca copiar o rosto. Omni 1.2 caiu no meio do lote; o T04 saiu no Omni 1.1 com a mesma seed. Falhas do modelo ("Video generation failed") não são cobradas: tentar de novo.

**05.** Texto pequeno em prancheta fica ilegível em 360p: o dono reprovou os takes do modelo. Solução padrão para cena com muito texto: `prancheta_zoom.py`. "120 000" na legenda vira `120\h000` para não quebrar. No T08 o modelo inventou uma frase sem sentido depois do fim da fala: cortar numa pausa real.

**06.** "A mesma modelo" da referência foi recusado (pode ser pessoa real): personagem nova com o mesmo visual. Omni 1.1 só aceita takes de 3 a 10 s e falha muito (sem custo). O modelo bloqueou "n'achetez pas" repetidas vezes; "ne prenez surtout pas" passou com o mesmo sentido. Fato não confirmado pelo dono ("fabriqué en France") saiu do roteiro. Legenda "1400€" junta.

**07.** O modelo acrescentou "Hein ?" e repetiu "Profitez de l'offre": cortes na montagem, sem gerar de novo. Cards de antes/depois a 470 px cobriam a boca; 380 px em y=985 resolveu. O dono às vezes prefere gerar as imagens na própria ferramenta: entregar prompts em inglês prontos para colar.

**07 Sono.** Reaproveitar takes economiza: 13 takes antigos (4 recortados) + 3 novos = US$ 0,70. Omni fora do ar: Veo 3.1 Lite com aprovação do dono.

**08–10.** Lote liberado de ponta a ponta pelo dono. Recorte local da imagem (B1_v2 do 08) custa 0. No 10 o modelo deformou o texto do sachê em todos os takes: daí `colar_produto.py` e as opções `silent`, `patch` e `caption_y` do `montar.py`.

**11–12.** Referências já em francês, da concorrência: só a marca muda. Omni deformava o rótulo; Veo 3.1 Lite 720p mantém o rótulo, mas só aceita 4, 6 ou 8 s e fala rápido (~3,6 palavras/s). "She says" no prompt faz o Veo colocar uma mulher na cena: usar `"say": "The unseen off-screen narrator says:"`. Mesmo assim, em cena de produto parado o Veo pôs uma apresentadora: usar só a voz sobre a imagem. O fundo pode mudar depois de ~4 s; se a fala já acabou, o corte de silêncio resolve.

**13.** Primeiro reaproveitamento da copy vencedora (05) em outro formato. O dono pediu que a apresentadora **aponte para o quadro sempre que falar do que está escrito**: uma imagem de partida por linha do quadro, com o canetão na linha certa. O modelo inventou frase depois do fim da fala de novo (T01): corte em pausa. Nova ferramenta `quadro_nitido.py` troca o texto do quadro pelo nítido, mantendo mãos e cabelo do take.
