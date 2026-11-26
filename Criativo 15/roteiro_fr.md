# Roteiro FR — Criativo 15 (Modelagem do 03: Conflito situacional)

Processo: **Modelagem** ([MODELAGEM.md](../MODELAGEM.md)), teste **CIN-T004** (ver [conceito.md](conceito.md)).
Base: [Criativo 03](../Criativos%20Exemplo/Narrado/Criativo%2003/roteiro_fr.md) e a quebra dele ([quebra.md](../Criativos%20Exemplo/Narrado/Criativo%2003/quebra.md)).
Formato: **Conflito situacional** (formato 08 do `FORMATOS.md`, primeiro nosso; guia em [Conflito situacional/FORMATO.md](../Criativos%20Exemplo/Conflito%20situacional/FORMATO.md)).

**Variável em teste**: a abertura. O 03 começa direto na prancheta com a voz; o 15 abre com **3 s de cena encenada, sem fala**, e só depois entra o 03 **inteiro e sem nenhuma mudança** (o arquivo final, com legenda).

Adaptações em relação ao 03:
1. Cena H0 de 3 s antes do vídeo. Nenhuma palavra nova: a primeira frase do 03 ("Si votre glycémie vous fait pisser 3 fois par nuit…") faz a ponte entre a cena e a prancheta.

## Cena H0 (0–3 s, sem fala)

Quarto francês às escuras, luz azulada da noite pela janela. Uma mulher de ~60 anos, cabelo grisalho curto despenteado, camisola de algodão rosa-claro, senta de uma vez na beira da cama, cansada, a mão na testa. No primeiro plano, na mesa de cabeceira, um **despertador digital com números vermelhos marcando 03:07**. Ela se levanta e anda em direção à porta entreaberta do banheiro, de onde vem uma faixa de luz amarela. Ao lado dela, o marido dorme de costas, imóvel.

- Por que essa cena: é o painel 1 do 03 ("Pisser 3 fois par nuit ?") virando realidade, com uma mulher da idade do público. O 03:07 é a imagem do "toda noite de novo".
- Som: ambiente baixo do take (respiração, lençol, passos). Se o modelo puser fala ou música, `"silent": true` e o corte seco para a voz do 03.
- Legenda: nenhuma na cena (o primeiro texto na tela é o da prancheta).

| Take | Imagem | ~s | Fala (FR) |
|------|--------|----|-----------|
| H0 | H0 | 3 | (sem fala) |
| 05 | — | 62,6 | o Criativo 03 inteiro: `Vídeos Prontos/Criativo 03 - FR.mp4` |

Duração esperada: ~65,6 s.

## Roteiro anotado

| Tempo | O que acontece | Função | Elementos |
|-------|----------------|--------|-----------|
| 0–3 s | mulher acorda às 03:07 e vai ao banheiro | hook visual (conflito encenado) | [Gancho visual + Conflito + Identificação: a cena que ela vive toda noite; Curiosidade: "por que isso acontece?"] |
| 3 s em diante | 05 inteiro | ver quebra do 03 | a primeira frase do 03 vira a **ponte**: nomeia a cena que acabou de ser vista e já dá a causa (efeito a-há) |

## Checklist (COPY.md, seção 9)

- A cena tem ligação clara com a mensagem (o primeiro sintoma do 03). ✔ Não é isca.
- Primeiro quadro: rosto de mulher da idade do público + 03:07 vermelho no escuro. ✔
- Encenada, sem parecer notícia ou acidente. ✔

## Notas de produção

- H0: imagem Nano Banana 9:16 (`H0_v1.png`) e take Omni 360p de 3 s sem fala, a partir dela.
- Montagem: H0 escalado para 1080x1920 + o arquivo final do 03, emendados com FFmpeg (corte seco). Sem passar o 03 pelo `montar.py` de novo.
- Se o 03:07 sair deformado no take, colar o despertador nítido da imagem por cima (`colar_produto.py` + overlay `patch`), custo 0.
- H0 (2026-11-24): imagem na primeira tentativa (US$ 0,04); take de 3 s no Omni 1.1 (o 1.2 estava fora do ar), US$ 0,10, sem fala (volume -91 dB), relógio 03:07 nítido o take inteiro.
- Montagem: H0 escalado para 1080x1920 com áudio mudo + o arquivo final do 03, emendados com FFmpeg (`concat`). 65,6 s, -13,6 LUFS. `Vídeos Prontos/Criativo 15 - FR.mp4`.
- Custo total: US$ 0,14.
