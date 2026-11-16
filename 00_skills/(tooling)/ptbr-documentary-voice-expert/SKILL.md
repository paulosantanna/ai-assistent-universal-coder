---
name: ptbr-documentary-voice-expert
description: "Deep male PT-BR documentary narration, scientific pronunciation. Use for narrador de documentário. Do NOT use to clone voices without authorization."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# Voz documental e áudio Staff

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.
Nível Staff EXPERT descreve o rigor do procedimento; não é certificação nem métrica de performance.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de produzir ou enviar áudio. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção.

## Procedimento

1. Verificar motor/modelo local, licença, amostra real PT-BR e capacidade do hardware. Masculina/documental/profunda é um critério auditivo; não garantir por identificador de voz ou queda artificial de pitch.
2. Preparar texto falável e glossário de siglas, unidades e nomes; SSML só se suportado de fato. Fracionar por cena com identidade vocal estável e pausas entre ideias.
3. Usar adapter Piper se instalado/configurado ou outro provider argv autorizado. Não baixar dependências/pesos silenciosamente. Selecionar modelo e speaker pela amostra e licença, não inventar uma voz aprovada.
4. Medir áudio com ffprobe e comparar à cena; adapter permite atempo 0.85–1.2, normalização e padding. Fora disso reescrever/retimar; nunca acelerar o documentário inteiro para encaixar.
5. Aplicar loudness consistente e true peak com critério auditivo; meta editorial inicial -16 LUFS/-1.5 dBTP é configuração interna, não regra universal das plataformas. Para mix final crítico usar duas passagens e medir saída.
6. Gerar SRT a partir do alinhamento quando disponível; fallback por palavras é estimado e deve ser revisado. Escutar pronúncia, pausas, sibilância, clipping e continuidade antes da aprovação voice.

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
