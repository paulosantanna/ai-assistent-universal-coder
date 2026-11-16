# Mixed apply plan (Track C)

> Run dir: `/agent/repos/ai-assistent-universal-coder/.harness-eval/runs/2026-11-13-full`
> Judges: J1 model=`grok-4.7` · J2 model=`grok-4.7`
> **This file is the only Mixed apply input.** Do not re-judge usefulness.

## What these words mean

| Word | Meaning | Apply must |
|------|---------|------------|
| **KEEP** | Text from judge Keep-core columns | Remain in the harness surface as rule/snippet |
| **CUT** | Text from judge Slim columns | Delete or compress only this bulk |
| **Apply** | Mechanical edit | Not a new design pass |

## Hard rules for apply agents

1. For each Mixed ID below, edit **only** that path.
2. **KEEP** items must survive (same contract — concern/module/section/checklist).
   Do not replace a KEEP teaching snippet with a weaker pattern.
3. **CUT** only what both judges' Slim columns describe (or the union when both
   clearly name the same bulk). If KEEP and CUT conflict, **skip that path** (Hold).
4. Never replace a fenced teaching snippet with `See app/...` / `lib/...` / `test/...`.
5. Never defer KEEP content to AGENTS.md or another surface unless CUT explicitly
   names OVERLAP with that path **and** KEEP still retains the behavior contract.
6. Do not open the repo to invent a different convention than KEEP states.
7. After edits: every KEEP bullet must still be satisfied by the file text.

## Paths (0)

_No dual-MIXED surfaces in this run._

