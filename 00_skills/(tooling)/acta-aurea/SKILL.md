---
name: "acta-aurea"
description: "Turn an authorized meeting/call video (Teams/OBS .mkv/.mp4) into the complete offline pack: transcript, named speakers, topics, minutes, summary, glossary, subtitles and HTML player. Use for analisar essa call, gerar ata, transcreva a reunião or transcreva esse vídeo de reunião, even when only transcription is named. Do NOT use for a bare audio file with no meeting/speakers/pack (vox-aurum), live dictation or generic report design."
license: "CC-BY-4.0"
metadata:
  author: "AEOS; photographic reference supplied by user"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# acta-aurea

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Workflow

1. Identify the authorized recording, requested destination and language. The source discriminates: meeting video uses this complete pack; bare audio uses vox-aurum. Use PT-BR deliverables unless the user specifies otherwise.
2. Read [environment](references/environment.md) before prerequisite setup and [pipeline](references/pipeline.md) before processing. Resolve real skill/interpreter/model paths; do not copy photographed C:/Workspace_Santander paths as installed resources.
3. Extract mono 16 kHz audio and metadata with scripts/extract_audio.py; reuse approved FFmpeg/PyAV only. Record source hash, duration and original filename without private media in Git/notebook.
4. Use vox-aurum/scripts/transcribe.py with --srt and a local verified model. GPU is used only if requested/authorized and available; otherwise CPU. Inspect actual TXT/SRT and terminal status; stderr progress alone is not failure, and a failed process is never ignored without valid outputs.
5. Run scripts/diarize.py; begin with anonymous labels. Inspect embedding quality, silhouette/distribution and uncertainty; a similarity score is not identity proof. Confirm participant names with the user before setting confirmed: true.
6. Edit the single call.json: timestamped topics, participants, minutes, summary, actions and acronym glossary. List off-topic candidates and omit only user-approved segments; never remove by inference.
7. Run scripts/build_deliverables.py from call.json. Produce index.html, ata.md, resumo.md, transcricao.md, legendas.srt, legendas.vtt and capitulos.vtt; regenerate deterministically after edits.
8. Verify names/omissions, monotonically valid timestamps, escaped HTML, selectable local video, topic seeking and offline loading. Present index.html and precise remaining engine/media uncertainties.

## Inputs, output and stop

Inputs: authorized meeting source, output, confirmed names and omission choices. Output: complete verified offline package derived from call.json.
Dependency/model installation must follow actual authorized setup; no silent package/model download, corporate mirrors assumed or private upload. Missing engine blocks its dependent step; speaker uncertainty stays explicit.
Source: IMG_2749–IMG_2755. Helpers are local implementations of the observed contracts, not recovered originals.

## Examples and failure handling

Example: “transcreva esta reunião do Teams” → full seven-output pack with confirmed names/omissions; “quem falou o quê” → diarized pack with minimal minutes and empty topics if appropriate. Error: missing Whisper/encoder → block dependent stage and report the actual prerequisite.

## Retained resources

- Read [retained provenance](references/provenance.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained usage-and-verification](references/usage-and-verification.md) only for its matching mode; this entry and root governance take precedence.
