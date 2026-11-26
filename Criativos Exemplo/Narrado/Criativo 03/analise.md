# Análise — Criativo 03

Fonte: `Vídeo Bruto/Criativo #05.mp4`
Formato: 9:16, 360x640, 30 fps, 58,5 s, áudio AAC. Idioma: inglês.
Transcrição completa com timestamps: `referencia/transcript.txt`.
Produto do novo criativo: **Cinnarae** (gomas de bisglicinato de magnésio, framboesa, ursinhos vermelhos; foto do pacote em `Referências/`). País: França. Idioma: francês.

## Formato geral

Narração em off (voz feminina, primeira pessoa) sobre um infográfico impresso numa prancheta, com uma varinha de madeira apontando cada painel. Depois vêm uma montagem rápida de mulheres segurando o produto e B-roll do pacote. **Ninguém fala para a câmera**: não há sincronia labial.

## Estrutura

| # | Tempo | Bloco | Cenário / enquadramento | Fala (resumo) |
|---|-------|-------|-------------------------|---------------|
| 1 | 0,0–26,8 | HOOK — 3 problemas | Plano fixo de cima: prancheta com o infográfico 1 ("Why Magnesium Bisglycinate Matters"), 3 painéis ilustrados (homem indo ao banheiro à noite / mulher com boca seca / mulher sem conseguir dormir). A varinha aponta o painel que está sendo falado. | "Se o açúcar no sangue te faz mijar 3x por noite… / se acorda com a boca seca como um deserto… / se não consegue dormir a noite toda… tome bisglicinato de magnésio." |
| 2 | 26,8–29,2 | PRODUTO | Mão segurando o pacote, bancada de cozinha. | "E eu uso as gomas de bisglicinato de magnésio da SP Nutrition." |
| 3 | 29,2–43,9 | BODY — uso e resultado | Infográfico 2 na prancheta (sem açúcar / tome duas antes de dormir / durmo a noite toda), mesma varinha. | "Sem açúcar e suaves para o estômago. Tome duas antes de dormir. Agora durmo a noite toda, sem idas ao banheiro, sem boca seca. Acordo descansada e com energia." |
| 4 | 43,9–49,5 | PROVA SOCIAL | 5 cortes de ~1 s: mulheres diferentes segurando o pacote (cozinha, varanda, cama) e o pacote numa mesa. | "Mais de 120.000 mulheres já tomam isso toda noite… e sempre esgota rápido." |
| 5 | 49,5–58,5 | CTA — garantia e oferta | B-roll do pacote: duas mãos segurando, dedo no pacote (close), pacote aberto com as gomas vermelhas. | "Se não sentir diferença em 30 dias, devolvemos o dinheiro. Clique no link para 20% off no primeiro pedido." |

Cortes secos: 26,81 · 29,25 · 30,45 · 43,88 · 44,88 · 45,88 · 46,88 · 47,88 · 49,48 · 51,81 · 54,25 · 55,98 s. Entre 0 e 26,8 s e entre 30,5 e 43,9 s não há corte (plano contínuo da prancheta).

## Estilo de edição

- Legenda: 1 a 3 palavras, amarela, centro do quadro. É praticamente o nosso padrão do `montar.py`.
- O texto do infográfico é a maior parte do visual e precisa estar em francês.
- O produto aparece em ~35% do vídeo.
- Áudio: uma narradora só, ritmo calmo e confiante.

## Imagens necessárias (o usuário gera, a partir dos meus prompts)

Infográficos (prancheta vista de cima, mesmo estilo de ilustração):
1. **Q1a / Q1b / Q1c**: infográfico 1 com a varinha apontando o painel 1, 2 ou 3. O mínimo é uma imagem (Q1), com a varinha sobre o painel 1.
2. **Q2a / Q2b / Q2c**: infográfico 2, com a varinha na linha "sem açúcar", "tome duas" ou "durmo a noite toda". O mínimo é uma imagem (Q2).

Produto (B-roll, foto do pacote Cinnarae como ref):
3. **R1**: mão segurando o pacote, bancada de cozinha francesa.
4. **R2**: pacote em pé numa mesa, com uma vela ao lado.
5. **R3**: duas mãos segurando o pacote de frente, em close.
6. **R4**: close do pacote com um dedo de unha pintada tocando o rótulo.
7. **R5**: pacote aberto na mão, mostrando as gomas vermelhas.

Prova social (mulheres francesas diferentes segurando o pacote):
8. **F1**: cozinha, camiseta branca, ~45 anos, cabelo castanho.
9. **F2**: varanda/terraço, camisa branca, ~45 anos, sorrindo para a câmera.
10. **F3**: quarto, pijama, sentada na cama.
11. **F4**: sala, segurando o pacote perto do rosto.

Texto dos infográficos: se a ferramenta de imagem errar acentos ou letras, gere as pranchetas **sem texto** e eu aplico o texto em francês localmente, sem custo.

## Takes estimados

- Os 8 takes de narração (4 a 12 s cada, ~75 s brutos) são gerados a partir da imagem da própria cena. A narradora fica fora de quadro, com a mesma persona e a mesma seed em todos.
- Se o take deformar o texto do quadro, a imagem estática entra por cima (overlay em tela cheia) e do take só se aproveita a voz. Esse caso não exige mudança no `montar.py`.
- A montagem rápida (F1–F4) e as trocas de B-roll (R4, R5) entram como overlays estáticos de ~1 s, sem custo.
- Custo estimado (360p, ~US$ 0,023/s): ~75 s × 0,023 ≈ **US$ 1,75**. Com teste e correções, **~US$ 2,20**. Imagens: US$ 0 (geradas pelo usuário).

## Adaptações culturais para a França

- "SP Nutrition" vira "Cinnarae".
- Tratamento por "tu", que é o padrão de UGC/TikTok francês para um anúncio que fala direto com quem assiste.
- Cozinha e cômodos franceses nas imagens R e F (armários claros, azulejo metrô, janelas com venezianas), sem nada americano.
- Garantia de 30 dias e 20% off no primeiro pedido: mantidos (o usuário confirmou a garantia).

## Alertas de política (decisão do usuário: manter a copy agressiva)

- **Glicemia e insulina** (T01, T02): na UE não há alegação autorizada de efeito do magnésio sobre o açúcar no sangue (Reg. 1924/2006). Risco alto de reprovação e de DGCCRF.
- **"Pisser"** (mijar): linguagem vulgar, reduz a entrega na Meta.
- **Depoimento em primeira pessoa** ("je dors d'une traite") com narradora e mulheres geradas por IA: depoimento fabricado. A lei francesa de influenciadores (Loi 2023-451) pede a menção "Image virtuelle".
- **"Sans sucre"** é alegação nutricional regulada (máx. 0,5 g de açúcar por 100 g). Só pode ficar se for verdade para a Cinnarae.
- **"Plus de 120 000 femmes"** precisa ser verdade. Se não for, é prática comercial enganosa.
