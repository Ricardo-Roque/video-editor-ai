# Meta: métricas e publicação pausada

O painel (`tools/painel.py`) e o `tools/meta.py` usam a Marketing API da Meta com um token de **usuário do sistema** da sua BM. Com o token:

- **Métricas**: compras, ROAS, custo por compra, CTR do link, gancho (views de 3 s), thruplay e curva de retenção de cada anúncio, por dia, gravados no Supabase. O painel sincroniza sozinho a cada hora enquanto estiver aberto (`META_SYNC_MIN` muda o intervalo).
- **Publicação**: sobe um criativo como anúncio **PAUSADO** num conjunto que já existe. Ativar é sempre com você, no Gerenciador.

Cada pessoa configura uma vez no próprio computador. O token fica só no `.env`. Nunca o cole no chat, no Git ou no painel.

## 1. Criar o app (5 min)

1. Entre em [developers.facebook.com](https://developers.facebook.com) com o Facebook que administra a BM.
2. **Meus apps > Criar app**. Caso de uso: **Outro**. Tipo: **Empresa**. Nome: por exemplo `Criativos <sua marca>`. Vincule ao seu **portfólio empresarial** (a BM).
3. No painel do app, em **Adicionar produtos**, adicione **API de Marketing**.
4. O app pode ficar em **modo de desenvolvimento**. Para mexer só nas contas da sua própria BM, não precisa de revisão da Meta.

## 2. Criar o usuário do sistema (5 min)

1. Em [business.facebook.com/settings](https://business.facebook.com/settings): **Usuários > Usuários do sistema > Adicionar**.
2. Nome: `agente-criativos`. Função: **Funcionário**. Não precisa ser administrador.
3. Em **Atribuir ativos**, dê só o necessário. Não precisa dar "full" em tudo:

| Ativo | Permissão |
|---|---|
| Conta de anúncios usada nos testes | **Gerenciar campanhas** (ler números e criar anúncio pausado) |
| Página que assina os anúncios | **Criar anúncios** (ou "Anunciar") |
| Conjunto de dados / pixel | **Ver** |
| O app criado no passo 1 | **Gerenciar app** (Contas > Apps > adicionar pessoas) |

## 3. Gerar o token

1. Ainda no usuário do sistema: **Gerar novo token**.
2. App: o do passo 1. Validade: **Nunca expira**.
3. Permissões: `ads_read`, `ads_management`, `business_management`, `pages_show_list`, `pages_read_engagement`. Se aparecer, marque também `pages_manage_ads`.
4. Copie o token **direto para o `.env`**, sem passar pelo chat.

## 4. `.env`

```
META_ACCESS_TOKEN=EAAG...            # o token do passo 3
META_AD_ACCOUNT_ID=act_1234567890    # Gerenciador > conta de anúncios > ID, com "act_" na frente
META_PAGE_ID=1234567890              # página > Sobre > ID da página (só para publicar)
# META_IG_USER_ID=                   # opcional: conta do Instagram ligada à página
# META_SYNC_MIN=60                   # intervalo da sincronização automática
```

Confira tudo com:

```
python -I -X utf8 tools/meta.py verificar
```

Ele mostra de quem é o token, as permissões, a conta (moeda, fuso) e a página. Sem `META_AD_ACCOUNT_ID`, lista as contas que o token enxerga.

## 5. Ligar anúncios a criativos

O anúncio é ligado ao criativo pelo **nome**, que começa com o ID do criativo:

```
C19 | CIN-T003 | hook: três sintomas
```

(também vale "Criativo 19" em qualquer ponto do nome). Anúncios antigos com outro nome você liga na aba **Anúncios** do painel ou com `tools/meta.py ligar <ad_id> C19`. Ligação manual nunca é desfeita pela sincronização.

## 6. Comandos

```
python -I -X utf8 tools/meta.py sincronizar --dias 30     # puxa agora (o painel também faz)
python -I -X utf8 tools/meta.py sem-criativo              # anúncios ainda sem criativo
python -I -X utf8 tools/meta.py publicar --criativo C19 --arquivo "Vídeos Prontos/Criativo 19 - FR.mp4" \
    --conjunto <adset_id> --texto "<pasta do criativo>/copy_final_fr.txt" --link <url da página> \
    --titulo "..." [--descricao "..."] [--cta SHOP_NOW]   # ensaio: mostra o que seria criado
    ... --confirmar                                         # cria o anúncio PAUSADO
```

`publicar` cria só o anúncio, dentro de um conjunto que você já montou (orçamento, público e otimização continuam no Gerenciador). O status `PAUSED` está fixo no código. Pela regra do projeto, o Claude só roda `--confirmar` depois de mostrar o ensaio e você aprovar no chat.

## Como os números são lidos

| No painel | Origem na API |
|---|---|
| Compras / receita | `omni_purchase` (ou `purchase`, ou `offsite_conversion.fb_pixel_purchase`, o primeiro que existir) |
| Gancho (3 s) | ação `video_view` ÷ impressões |
| Thruplay | `video_thruplay_watched_actions` ÷ impressões |
| CTR do link | `inline_link_clicks` ÷ impressões |
| Retenção | `video_p25/50/75/95/100_watched_actions` e `video_view` ÷ `video_play_actions` |
| Média | soma de todos os criativos com números; contagens (compras, gasto) divididas pelo nº de criativos |

A curva bruta (`video_play_curve_actions`) também fica gravada em `metricas_meta.curva` para análise futura.
