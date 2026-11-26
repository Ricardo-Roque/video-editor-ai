# Formato: Palestrinha (quadro branco)

Formato 03 do quadro do Trello (ver [FORMATOS.md](../../FORMATOS.md)). O quadro também aceita slide, TV ou notebook como apoio visual; o que importa é o visual **provar o ponto** enquanto a pessoa fala, o que dá autoridade.

No nosso exemplo, uma apresentadora fala direto para a câmera, de pé na frente de um quadro branco escrito à mão, como numa mini-aula. Ela aponta para o que está escrito enquanto fala, e o quadro ganha linhas novas no meio do vídeo. O produto aparece na mão dela na apresentação e no CTA.

Usado para levar uma copy que já vendeu para um visual novo: o Criativo 11 é a copy do [Criativo 03](../Narrado/Criativo%2003/) sem mudar uma palavra.

## Exemplo

| Criativo | Duração | Custo | Ver primeiro |
|----------|---------|-------|--------------|
| [C11](Criativo%2011/) | 62,0 s | ~US$ 3,02 | `referencia_formato/` (análise do formato), imagens de partida com o gesto de apontar, `quadro_nitido.py` |

A referência de formato foi `Vídeo Bruto/Criativo #10.mp4` (japonês, canela × metformina, apresentador homem). Não é a referência da pasta 10.

## Como o formato funciona

- **Câmera**: tripé fixo, plano médio (cabeça até a coxa), vertical. Jump cuts quando a pessoa muda de posição; um corte seco quando o quadro muda de estado.
- **Quadro**: letra de mão grande, poucas palavras, desenhos simples, em colunas. Dois estados (Q-A e depois Q-B com linhas novas).
- **Texto do quadro no terço de cima**, acima da cabeça, para a legenda e a pessoa não cobrirem.
- **Gesto**: ela aponta para a linha que está falando. O dono pediu isso explicitamente e aprovou.

## Como escrever o roteiro

Quando a copy não vem pronta da referência:
- Moldura de **aula**: "Bem-vindo à aula de hoje: ..." ou "X contra Y"; o quadro mostra o tema.
- Abrir com curiosidade dirigida a quem assiste ("se te mandaram este vídeo, é porque...").
- Lista de 3 a 5 itens; cada item = situação familiar + efeito a-há + uma linha no quadro.
- Contraste em colunas (errado × certo, antes × depois) funciona muito bem no quadro.
- O produto entra como o último item ou a conclusão da aula, não como interrupção.

## Receita de produção

- **Personagem**: apresentadora nova (50+ no 11), visual realista de iPhone, nada de modelo. Passar um frame da referência como segundo `--ref` ajudou no enquadramento e na luz.
- **Imagens de partida**: uma por linha do quadro, já com o canetão na linha certa (C1 linha 1, C2 linha 2...). Variações saem editando a cena base. Manter também uma versão do quadro **sem mão sobre o texto**: é a base do `quadro_nitido.py`.
- **Takes**: Omni 1.2 Flash 360p, mesma persona e seed; personas `point1`, `point2`... descrevem o gesto. Testar o T01 antes do lote (voz, rosto, gesto).
- **Texto do quadro**: em 360p o modelo escreve errado ("Muits", "glycémie sinble"). Corrigir com `quadro_nitido.py`: cola o texto nítido da imagem quadro a quadro e mantém do take a mão, o canetão e o cabelo. Saída já em 1080x1920.
- **Prova social**: clipes UGC curtos (U1–U4, mulheres 50+ com o sachê) cortados sobre a voz do T07. O dono preferiu vídeo a foto parada. O Omni 1.2 não aceita `--no-audio` (HTTP 400): gerar com áudio e descartar na montagem.

## Cuidados

- **Política**: aqui a apresentadora faz alegação de saúde em primeira pessoa, na tela. É um risco maior que a mesma copy em narração em off.
- O modelo continua falando depois do fim da fala (T01 inventou "Mes saucères du synate."): cortar numa pausa real.
- `--region` do `quadro_nitido.py` muda por take (até onde vai o quadro sem cobrir o pacote); anotar nas notas de produção.
