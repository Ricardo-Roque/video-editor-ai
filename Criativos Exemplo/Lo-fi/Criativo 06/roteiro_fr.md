# Roteiro FR — Criativo 06 (decupagem por take)

Base: transcrição da referência (`referencia/transcript.txt`), traduzida para o francês falado, mesma ordem, sem cortes nem acréscimos.
Decisão do usuário: copy idêntica à referência, com todas as alegações e sem a menção "Image virtuelle", assumindo o risco.

Adaptações (só o que não existe ou não faz sentido na França):
1. "SPN Nutrition" virou "Cinnarae" (produto do usuário).
2. "Give it a go" virou "je vous conseille d'essayer" (registro "vous", padrão dos criativos do usuário; "I suggest" já está na frase original).

⚠ = alegação de risco (Reg. UE 1924/2006, DGCCRF, política da Meta). Mantidas por decisão do usuário.

| Take | Imagem | ~s | Fala (FR) |
|------|--------|----|-----------|
| T02 | B1 | 11 | Ça, c'est moi à 72 ans, et je me sens 10 ans plus jeune. Et c'est en grande partie grâce à Cinnarae, qui me donne de l'énergie. Alors je vous conseille d'essayer. ⚠ |

T01 (H1, ~3 s, sem fala): ela se levanta do chão de um impulso e fica em pé de frente para a câmera, o homem ri ao fundo. Gerado à parte com `tools/gerar_take.py` (o lote só lê takes com fala).

Total estimado: ~14 s de takes brutos; final esperado ~13 s (igual à referência).

## Notas de produção

- A referência é um plano-sequência; aqui vira 2 takes (levantar + falar) com corte seco quando ela fica em pé.
- B1_v2 = recorte local da B1_v1 (joelhos para cima, como na referência), custo 0.
- T01 gerado com `gerar_take.py` (3 s, sem fala); na montagem entra com `"silent": true`.
- Brand ouvida pelo whisper como "Synaret" (mesma pronúncia "Si-na-rê" aceita no Criativo 05).
- Montagem v1: `Vídeos Prontos/Criativo 06 - FR.mp4`, 13,4 s.
