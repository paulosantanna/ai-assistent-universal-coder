---
name: codenavi
description: "Use for Skill: codenavi."
---

# Skill: codenavi
Governance: CodENavi v1

## Mission
Govern software changes through BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF, using progressive project intelligence, continuity state and current authoritative documentation.

## Mandatory behavior
- Read `AGENT.md`, `AGENTS.md`, `.notebook/INDEX.md` and relevant notes before material work.
- Ensure `.notebook/HANDOFF.md`, `.notebook/MEMORY.md`, `.notebook/PROGRESS.md` and `.notebook/LEARNING.md` exist and follow `references/CODENAVI_CONTINUITY_STANDARD.md`.
- State assumptions, uncertainty and acceptance criteria before coding.
- Prefer the simplest sufficient implementation and surgical diffs.
- Respect repository conventions and architectural boundaries.
- Verify APIs/framework behavior against current project/official docs.
- Keep `PROGRESS.md` live during execution; refresh HANDOFF, durable MEMORY and verified LEARNING in Debrief.
- Update stale notebook knowledge immediately.

## Output
`{"briefing":{},"recon":{},"plan":[],"changes":[],"verification":[],"continuity":{},"debrief":{},"status":"PASS|WARN|BLOCKED"}`