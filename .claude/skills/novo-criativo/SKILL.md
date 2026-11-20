---
name: novo-criativo
description: Start or continue a video creative in this project (reference video → translated script → AI images → AI takes → local montage), following PROCESSO.md with approval gates and minimal API spend. Use when the user says "novo criativo", names a "Criativo NN", drops a new reference video in "Vídeo Bruto/", or asks to continue a creative's next stage.
---

# Novo criativo

1. Read `PROCESSO.md`, `CLAUDE.md` and `PRODUTOS.md` at the project root. They are the source of truth for every step, tool command, naming convention, product fact and rule.
2. Read `CRIATIVOS.md` and pick the closest existing creative by format. Use its folder (analise, prompts, takes_config, montagem.json, production notes) as the template for decisions.
3. Identify the creative:
   - New: ask only for what is missing among: creative number (`Criativo NN`, the next free folder number, not the reference file's number), reference file in `Vídeo Bruto/`, target language, target country, product (and whether packaging or claims change), and whether the format follows the reference or another one. Then do Etapa 0 (copy `_Modelo Criativo/` into `Criativo NN/`, check that the video model is up).
   - Existing: open `Criativo NN/` and work out the current stage from the files present (analise.md, roteiro, imagens, takes, montagem) and the "Notas de produção" in the roteiro. Tell the user where it stands and what comes next. If images or takes are missing because media is not in Git, ask the user to copy them from the team's shared folder.
4. Run the next stage exactly as PROCESSO.md describes, then stop at its approval gate and present the result in Portuguese (with back-translation of any foreign-language text, costs estimated before and spent after).
5. When the creative is delivered, update its production notes, its row and lessons in `CRIATIVOS.md`, any newly confirmed product fact in `PRODUTOS.md`, and document any new tool or option in `PROCESSO.md`.
