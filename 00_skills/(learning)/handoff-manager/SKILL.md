---
name: handoff-manager
description: "Maintain a concise .notebook/HANDOFF.md of the last verified state. Use for handoff updates. Do NOT use to promote unverified claims."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: handoff-manager

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
