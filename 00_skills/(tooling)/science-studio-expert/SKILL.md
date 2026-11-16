---
name: science-studio-expert
description: "Orquestrar Science Studio AI do tema ao Motion Comic revisável. Use for criar vídeo de ciência. Do NOT use to publish without review."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.2.0
  owner_agent: codenavi-agent
---

# Orquestração Staff de produção científica

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.
Nível Staff EXPERT descreve o rigor do procedimento; não é certificação nem métrica de performance.

## Procedimento

1. Resolver tema, público e perfil: short=60 s 9:16, youtube=600 s 16:9, documentary=3600 s 16:9, full-documentary=5400 s 16:9. Não perguntar novamente por idioma/voz já definidos: PT-BR, masculina documental profunda, sem balões.
2. Consultar doctor, serviços/modelos/configuração e direitos reais antes de prometer geração automática. Preferir local; cloud somente dentro da autorização/custo. Não instalar dependências silenciosamente.
3. Executar pesquisa → roteiro/claims → storyboard/arte → animação/VFX → voz/sincronização → render/revisão. Usar as skills irmãs por etapa, sob a mesma identidade.
4. Para 60/90 minutos, criar arco e capítulos com fatos próprios, recorrências editoriais justificadas, orçamento de cenas/armazenamento e produção incremental; não esticar o mesmo clipe.
5. Operar a CLI compartilhada e manter cenas/áudio/arte/evidências em projeto local. Pelo chat, preparar os insumos e executar as ferramentas disponíveis. No Dark-videos, usar a integração autenticada e o mesmo contrato. Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md`: Spec-driven 4 ou spec-driven-lean 2, e a regra inviolável de que o Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app.
6. Entregar MP4 e SRT, projeto e fontes, relatório de revisão e capítulos de YouTube quando autorados. Estado final aguardando revisão humana; exportar só após os cinco checks. Publicação é outra ação explícita.

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
