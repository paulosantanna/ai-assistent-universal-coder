---
name: science-vfx-expert
description: "Plan controlled science VFX: gravitational lens, particles, glow. Use for VFX científicos em Motion Comic. Do NOT use to claim validated physics."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# VFX científicos e legibilidade Staff

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.
Nível Staff EXPERT descreve o rigor do procedimento; não é certificação nem métrica de performance.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de produzir ou enviar vídeo. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção.

## Procedimento

1. Classificar efeito como diagrama, ilustração artística ou simulação quantitativa. Se quantitativo, exigir equações, unidades, condições e validação numérica; composição artística recebe rótulo apropriado.
2. Para lente gravitacional: planejar desvio da luz e imagens/arcos coerentes com geometria qualitativa; distorcer fundo por mapa radial ou clipe/shader previamente validado. FFmpeg lenscorrection modela lente óptica e não certifica relatividade.
3. Para acreção: partículas em órbita/fluxo motivado, disco emissivo fora do horizonte e distribuição visual plausível; não mostrar brilho material saindo de dentro do horizonte sem explicar a ilustração.
4. Separar emissivo, glow e partículas do objeto principal. Limitar exposição, número/tamanho/velocidade e flicker; glow complementa forma em vez de lavar contraste. Ruído aleatório não vira fenômeno científico.
5. Entregar efeitos como camadas RGBA/clipes pré-renderizados compatíveis com timeline; compositor local suporta overlay/blur, não um solver científico nem geração procedural completa. Para distorções avançadas usar workflow/clipe real.
6. Verificar frames e movimento em escala de cinza/áreas claras, não ofuscar legendas; revisar com fonte científica e registrar simplificações. Se ferramenta/modelo ausente, bloquear efeito dependente, conservar a timeline.

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
