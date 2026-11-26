# Modelagem: criativo novo a partir de variáveis vencedoras

O projeto tem dois processos para fazer um criativo:

| | **Réplica** ([PROCESSO.md](PROCESSO.md)) | **Modelagem** (este documento) |
|---|---|---|
| Objetivo | refazer uma referência o mais fiel possível, em outro idioma e país | construir um conceito novo empilhando variáveis que já venceram e testando **uma** variável nova |
| Ponto de partida | um anúncio (nosso ou da concorrência) | a biblioteca de variáveis da marca + um ou mais anúncios quebrados |
| Roteiro | tradução, mesma ordem e conteúdo | roteiro novo que segue o padrão reutilizável, com as vencedoras e a variável em teste |
| Quando usar | a referência já é forte e só precisa existir no nosso mercado; velocidade | queremos aprender o que vende e escalar; a réplica cansou; criativo nosso que não performou |
| O que deixa | o criativo + as variáveis da referência na biblioteca, como Candidate | o criativo + um teste registrado, que vira Winner ou Loser quando os números chegarem |

O dono escolhe o processo no começo. Sem escolha explícita: referência de vídeo com pedido de "traduzir", "refazer" ou "replicar" é **Réplica**; "modelar", "criar a partir de", "empilhar", "conceito novo" ou "variação de um vencedor" é **Modelagem**. Na dúvida, perguntar.

O método vem da skill *Creative Winning Variables* (ver [Origem](#origem)) e se soma ao que já usamos: o [Copy/COPY.md](Copy/COPY.md) para nível de consciência, sofisticação e lead, e o [FORMATOS.md](FORMATOS.md) para formatos e roteiro anotado. Quando o método e uma regra do projeto discordam, vale a regra do projeto (aprovação em cada etapa, gasto mínimo, fato só de `PRODUTOS.md`).

## Ideias que guiam a Modelagem

- **Todo criativo é uma pilha de variáveis**: formato da filmagem, quem fala, idade, cabelo, roupa e cor, mesa, fundo, hook, mecanismo, legenda, ritmo, oferta. Cada uma pode ganhar ou perder. Detalhe pequeno conta.
- **Criativo campeão é construído, não achado**: sai de empilhar o maior número possível de variáveis já provadas, teste a teste. Copiar um swipe 1:1 raramente é o caminho.
- **Corrida de rato**: microvariações de um vencedor (hook um pouco diferente, abertura parecida) quase nunca superam o original e gastam até ele morrer; aí culpam o produto ou a página. Variação ainda serve (o hook A/B do [COPY.md](Copy/COPY.md) seção 7), mas não escala como um conceito novo.
- **A maioria dos testes perde, e a perda também é dado**: registrar perdedoras evita testá-las de novo.
- **Todo teste tem um motivo**: uma hipótese escrita antes de gastar. Um teste "aleatório" de vez em quando é permitido, mas marcado como tal.
- **Nossos dados valem mais que swipe**: um swipe é um ponto de dado. Tempo no ar da concorrência pode ser mérito da oferta, não do criativo.
- **Hook se decide nos 3 primeiros segundos.** Métrica: hook rate = visualizações de 3 s ÷ impressões. A barra do método é acima de 50% (sugestão, ajustável aos nossos números).
- **Gastar é comprar dado**: todo teste termina numa conclusão registrada.

## Visão geral (Modelagem)

| Etapa | O que sai | Custo | Quem aprova |
|-------|-----------|-------|-------------|
| M0. Preparação | `Criativo NN/` (como na Etapa 0) + leitura da biblioteca da marca | 0 | — |
| M1. Quebra | `quebra.md` de cada anúncio base (ou link para uma quebra já feita em `Quebras/`) + linhas novas na biblioteca | 0 | dono |
| M2. Conceito | `conceito.md`: 3 testes de conceito, padrão reutilizável, mapa para a marca, plano de produção, custo, política | 0 | dono escolhe 1 teste |
| M3. Roteiro | `roteiro_<idioma>.md` anotado + `comparativo_roteiro.md` | 0 | dono, roteiro inteiro |
| M4. Produção | vídeo: Etapas 3 a 6 do `PROCESSO.md`; nativo: N3 e N4 | como na Réplica | como na Réplica |
| M5. Registro | teste com status "no ar" na biblioteca; nome do anúncio com o ID do teste | 0 | — |
| M6. Resultados | números do Gerenciador no teste; status das variáveis atualizado; nota de tier | 0 | dono |

Arquivos de um criativo de Modelagem: `referencia/` (evidências), `quebra.md`, `conceito.md`, `roteiro_<idioma>.md`, `comparativo_roteiro.md`, `prompts_imagens.md` e, se for vídeo, `takes_config.json` e `montagem.json`. Modelos em [_Modelo Criativo/](_Modelo%20Criativo/). O `analise.md` é da Réplica; na Modelagem o papel dele fica dividido entre `quebra.md` e `conceito.md`.

---

## M0. Preparação

1. Etapa 0 do `PROCESSO.md` (número, pasta, chave, modelos no ar).
2. Ler a biblioteca da marca em [Variáveis/](Variáveis/) inteira: vencedoras, perdedoras e testes em andamento. Uma variável que já perdeu não volta sem motivo novo.
3. Juntar o que existe sobre o anúncio base: é vencedor, perdedor, controle atual, não testado ou swipe? Há números (gasto, CPA, ROAS, hook rate, CTR) e os do controle? Sem números, tudo sai como Candidate; dizer isso e seguir.

## M1. Quebra do anúncio

Uma quebra por anúncio base, na ordem abaixo. Modelo: [_Modelo Criativo/quebra.md](_Modelo%20Criativo/quebra.md). Se o anúncio já foi quebrado em `Quebras/`, linkar e só completar o que faltar.

**Regra de ouro: separar o que se viu do que se acha.** Observação primeiro, julgamento depois. Valores específicos, nunca categorias: "mesa preta", não "móvel"; "mulher de uns 60, cabelo grisalho, conjunto azul-marinho florido", não "senhora".

### 1. Evidência

- **Vídeo**: `tools/analisar_referencia.py` (ver Etapa 1 do `PROCESSO.md`). Ele gera as folhas com tempo (1 quadro/s), o hook denso (`hook_3s.jpg`, um quadro a cada 0,25 s), os cortes candidatos, a transcrição com tempo por palavra e o `evidencias.md` com ritmo de cortes por trecho, palavras nos 3 primeiros segundos, palavras/s, pausas, volume e fundo sob a voz.
- **Não confiar numa assistida só**: edição rápida engana. Conferir cada corte nas folhas e completar a lista à mão no `evidencias.md` (tempo, antes → depois, duração). Ver onde os cortes se concentram: o padrão comum é apertado no hook, mais lento no corpo e apertado de novo no CTA.
- **Texto na tela** registrado à parte da fala: fonte, tamanho como fração da altura do quadro (medir, não dizer "grande"), posição, cor que codifica sentido (uma cor para alegação, outra para prova ou urgência), atraso entre o texto aparecer e a palavra ser dita.
- **Nativo**: a imagem e o texto do post, lidos pelo Chrome (passo 1 da seção "Criativo nativo" do `PROCESSO.md`).
- O que não deu para ver vai escrito ("sem áudio", "só 1 frame do hook").

### 2. Os seis elementos centrais

Uma seção curta para cada, em texto (não em tabela). Elemento ausente também é variável: dizer que falta.

1. **Avatar**: o problema exato e quando ele acontece ("acorda às 3 h toda noite"); as soluções que ela já tentou, **na ordem** em que aparecem, e por que cada uma falhou; o custo real que importa para ela; e a aposta maior que o anúncio está vendendo por trás (o casamento, a neta, a dignidade).
2. **Autoridade**: quem entrega a afirmação principal e **como ela é apresentada**. Descoberta orgânica (uma amiga leva a um grupo, ela vê a especialista ajudando outra pessoa antes de qualquer venda) soa mais crível do que "fui ao médico" ou "li um artigo". Nomear o recurso usado.
3. **UMP, mecanismo único do problema**: citar onde entra. Vem primeiro em linguagem simples e só depois o nome técnico? Tem duas camadas: (a) por que o problema é maior do que parece, (b) por que as soluções anteriores falharam, terminando numa frase que **tira a culpa** dela?
4. **UMS, mecanismo único da solução**: citar onde entra. Conferir a ordem: (a) o que uma solução de verdade precisa fazer, antes de nomear qualquer coisa; (b) a categoria da solução, sem marca; (c) os componentes, cada um ligado a uma falha do UMP. Onde a marca aparece (em textos longos, muitas vezes entre 60% e 65% do caminho) e como as versões concorrentes são desqualificadas. Fato concreto de processo ou origem vence "o nosso é melhor".
5. **Nível de consciência** (seção 2 do `COPY.md`), com a frase que prova.
6. **Sofisticação do mercado** (1 a 5, seção 2 do `COPY.md`): ganha por promessa direta ou maior (1–2), por mecanismo (3), por mecanismo melhor (4) ou por identidade e experiência (5)? Citar a frase.

Completar com o resto do diagnóstico da seção 2 do `COPY.md` (tipo de lead, crença única, 4 pés).

### 3. Variáveis de formato e produção

Trecho a trecho (hook, cada cena, transições, fecho):

- **Hook / scroll-stopper**: tipo, primeiro quadro, recurso (ex.: frase chocante + pergunta aberta), por que serve a este nicho, quantas palavras nos 3 primeiros segundos, se os 3 s fazem muito ou pouco trabalho.
- **Filmagem**: câmera de segurança, celular, podcast, selfie, estúdio, animação, IA; qualidade e resolução; ângulo e enquadramento.
- **Mensageiro**: papel, idade, gênero, etnia aparente, visual, energia, jeito de falar.
- **Cenário**: primeiro plano, fundo, objetos, lugar.
- **Figurino**: peça e cor.
- **Estrutura**: ordem dos trechos e transições (ex.: cena chocante → autoridade); formato do [FORMATOS.md](FORMATOS.md).
- **Texto na tela**: estilo, tamanho, posição, cor, tempo em relação à voz.
- **Áudio e ritmo**: voz, trilha, efeitos, ritmo de cortes, palavras/s, duração.
- **Nativo**: tipo de imagem (foto de celular ou produzida; pessoa da história, cena final, quebra de padrão ou problema em close), texto sobre a imagem, recurso de layout (lista de notas do celular, card de avaliação, tabela comparativa), cores e legenda.
- **Qualquer outra coisa**: se dá para mudar, é variável.

Hipótese comum e **não provada**: filmagem de resolução mais baixa parece mais nativa e pode escapar de uma penalização a anúncio polido demais. Fica marcada como teoria até ser testada.

### 4. Tabela trecho a trecho

Uma linha por frase ou bloco curto (um nativo longo chega a 30 linhas). Colunas: tempo (vídeo), o que é dito ou mostrado (resumo em português), **função** e elementos de atenção (vocabulário do [FORMATOS.md](FORMATOS.md)). É o roteiro anotado da Réplica com a coluna de função a mais.

Funções, com nomes simples: hook, desqualificar, aumentar a aposta, agitação, descoberta, entrada da autoridade, UMP (camada 1/2), UMS (camada 1/2/3), desqualificar concorrente, matar objeção, tirar a culpa, prova, urgência, callback, espelho de um trecho anterior, CTA, P.S.

**Callbacks** em destaque: um número ou frase plantado cedo e pago depois ("3 h da manhã" no hook que volta no fecho). Essa estrutura de plantar e pagar é das coisas que mais vale levar.

### 5. Classificar, questionar, hipótese

Cada variável relevante recebe **um** status, e só estes quatro:

| Status | Quando |
|--------|--------|
| **Winner** | venceu o controle quando era a coisa testada, ou aparece em vários vencedores nossos (nesse caso, nota "não isolada") |
| **Loser** | foi testada e perdeu com clareza |
| **Candidate** | ainda não provada: está num vencedor mas não foi isolada, está no controle ("no controle"), ou veio de swipe |
| **Random** | veio de um teste "jogar na parede", sem hipótese |

- Um anúncio vencedor não torna vencedora cada variável dele.
- Resultado a poucos % do controle com pouco gasto continua Candidate: "inconclusivo, precisa de mais gasto".
- **Variável de swipe é sempre Candidate**, por mais tempo que o anúncio esteja no ar.
- Confiança e ressalvas vão nas notas; não inventar status novo.

Para cada variável-chave: **pergunta** (por que pode funcionar com este avatar, em uma linha), **pesquisa** (bate com a biblioteca, quebras anteriores e `PRODUTOS.md`? dizer se não havia com o que comparar) e **hipótese** (uma frase que um teste pode provar falsa).

**Tier (F a S)**: mede até quanto gasto o anúncio continua lucrativo. Só sai com gasto **e** linha de lucro (CPA de break-even ou ROAS alvo, em `PRODUTOS.md`). Sem os dois, não dar tier: dizer como ele se compara ao controle e o que falta. Faixas sugeridas em [Variáveis/README.md](Variáveis/README.md).

### 6. Atualizar a biblioteca

Toda variável relevante vira linha em `Variáveis/<Marca>.md`, vencedora **e** perdedora, com fonte, evidência e hipótese. Variável que já existe ganha a evidência nova na mesma linha (e o status muda se for o caso), em vez de virar linha repetida. Regras e colunas em [Variáveis/README.md](Variáveis/README.md).

➡ **Aprovação:** o dono lê a quebra.

## M2. Conceito

Arquivo `conceito.md` (modelo em `_Modelo Criativo/conceito.md`).

1. **Testes de conceito** (3, salvo pedido diferente). Conceito novo, não microvariação. Cada um no bloco:

   ```
   Teste: <ID da biblioteca, ex.: CIN-T004> — <nome curto>
   Vencedoras empilhadas: <IDs e valores da biblioteca, ou "nenhuma provada ainda" + o que fica constante>
   Variável em teste: <variável: valor atual → valor novo>
   Hipótese: <a frase falseável>
   Vence se: <resultado contra o controle ou o melhor anúncio>
   Perde se: <resultado que mata a variável>
   Métricas: <hook rate (barra: acima de 50%), CTR, CPA/ROAS>
   Tipo: Deliberado | Aleatório
   Formato e produção: <formato do FORMATOS.md, imagens e takes, custo estimado>
   ```

   **Uma variável por teste**: muda só ela, o resto fica igual. Exemplo: manter a abertura com cena chocante e o cenário de podcast e testar a idade da autoridade; depois o gênero, um de cada vez.
2. **Padrão reutilizável**: os movimentos estruturais do anúncio base como **instruções numeradas**, não observações ("o hook abre em X", "a autoridade chega por Y", "o UMP vem em duas camadas, nesta ordem", "a marca aparece por último", "o número plantado volta no fecho", "o fecho volta à aposta que o hook abriu").
3. **Mapa para a marca**: cada movimento ligado à marca, trecho a trecho, a ponto de servir de briefing, com a linha candidata escrita (marcada como rascunho).
   - **Avatar**: da pesquisa real de clientes. Nunca um avatar inventado; sem pesquisa, listar o que falta.
   - **Autoridade**: um caminho de descoberta real e crível para a marca. Se não existe, é lacuna. **Nunca inventar especialista, credencial ou citação.**
   - **UMP / UMS**: só mecanismos que `PRODUTOS.md` e fontes verificáveis sustentam (ex.: bisglicinato puro, zéro oxyde). Se o diferencial real da marca é mais fraco que o da referência, dizer.
   - **Callbacks e fecho**: um número ou frase real da marca para plantar cedo e pagar no fim.
4. **Plano de produção**: formato, guia `FORMATO.md`, texto na tela (tabela do `PROCESSO.md`), imagens, takes e custo, como a análise da Réplica.
5. **Política e perguntas abertas**: riscos avisados uma vez (decisão do dono registrada); fatos que faltam em `PRODUTOS.md`.

➡ **Aprovação:** o dono escolhe o teste (ou pede outro). O escolhido entra na tabela de testes da biblioteca com status "proposto".

## M3. Roteiro

Para o teste escolhido:

1. Seguir o padrão reutilizável **instrução por instrução**, com as vencedoras empilhadas mantidas e só a variável em teste trocada.
2. Mesmo peso emocional e mesmos elementos de atenção nas mesmas posições (a tabela trecho a trecho é o esqueleto). Trocar o tema mantém o peso: onde havia um conflito universal, outro tão forte; onde havia uma referência conhecida, outra tão conhecida no país.
3. **Nada inventado que pareça fato**: número, estudo, pessoa real e citação só com fonte verificável (link no roteiro); fato do produto só de `PRODUTOS.md`; sem fonte, fica de fora.
4. Entregar anotado frase a frase (função + elementos) e com a tradução de volta para o português (`comparativo_roteiro.md`). Quando a ideia ainda está aberta, propor antes 2 ou 3 ideias curtas (tema novo, estrutura, formato) para o dono escolher. Seguir "Como escrever o roteiro" do `FORMATO.md` do formato escolhido.
5. Hooks e ângulos: seções 3 e 7 do `COPY.md`. Checklist da seção 9 antes de aprovar.
6. Mesma copy em outro formato (como o 11, copy do 03 em Palestrinha): a copy não muda, a variável em teste é o formato; pular para M4.

➡ **Aprovação:** roteiro inteiro.

## M4. Produção

Igual à Réplica: vídeo pelas Etapas 3 a 6 do `PROCESSO.md` (imagens uma a uma, takes, montagem), nativo pelas etapas N3 e N4. O que é constante no teste precisa ficar constante também na produção: se o teste é a idade da autoridade, cenário, figurino e enquadramento são os mesmos do controle.

## M5. Registro do teste

- Na entrega, o teste muda para "no ar" na tabela de testes da biblioteca, com o número do criativo.
- Nome do anúncio no Gerenciador: `<código> | <ID do teste> | <variável>: <valor>`, com o código do criativo (C03, CN05, CI01) (ex.: `C15 | CIN-T004 | autoridade: idade 40 → 65`). É o que liga o resultado ao teste, à mão hoje e automaticamente quando o projeto subir campanhas.
- Seguir "Ao entregar um criativo" do `PROCESSO.md`.

## M6. Resultados

Quando o dono trouxer os números (print ou exportação do Gerenciador): gasto, impressões, visualizações de 3 s (hook rate), CTR, CPA ou ROAS, do criativo **e do controle**, no mesmo período.

1. Gravar os números no teste (coluna "Resultado") e mudar o status: vencedor, perdedor ou inconclusivo.
2. Atualizar o status das variáveis pelas regras da M1, passo 5: a variável testada vira Winner ou Loser; as empilhadas ganham mais uma evidência.
3. Tier, se houver linha de lucro.
4. Perdedor: rodar o **modo reverso** antes de desistir do conceito.

---

## Quebra avulsa (sem produção)

Para alimentar a biblioteca sem fazer criativo: um swipe da Biblioteca de Anúncios, um vencedor nosso, um perdedor nosso. Faz só a M1 e grava em:

```
Quebras/<Marca>/<AAAA-MM-DD> <anunciante> - <tema>/
├─ quebra.md
└─ referencia/      evidências (fora do Git as mídias, como nos criativos)
```

Termina com os 3 testes de conceito propostos (passo 1 da M2), para o anúncio não parar na análise. É a unidade de trabalho que a mineração automática vai produzir.

## Modo reverso: diagnosticar um criativo nosso que não performou

1. Fazer a M1 no nosso anúncio.
2. Comparar cada variável com a biblioteca e com as quebras anteriores.
3. Ordenar os suspeitos: **um** suspeito principal, depois os outros em ordem. Não uma lista solta.
4. Propor a menor correção isolada que testa o suspeito principal (vira um teste na biblioteca).
5. **Não culpar produto, mercado ou página primeiro.** Ver antes se as variáveis do criativo foram isoladas e testadas. Na maioria das vezes, foi o criativo.

## Saída de uma quebra (ordem)

1. Evidências: o que foi usado e o que não deu para ver.
2. Os seis elementos centrais.
3. Variáveis de formato e produção.
4. Tabela trecho a trecho.
5. Classificação, hipóteses e tier (ou o que falta para ele).
6. Linhas da biblioteca (novas e atualizadas).
7. Testes de conceito (3).
8. Padrão reutilizável e rascunho para a marca (na quebra avulsa, só o padrão e o que falta para o rascunho).
9. Lacunas: os dados que transformariam Candidates em Winners ou Losers.

Mesmo num pedido rápido: cada seção mais curta, mas nunca sem classificação, testes e lacunas.

## Erros comuns

- Chamar uma variável de vencedora por causa de um anúncio, ou um swipe de vencedor pelo tempo no ar.
- Registrar só o que ganhou.
- Testar sem motivo e depois não saber o que causou o resultado.
- A corrida de rato: microvariação atrás de microvariação do mesmo vencedor.
- Culpar produto, mercado ou página antes de isolar as variáveis do criativo.
- Pular detalhe "pequeno" (cor da roupa, fundo).
- Parar na análise sem testes e sem rascunho.
- Inventar dor de cliente, especialista ou mecanismo para preencher o mapa da marca.

## Origem

Método adaptado da skill *Creative Winning Variables* (arquivos `SKILL.md` e `references/video-evidence.md`, recebidos pelo dono em 2026-11-24). Aqui o método foi reescrito em português e encaixado no fluxo do projeto: as evidências saem do `analisar_referencia.py`, o diagnóstico de copy vem do `COPY.md`, os formatos do `FORMATOS.md`, e as aprovações e regras de gasto e de fatos do `PROCESSO.md`. A antiga Etapa 2b (roteiro novo a partir de um vencedor) virou a M3 deste processo.
