---
name: "vox-aurum"
description: "Transcribe authorized local bare audio offline with a verified local Whisper model, preserving spoken language and literal output; optionally use an explicitly requested GPU. Use for transcreva esse áudio, áudios dessa pasta, audio to text or transcrição offline. Do NOT use for meeting/call video even if only transcrever is requested (acta-aurea), diarized minutes, live dictation, editing/translation or voice cloning."
license: "CC-BY-4.0"
metadata:
  author: "AEOS; photographic reference supplied by user"
  version: "1.1.1"
  owner_agent: "codenavi-agent"
---

# vox-aurum

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Workflow

1. Reuse a supplied file/folder path. Ask for it only when missing; list candidates with scripts/transcribe.py --audio-dir PATH --list and select the requested files. Explicit todos authorizes the listed audio scope.
2. Read [environment](references/environment.md) for missing engine/model/format/GPU prerequisites. Use a verified Python interpreter and local models; do not silently install packages or fetch a model. No fixed corporate paths or assumed mirror/CUDA versions.
3. Run scripts/transcribe.py with --audio or --audio-dir/--select, --model, --model-dir and --out-dir. Use --model auto for unknown machines; CPU is default, and --device cuda requires the user's GPU/speed request plus actual availability.
4. Preserve spoken language (default pt); seed punctuation with the documented initial prompt rather than rewriting recognized text. No silent translation or invented unintelligible words.
5. For long jobs, wait/poll actual status and artifacts. Separate stdout/stderr; inspect UTF-8 cached TXT and completion markers, not mangled terminal echo. Nonzero status still requires investigation; mere progress on stderr does not imply failure.
6. Present each transcript verbatim in a code block or blockquote. Put possible technical-term recognition issues outside the literal text. Request timestamps/subtitles only when applicable or required by acta-aurea.
7. Save directly when the user supplied a destination. Otherwise offer saving and ask the destination if needed; reuse the cached file rather than retranscribe. Do not treat this offer as permission for unrelated actions.

## Inputs, output and stop

Input: authorized audio, selection, language and actual local runtime/model. Output: literal transcript, source/output paths, requested subtitles and uncertainty. Read [usage](references/usage-and-verification.md) for examples/errors.
No model download or cloud fallback. Missing decoder/engine/model blocks transcription with an actionable error. GPU failure is reported; any CPU fallback is explicit. Helpers implement the photo contract locally; no full Whisper runtime verification is claimed by this package's installation.
Source: IMG_2756–IMG_2761; photographed version 1.1.1.

## Retained resources

- Read [retained provenance](references/provenance.md) only for its matching mode; this entry and root governance take precedence.
