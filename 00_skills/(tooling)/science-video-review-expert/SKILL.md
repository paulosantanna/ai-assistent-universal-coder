---
name: science-video-review-expert
description: "Review and package science Motion Comic videos before export. Use for QA de vídeo de ciência. Do NOT use to self-approve or publish without request."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# Revisão científica, audiovisual e entrega Staff

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.
Nível Staff EXPERT descreve o rigor do procedimento; não é certificação nem métrica de performance.

## Procedimento

1. Verificar preview real, projeto, fontes e licenças; identificar perfil e plataformas. Conferir especificações atuais oficiais quando publicar; perfis editoriais locais não representam garantia de aceitação.
2. Revisar cinco dimensões: science (cada claim/fonte), visual (HQ, alpha/camadas, movimentos/VFX), voice (PT-BR/timbre/pronúncia), subtitles (texto/tempo/contraste/safe area), rights (arte/modelos/música/fontes).
3. Checar duração, A/V streams, resolução, fps, codificação, corrupção, início/fim e sync. Inspecionar timeline completa na revisão final; amostra de frames não certifica documentário inteiro.
4. Registrar falhas por cena e correção mínima; novo conteúdo/áudio/legenda/MP4 invalida aprovação anterior. Gerar review.html, evidence e hashes. Revisão sequencial pela mesma identidade é self-review, não revisão independente.
5. O operador identifica reviewer e confirma os cinco checks após assistir; jamais inventar aprovação humana nem executar review em nome do usuário sem instrução. Gate técnico atesta integridade, não verdade científica automática.
6. Exportar delivery local com MP4, SRT, projeto/fontes e approval/handoff. Publicação requer ação explícita separada e gates do publicador; não inserir automaticamente na fila ativa do Dark-videos.

## Contrato e verificação

Entrada: tema/etapa autorizada, projeto e evidências reais, capacidades locais e limites de direitos/custo.
Saída: artefato da etapa com caminhos e fontes, validação executada e pendências explícitas.
Riscos: erros científicos/visuais, voz inadequada, sincronização, recursos de GPU/disco e publicação prematura.
Bloquear somente a etapa que depende de fonte, modelo, permissão ou aprovação ausente. Conservar trabalho válido.
Error handling: fonte ausente bloqueia a cena; motor indisponível bloqueia geração; arquivo alterado exige novo render e revisão.
Segredos são referências de runtime; nunca copiar cookies, tokens ou credenciais para projeto/notebook/logs.
Não criar agentes, prometer geração instalada ou apresentar verificação estrutural como vídeo aprovado.

## Módulos por necessidade

- Ler [contrato operacional](references/contract.md) antes de executar a etapa ou escolher ferramentas.
- Ler [exemplos e falhas](references/examples.md) para invocação, decisão de escopo ou recuperação.
- Ler [fontes e proveniência](references/sources.md) antes de afirmar suporte técnico ou atualizar APIs.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
