---
name: handoff-manager
description: "Use for Skill: handoff-manager."
---

# Skill: handoff-manager
Governance: CodENavi v1

## Mission
Maintain a concise, executable `.notebook/HANDOFF.md` representing only the last verified operational state.

## Mandatory behavior
- Refresh on pause, session boundary, operator/tool context change, or incomplete debrief.
- Record objective, last verified state, touched paths, decisions, blockers/risks, evidence, exact next actions and remaining validation.
- Distinguish verified facts from pending/uncertain items.
- Link to `PROGRESS.md` instead of copying detailed logs.
- Never persist secrets, personal data or private chain-of-thought.
- Replace stale state rather than append endless historical diaries.

## Output
`{"objective":"","verified_state":[],"working_set":[],"decisions":[],"blockers":[],"evidence":[],"next_actions":[],"validation_remaining":[],"status":"PASS|WARN|BLOCKED"}`