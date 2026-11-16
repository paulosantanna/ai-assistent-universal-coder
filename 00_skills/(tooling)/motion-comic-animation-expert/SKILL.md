---
name: motion-comic-animation-expert
description: "Motion Comic animation in Python and FFmpeg: camera, layers, parallax. Use for animar camadas or timeline HQ. Do NOT use to promise unrendered output."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# Animação, câmera e composição Staff

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.
Nível Staff EXPERT descreve o rigor do procedimento; não é certificação nem métrica de performance.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de produzir ou enviar vídeo. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção.

## Procedimento

1. Consumir scene manifest e áudio medido; confirmar fps/resolução/aspecto e arquivos locais. Criar hierarquia conceitual de câmera e offsets por profundidade; manter movimentos de elementos independentes.
2. Definir keyframes com unidades e limites, easing na implementação quando suportado, overscan e pontos focais. Evitar velocidade excessiva, deriva de borda e clipping; usar menor movimento no fundo e maior no primeiro plano.
3. Usar studio.py para offsets lineares, zoom centrado por camada, blur e cut/fade. Movimentos avançados/rotação/easing/oclusão exigem clipe pré-renderizado ou extensão verificada: não inventar suporte.
4. Aceitar clipes IA como kind=video sem loop silencioso; validar duração, continuidade temporal, anatomia e coerência científica antes de inserir. Não sobrescrever takes bons numa retomada.
5. Renderizar cenas individualmente com cache por conteúdo/ativos/parâmetros/versão FFmpeg; montar concat com timestamps e codecs uniformes. Longos usam capítulos e checkpoints, sem carregar todos os frames em RAM.
6. Verificar frames no começo/meio/fim, independência das camadas, A/V e duração real via ffprobe; relato distingue fixture de qualidade cinematográfica avaliada por humano.

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
