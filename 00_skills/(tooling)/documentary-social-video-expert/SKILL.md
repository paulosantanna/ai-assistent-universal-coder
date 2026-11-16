---
name: documentary-social-video-expert
description: "Publication pack: titles, chapters, thumbnails, vertical cuts. Use for YouTube/Reels metadata. Do NOT use to publish (dark-videos-pipeline-expert)."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Pacote de publicação multiplataforma Staff

Governança: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill de `codenavi-agent`; herda `AGENTS.md`. Lentes são internas; sem novas identidades de agente; sem burlar gates de segredo ou permissão.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de montar um pacote que possa ir ao Spotify. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção. Vídeo minerado fica de fora.

Isto é **planejamento de metadados**, não publicação. Publicar é ação separada, com pedido
explícito do operador e os gates reais do publicador existente.

## Procedimento

1. **Recusar clickbait falso.** O título descreve o que o vídeo entrega. É proibido "filmado",
   "real", "exclusivo", "imagens de microscópio" quando o vídeo é ilustração gerada. Um título que
   o conteúdo não sustenta é defeito, não marketing.
2. **Confirmar limites de plataforma na fonte oficial** antes de afirmar qualquer número: duração
   máxima, proporção, dimensões, formato de capítulos, requisitos de thumbnail. Citar a URL. Nunca
   afirmar limite de plataforma de memória.
3. **Escrever capítulos por timestamp real** cobrindo a duração inteira, com o primeiro em `00:00`
   e incrementos coerentes. Timestamp inventado quebra o recurso de capítulos.
4. **Oferecer opções de título, não uma** — com o comprimento medido em caracteres e o que cada
   uma promete. Registrar o que o título NÃO pode prometer.
5. **Descrição completa**: resumo honesto, capítulos, fontes/atribuições (incluindo créditos de
   trilha exigidos por licença), e natureza educativa do conteúdo.
6. **Thumbnail em 1280×720**: descrever imagem, texto de tela curto e legibilidade. Texto de tela
   não pode contradizer o vídeo.
7. **Derivar verticais 9:16 sem mentir**: cortes de 30–60 s com origem identificada (capítulo +
   tema), hook real nos primeiros 2 s, texto de tela e hashtags. O corte herda a honestidade do
   vídeo de origem — não se cria promessa nova no corte.
8. **Mapear risco de retenção sem inventar número**: apontar onde um documentário longo perde
   audiência e o que muda (ritmo, retomada de gancho, quebra de capítulo). Não citar métrica de
   retenção que não foi medida.

## Contrato e verificação

Entrada: duração/estrutura do vídeo, tema, arquivo de entrega, limites de plataforma confirmados.
Saída: `plan.json` estruturado e `metadata.md` pronto para uso, em PT-BR.
Verificação: capítulos somam a duração real e começam em 00:00; nenhum limite de plataforma sem
fonte citada; nenhuma afirmação de título sem lastro no conteúdo; créditos de licença presentes.
Riscos: clickbait falso, timestamp errado, limite de plataforma inventado, promessa de thumbnail
não cumprida, corte vertical que cria promessa nova, publicação confundida com planejamento.
Bloquear a etapa de metadados quando a duração final não estiver fechada — capítulo sem duração
real é chute.
Error handling: limite de plataforma não confirmável é declarado como não confirmado, não estimado.
Segredos são referências de runtime; nunca persistir cookies, tokens ou credenciais de conta.
Não criar agentes, não publicar, não operar conta de rede social.

## Módulos por necessidade

- Ler [limites confirmados](references/platform-limits.md) antes de afirmar qualquer número; ele
  cobre retenção e honestidade de título e corte.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
