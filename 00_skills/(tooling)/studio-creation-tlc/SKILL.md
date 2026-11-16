---
name: studio-creation-tlc
description: "TLC rule for Dark Videos media (spec-driven, Spotify). Use for media creation with a role skill. Do NOT use as substitute or to upload mined files."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Criação de áudio e vídeo no padrão TLC

Governança: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill de `codenavi-agent`; herda `AGENTS.md`. Lentes são internas; sem novas identidades de agente; sem burlar gates de segredo ou permissão.

## Qual trilha TLC

Trabalho com decisão de arquitetura ou lista de tarefas: Spec-driven 4.0.0 em `00_skills/(development)/spec-driven/SKILL.md` (specify, design, tasks, execute). Critérios EARS, provas e verificação de mutação.

Trabalho sem lista de tarefas: Spec-driven-lean 2.0.0 em `00_skills/(development)/spec-driven-lean/SKILL.md` (plan, checks, build, verify). O plano congela a obrigação observável antes do código.

As duas trilhas escrevem em `.specs/` do projeto alvo. Não inventar aprovação humana. Não criar outra identidade de agente.

## Spotify no Dark Videos

Regra inviolável: o Spotify só recebe áudio e vídeo criados dentro do Dark Videos e/ou gerados por IA neste app.

- O recibo é HMAC em `backend/app/modules/studio/origin.py`. Origens permitidas: `dark-videos` e `ai`. Quem grava o recibo é o processo que criou o arquivo.
- Pedido com origem, caminho ou publicação minerada não sela nada. A resposta é `spotify_origin_refused`.
- Não existe parâmetro de exceção, force ou bypass.
- Login é OAuth em `accounts.spotify.com`. Captura de sessão do navegador responde `spotify_oauth_only`.
- A API pública do Spotify não recebe catálogo. Mídia admitida responde `spotify_catalog_upload_unavailable` e o arquivo permanece na máquina. Não declarar envio concluído.
- O despacho de vídeos minerados não inclui Spotify (`SOCIAL_PUBLISH_PLATFORMS`).

## Verificação

Prova mínima: `pytest backend/tests/modules/studio/test_spotify_origin.py backend/tests/oauth/test_spotify_login.py` a partir de `D:\Git\dark-videos`.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
