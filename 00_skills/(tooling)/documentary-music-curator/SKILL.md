---
name: documentary-music-curator
description: "Select calm documentary music with verified license, no Content ID risk. Use for track licensing. Do NOT use for final mix or unlicensed downloads."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Curadoria de trilha calma com licença verificável

Governança: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill de `codenavi-agent`; herda `AGENTS.md`. Lentes são internas; sem novas identidades de agente; sem burlar gates de segredo ou permissão.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de produzir ou enviar áudio. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção.

Duas autoridades simultâneas: procedência legal do áudio e engenharia de áudio de documentário.
Uma faixa bonita com licença duvidosa é um passivo, não um ativo.

## Procedimento

1. **Fixar o critério de calma antes de buscar.** Calma é propriedade mensurável, não impressão:
   andamento contido (referência ≤ ~90 BPM), ausência de percussão marcada ou bateria em destaque,
   ausência de vocal cantado inteligível, estabilidade dinâmica (LRA baixo a médio), sem pico
   súbito. Gêneros típicos: ambient, drone tonal, neoclássico lento, piano/strings lentos, pads.
2. **Buscar apenas em acervos com licença explícita**: Free Music Archive com tag Creative Commons,
   Pixabay Music sob Pixabay Content License, ccMixter, Wikimedia Commons (CC0/CC BY), Internet
   Archive (PD/CC0), Openverse, ou página oficial do artista com licença declarada.
3. **Recusar o rótulo "No Copyright Music".** Canal de YouTube que se autodenomina sem copyright,
   sem licença explícita na descrição/artista, é rejeitado. A maioria rotula errado e gera claim.
4. **Comprovar por faixa**: `license_name`, `license_url`, `evidence_url` reais e conferidos, mais
   `commercial_use`, `derivatives_allowed`, `attribution_required`. Sem URL de licença conferida,
   a faixa é **rejeitada** — nunca preencher licença suposta.
5. **Medir de fato**: `ffprobe`/`ffmpeg` para duração, loudness integrado e LRA. Medir, não estimar
   de memória. Registrar o número medido em `why_calm`.
6. **Exigir atribuição quando devida**: se `attribution_required`, capturar o texto exato que os
   créditos do vídeo devem exibir. Sem o texto, a faixa não entra por falta de crédito.
7. **Cobrir a duração real**: a trilha tem de cobrir o vídeo inteiro, com repetição declarada e
   pontos de loop definidos quando a faixa for mais curta que o vídeo. Reportar a lacuna se não
   houver acervo suficiente — lacuna declarada é aceitável, silêncio musical não.
8. **Registrar rejeições** com motivo concreto: é a prova de que o filtro operou.

## Contrato e verificação

Entrada: duração alvo, caráter desejado, orçamento zero ou licenciado, disponibilidade de rede.
Saída: `license-ledger.json` (aceitas + rejeitadas), arquivos das aceitas, relatório de seleção.
Verificação: cada aceita tem licença conferida por URL, duração medida, caráter de calma medido,
atribuição capturada quando exigida; total aceito cobre a duração alvo ou a lacuna está declarada.
Riscos: licença inexistente, claim de Content ID, música agitada, faixa que abafa o narrador,
cobertura insuficiente, acervo indisponível.
Bloquear a etapa musical quando não houver faixa com licença verificável; oferecer a trilha
procedural validada (`science-studio/music_gen.py`) como fallback declarado, nunca como equivalente.
Error handling: site indisponível não autoriza licença suposta; arquivo corrompido é rejeitado.
Segredos são referências de runtime; nunca persistir cookies, tokens ou credenciais.
Não criar agentes, não publicar, não ceder crédito a quem não é o autor.

## Módulos por necessidade

- Ler [critério de calma](references/calm-criteria.md) ao avaliar ou contestar uma faixa; ele contém
  as licenças aceitas e a regra de rejeição por procedência.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
