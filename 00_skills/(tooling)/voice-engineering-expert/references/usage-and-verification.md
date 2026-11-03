# Usage and verification

## Honesty note to include with every file

This WAV is original source-filter formant speech. It was not cloned from a person and it was not rendered by a commercial voice API. It is controllable in pitch, tract scale, breath and intonation. It is not claimed to pass a blind test against a recorded speaker. See the manifest field `ceiling`.

## Requests that should route here

- "engenharia de dados de voz para o aplicativo"
- "criar voz sintética feminina adulta em português"
- "voz infantil sem sotaque para um jogo educativo"
- "voice-engineering-expert, tom mais grave em 100 cents"

## Requests that should not

- "transcreva esse áudio" routes to vox-aurum.
- "gera a ata da call" routes to acta-aurea.
- "clona esta voz" is a refusal, not a different tool.

## Failure modes

- `blocked-use-context`: sexual, fraud or clone wording. Change the task or stop.
- `child-profile-needs-nonsexual-use-context`: add a real narration purpose.
- `out_dir is unsafe`: write under the project or `/tmp`.
- `unknown phone`: the override left the inventory. Use a symbol from the phone table.
- `utterance longer than 18 seconds`: split the text.
- F0 far from the band on a flat vowel: do not ship that file; re-render once with the preset F0. If it still misses, report the measurement and stop.

## Gates the self-check enforces

Sustained flat vowels for all six presets land within 18 percent of the reference F0. Demo sentences last more than 0.4 s, stay under full scale, and keep RMS above 0.02. Crest stays under 40. Portuguese demo contains the affricate `tsh` and keeps the lateral in "olá". Clone and empty child context refuse.
