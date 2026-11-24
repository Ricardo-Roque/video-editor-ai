# Biblioteca de variáveis

Uma biblioteca por marca (`<Marca>.md`), com toda variável de criativo que já analisamos ou testamos: as que ganharam **e** as que perderam. É lida antes de toda quebra e de todo conceito novo, para as variáveis se acumularem em vez de recomeçar do zero. O método está em [MODELAGEM.md](../MODELAGEM.md).

| Marca | Arquivo |
|-------|---------|
| Cinnarae (França) | [Cinnarae.md](Cinnarae.md) |

Marca nova: copiar o `Cinnarae.md`, apagar as linhas e trocar o prefixo dos IDs.

## Formato fixo

As duas tabelas de cada arquivo têm colunas fixas, na ordem abaixo. Não acrescentar nem renomear colunas: a mineração automática e a interface do projeto vão ler esses arquivos. Uma variável por linha; `|` dentro de célula vira `/`.

### Variáveis

`| ID | Categoria | Variável | Valor | Status | Fonte | Evidência | Hipótese | Data | Notas |`

- **ID**: prefixo da marca + `V` + número sequencial (`CIN-V001`). Nunca reaproveitar um ID.
- **Categoria**: Avatar, Autoridade, UMP, UMS, Consciência, Sofisticação, Lead, Hook, Formato, Filmagem, Mensageiro, Cenário, Figurino, Estrutura, Texto na tela, Áudio e ritmo, Imagem (nativo), Prova, Oferta, CTA.
- **Valor**: específico ("mesa preta", "mulher de uns 60, cabelo grisalho, conjunto azul-marinho"), nunca uma categoria.
- **Status**: só `Winner`, `Loser`, `Candidate` ou `Random` (definições na M1, passo 5, do `MODELAGEM.md`).
- **Fonte**: `Criativo NN` (nosso), `swipe <anunciante> <ID da Biblioteca de Anúncios>` ou o caminho da quebra em `Quebras/`.
- **Evidência**: resultado contra o controle, com números e período. Sem números: "sem dados".
- **Data**: da última mudança na linha (AAAA-MM-DD).
- **Notas**: confiança e ressalvas ("não isolada", "no controle", "inconclusivo, precisa de mais gasto", "swipe", risco de política).

Variável que reaparece ganha a evidência nova na mesma linha; não duplicar.

### Testes de conceito

`| Teste | Data | Criativo | Vencedoras empilhadas | Variável em teste | Hipótese | Vence se | Perde se | Status | Resultado |`

- **Teste**: prefixo + `T` + número (`CIN-T001`). O mesmo ID vai no nome do anúncio no Gerenciador: `C<NN> | <ID> | <variável>: <valor>`.
- **Vencedoras empilhadas**: IDs das variáveis da tabela acima.
- **Variável em teste**: `<variável>: <valor atual> → <valor novo>`.
- **Status**: `proposto`, `em produção`, `entregue` (pronto, sem confirmação de que está no ar), `no ar`, `vencedor`, `perdedor`, `inconclusivo`.
- **Resultado**: gasto, hook rate, CTR, CPA/ROAS do criativo e do controle, com o período.

## Status em uma linha

- **Winner**: venceu o controle quando era a coisa testada, ou aparece em vários vencedores nossos ("não isolada").
- **Loser**: testada e perdeu com clareza.
- **Candidate**: não provada; inclui toda variável de swipe e toda variável do controle ainda não isolada.
- **Random**: veio de teste sem hipótese.

## Tier (F a S)

O tier mede até quanto gasto um anúncio continua lucrativo. Precisa do gasto e da linha de lucro (CPA de break-even ou ROAS alvo da marca, em [PRODUTOS.md](../PRODUTOS.md)). Faixas **sugeridas**, a ajustar pelo dono:

| Tier | Gasto lucrativo acumulado |
|------|---------------------------|
| F | nunca ficou lucrativo |
| D | até ~500 € |
| C | até ~5.000 € |
| B | até ~25.000 € |
| A | até ~100.000 € |
| S | acima de ~100.000 € |

## Métricas

- **Hook rate** = visualizações de 3 s ÷ impressões. Barra do método: acima de 50% (sugestão).
- **CTR** (cliques no link ÷ impressões), **CPA** (custo por compra), **ROAS** (receita ÷ gasto).
- Comparar sempre com o controle (o melhor anúncio no ar) no mesmo período.
