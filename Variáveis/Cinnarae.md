# Biblioteca de variáveis — Cinnarae (França)

Formato e regras em [README.md](README.md). Método em [MODELAGEM.md](../MODELAGEM.md).

Controle atual: **não informado**. Linha de lucro (CPA de break-even ou ROAS alvo): **não informada** (ver [PRODUTOS.md](../PRODUTOS.md)). Sem esses dois, nenhuma variável sai de Candidate e nenhum anúncio recebe tier.

Linhas iniciais (2026-11-24): variáveis tiradas dos criativos já feitos e das referências da Elmora. Nenhuma tem número de performance ainda; todas são Candidate.

## Variáveis

| ID | Categoria | Variável | Valor | Status | Fonte | Evidência | Hipótese | Data | Notas |
|----|-----------|----------|-------|--------|-------|-----------|----------|------|-------|
| CIN-V001 | Formato | formato do vídeo | Narrado: narradora em off, primeira pessoa, sobre infográfico impresso numa prancheta vista de cima, varinha de madeira apontando o painel falado | Candidate | Criativo 05 | primeira venda da Cinnarae (2026-11-20); sem gasto, CPA nem controle registrados | o texto da prancheta acompanhando a voz segura o olho e dá cara de explicação, não de anúncio | 2026-11-24 | não isolada; base é swipe (SP Nutrition) |
| CIN-V002 | Hook | abertura | três sintomas noturnos em sequência "se... se... se..." (levantar 3 vezes para urinar, boca seca, não dormir a noite toda); 11 palavras nos 3 primeiros segundos; sem corte no hook | Candidate | Criativo 05 | sem dados | sintoma concreto e noturno faz a pessoa se reconhecer antes de ligar o problema ao magnésio | 2026-11-24 | na referência o primeiro sintoma vem ligado à glicemia: risco de política (ver `analise.md` do 05) |
| CIN-V003 | Áudio e ritmo | ritmo de cortes | plano contínuo no hook e no corpo (planos de ~6 s); final acelerado (planos de ~1,7 s nos últimos 20%) | Candidate | Criativo 05 | medido em 2026-11-24 com `analisar_referencia.py`; sem dados de performance | ritmo calmo enquanto explica e acelerado na prova e na oferta empurra para o clique | 2026-11-24 | — |
| CIN-V004 | Prova | prova social | montagem de 5 mulheres diferentes segurando o sachê, ~1 s cada, sobre a frase de número de clientes | Candidate | Criativo 05 | sem dados | ver várias pessoas comuns com o produto dá prova sem precisar de depoimento longo | 2026-11-24 | o número de clientes precisa ser verdadeiro; não está em `PRODUTOS.md` |
| CIN-V005 | Oferta | oferta no fecho | garantia de 30 dias + -20% na primeira compra | Candidate | Criativo 05 | sem dados | garantia antes do desconto tira o risco e deixa o desconto como empurrão final | 2026-11-24 | oferta da PDP mudou em 2026-11-22 (Black Friday) |
| CIN-V006 | Formato | formato estático | foto amadora + história em primeira pessoa de 1.200 a 3.300 palavras + link só no cartão | Candidate | swipe Elmora (base dos criativos 15 a 28) | sem dados nossos; anúncios da Elmora escolhidos por posição em impressões, número de variantes e dias no ar | não parecer anúncio faz ler até o fim; o lead de história chega no produto depois da identificação | 2026-11-24 | swipe: tempo no ar pode ser mérito da oferta |
| CIN-V007 | Avatar | dor de entrada | mulher de 55 a 65 anos, barriga dura de menopausa e despertar às 3 h da manhã | Candidate | swipe Elmora (16, 17, 18, 19, 20, 25) | sem dados | duas dores ligadas por um só mecanismo (cortisol) fazem a solução parecer maior | 2026-11-24 | swipe; barriga é alegação de risco (só como relato) |
| CIN-V008 | Autoridade | entrada da autoridade | mentor que descobre e não vende (cantineira, primo mecânico, técnica de radiologia); metáfora do mecanismo tirada da profissão dele | Candidate | swipe Elmora (17, 18, 19, 23) | sem dados | descoberta orgânica soa mais crível que "fui ao médico" | 2026-11-24 | swipe; nunca médico com nome nem credencial inventada |
| CIN-V009 | UMS | mecanismo da solução | bisglicinato puro, sem óxido: "vire o seu magnésio" e leia a ordem dos ingredientes; óxido absorvido em ~4% (Firoz e Graber, 2001) | Candidate | swipe Elmora (21, 26) | sem dados | fato concreto e verificável no verso do frasco vence "o nosso é melhor" | 2026-11-24 | zéro oxyde confirmado em `PRODUTOS.md` |
| CIN-V010 | Imagem (nativo) | tipo de imagem | quebra de padrão sem relação com o texto (caracol gigante, janela de trem, vaca deitada) | Candidate | swipe Elmora (17, 21, 25) | sem dados | a estranheza para o dedo; o texto faz o resto | 2026-11-24 | swipe |
| CIN-V011 | Imagem (nativo) | tipo de imagem | o problema em close: corpo sem rosto com um detalhe que conta a história (barriga com adesivo hormonal) | Candidate | swipe Elmora (18) | sem dados | a leitora vê o próprio corpo antes de ler | 2026-11-24 | swipe; maior risco de política dos quatro tipos |
| CIN-V012 | Avatar | dor de entrada (sono) | cãibras e pernas inquietas à noite como porta para o sono | Candidate | Criativos 22, 24, 27 | sem dados | dor física noturna e concreta é mais crível e mais segura para política que "insônia" | 2026-11-24 | ângulo definido pelo dono na leva 19–28 |
| CIN-V013 | CTA | fecho do nativo | sem URL no texto; o post termina apontando para o cartão ("je vous le mets juste en dessous 👇") | Candidate | Criativos 19 a 28 | sem dados | o post continua parecendo pessoal até o fim | 2026-11-24 | regra do dono (2026-11-22) |

## Testes de conceito

| Teste | Data | Criativo | Vencedoras empilhadas | Variável em teste | Hipótese | Vence se | Perde se | Status | Resultado |
|-------|------|----------|-----------------------|-------------------|----------|----------|----------|--------|-----------|
| CIN-T001 | 2026-11-24 | 13 | CIN-V002, CIN-V004, CIN-V005 (copy do 05 sem mudança) | formato: Narrado (prancheta, narradora em off) → Palestrinha (apresentadora de pé apontando um quadro branco) | uma pessoa em cena apontando o quadro segura mais que a voz em off, com a mesma copy | hook rate e CPA melhores que os do 05 no mesmo período | CPA pior que o do 05 com gasto comparável | entregue | sem números registrados (teste registrado depois da entrega) |
