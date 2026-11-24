---
name: quebra-de-variaveis
description: Break an ad down into its winning variables without producing a creative, diagnose one of our underperforming creatives, or log ad results into the brand's winning-variables library. Follows MODELAGEM.md (evidence, six core elements, production variables, beat table with jobs, Winner/Loser/Candidate/Random, library update, one-variable concept tests, reusable pattern). Use when the user says "quebra", "quebrar o anúncio", "por que esse anúncio vende", "variáveis vencedoras", "diagnosticar o criativo NN", "não performou", "resultados do criativo", sends Ads Manager numbers for a creative, or asks to update the library in "Variáveis/".
---

# Quebra de variáveis

1. Read `MODELAGEM.md`, `CLAUDE.md`, `PRODUTOS.md`, `Variáveis/README.md` and the brand's library `Variáveis/<Marca>.md` (Cinnarae if not said). Reply in Portuguese, back-translating any foreign-language text.
2. Work out which of the three jobs this is, and ask only for what is missing (the ad, what it is: winner / loser / control / untested / swipe, performance numbers and the control's, brand). Missing numbers never block the work: say every variable will be Candidate and go on.

## Quebra avulsa (breakdown only)

- Folder: `Quebras/<Marca>/<AAAA-MM-DD> <anunciante> - <tema>/`, with `quebra.md` from `_Modelo Criativo/quebra.md` and a `referencia/` folder.
- Video: run `python -I -X utf8 tools/analisar_referencia.py --video "<file>" --out "<folder>/referencia" --language <code>` and look at `hook_3s.jpg`, the timestamped sheets and `evidencias.md` before writing. Confirm the cut list by eye and fill the "Conferido no olho" part of `evidencias.md`.
- Native (Ad Library link): read it with Claude in Chrome as in "Criativo nativo" step 1 of `PROCESSO.md`; save the image and `fonte.md`, never the third-party ad text itself.
- Write the breakdown in the order of "Saída de uma quebra" in `MODELAGEM.md`: evidence, six core elements, production variables, beat table with jobs and callbacks, classification with question / research / hypothesis, tier or what is missing for it, library rows, 3 concept tests, reusable pattern, gaps. Observation before judgment; specific values, never categories.
- Add or update rows in `Variáveis/<Marca>.md`, keeping the fixed columns and never reusing an ID. Add the proposed tests to the tests table with status `proposto` only if the user picks one.

## Modo reverso (our underperformer)

Same breakdown on our own creative (`Criativos Exemplo/<formato>/Criativo NN` or the root), then compare each variable with the library and past breakdowns, rank one primary suspect and the rest in order, and propose the smallest isolated fix as a test. Do not blame product, market or landing page before checking whether the creative's variables were ever isolated.

## Resultados (numbers for a creative)

Record spend, impressions, 3-second views (hook rate = 3 s views / impressions), CTR, CPA or ROAS for the creative and the control in the same period in the test's "Resultado" cell; set the test status (`vencedor`, `perdedor`, `inconclusivo`); update the tested variable to Winner or Loser and add the evidence to the stacked ones, following step 5 of M1 in `MODELAGEM.md` (a result within a few percent on little spend stays inconclusive). Give a tier only when `PRODUTOS.md` has the break-even CPA or target ROAS. For a loser, offer the reverse mode.

## Always

- Never invent data, experts, credentials, quotes or mechanisms; product facts only from `PRODUTOS.md`.
- Flag ad-policy risks once (health claims, before/after bodies, timeframes, fabricated testimonials or authority).
- Show the finished write-up in the chat too, not only in the file. The work costs nothing (no paid API calls).
- Offer commit and push when done.
