---
name: documentary-audio-engineer
description: "Mix documentary audio: narration and music ducking, -16 LUFS, -1.5 dBFS peak. Use to mix narration or fix loudness. Do NOT use for music choice."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Engenharia de áudio documental Staff

Governança: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill de `codenavi-agent`; herda `AGENTS.md`. Lentes são internas; sem novas identidades de agente; sem burlar gates de segredo ou permissão.

## TLC e Spotify

Ler `00_skills/(tooling)/studio-creation-tlc/SKILL.md` antes de produzir ou enviar áudio. Spec-driven 4 ou spec-driven-lean 2. Spotify só recebe mídia criada no Dark Videos e/ou por IA neste app; não há exceção.

O gate de áudio só vale se a medição acontecer de verdade. Medição que falha em silêncio já
produziu um vídeo aprovado com 90% de silêncio — este erro não se repete.

## Procedimento

1. **Medir antes de opinar.** `ffmpeg`/`ffprobe` medindo, não escuta por impressão: loudness
   integrado (LUFS), true peak (dBFS), LRA, e eventos de silêncio com início e duração.
2. **QA de silêncio com `-v info`, nunca `-v error`.** Armadilha real e documentada: com
   `-v error` o `silencedetect` **não emite eventos** e o relatório sai falsamente "0 silêncios".
   Comando correto: `ffmpeg -v info -i ARQ -vn -af silencedetect=noise=-45dB:d=2.0 -f null -`.
3. **Verificar narração contra a duração da cena.** Cena de 60 s com ~13 palavras produz ~54 s de
   silêncio. Faixa correta: 108–136 palavras por 60 s. Cena subnarrada volta para o roteiro; não se
   compensa com tempo morto, música alta ou pausa artificial.
4. **Mixar em etapa explícita e separada do compositor**: EQ de voz, compressão, `loudnorm` e a
   trilha em nível próprio, com **ducking por `sidechaincompress`** para a música ceder ao narrador.
5. **Perseguir os alvos medidos**: voz a **-16 LUFS integrado**, true peak **-1.5 dBFS**, LRA
   saudável. A trilha tem de ser audível (LRA do mix sobe com música presente) e nunca abafar.
6. **Distinguir o "zunido de fundo" de música.** Drone sem melodia não é trilha; se a calma
   esperada não estiver audível, o problema é de curadoria musical, não de volume.
7. **Fixar in-place quando a entrega revisada for a mesma do export**: `audio_mix.py --in-place
   --record render.json` para que o arquivo revisado e o exportado sejam os mesmos bytes.
8. **Registrar números por etapa** em relatório JSON: cada medição com valor e comando usado.

## Contrato e verificação

Entrada: preview renderizado (narração), trilha selecionada, alvos de loudness, diretório do projeto.
Saída: arquivo mixado, `render.json` atualizado por hash, relatório de medições.
Verificação: `-16 LUFS`/`-1.5 dBTP` medidos; zero silêncio acima de 2–3 s; música presente e
audível; decode limpo; narração preenche cada cena; arquivo revisado = arquivo exportado.
Riscos: silêncio por cena subnarrada, música inaudível, música abafando a voz, medição com flag
errada, dessincronia, aprovar por medição estrutural sem escutar.
Bloquear a etapa de mix quando a voz ou a trilha estiverem ausentes. Sem trilha, declarar a lacuna.
Error handling: medição sem eventos de silêncio exige conferir a flag antes de concluir "sem mudez";
loudness fora do alvo exige re-mix, não re-rotulagem.
Segredos são referências de runtime; nunca persistir cookies, tokens ou credenciais.
Não criar agentes, não publicar, não declarar aprovação artística a partir de números técnicos.

## Módulos por necessidade

- Ler [medições e alvos](references/measurements.md) antes de mixar ou contestar um resultado.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
