---
name: science-script-expert
description: "Escrever roteiros científicos PT-BR sincronizados com storyboard. Use for roteiro de ciência. Do NOT use for pesquisa sem fontes ou arte final."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# Roteiro documental e storyboard Staff

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.
Nível Staff EXPERT descreve o rigor do procedimento; não é certificação nem métrica de performance.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de produzir o roteiro que vira áudio/vídeo. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção.

## Procedimento

1. Consumir fontes verificadas e definir pergunta central, promessa honesta, explicação visual e conclusão; abertura deve funcionar sem clickbait nem afirmação falsa.
2. Para 60 s usar abertura curta, desenvolvimento e conclusão. Para 10 min construir progressão causal. Para 60/90 min criar capítulos e transições de assunto; outline global deve preceder geração em lotes.
3. Criar cenas de 5–15 s inicialmente e até 60 s só quando motivado; narration, visual, duration, claims e transition obrigatórios. O visual mostra o fenômeno mencionado naquele intervalo.
4. Planejar 110–145 palavras/minuto como estimativa editorial, medir o TTS de fato e reescrever para caber. Não declarar sincronização com base apenas na contagem de palavras.
5. Em cena de buraco negro: distinguir horizonte, disco/nuvem e lente; câmera revela material em acreção enquanto a fala explica sua dinâmica. Não mostrar ingestão indiscriminada do Universo.
6. Preservar pronúncias, unidades e transições contextualizadas; manter legendas discretas separadas da arte; sem balões. Validar somas de tempo e claims antes de pedir ativos.

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
