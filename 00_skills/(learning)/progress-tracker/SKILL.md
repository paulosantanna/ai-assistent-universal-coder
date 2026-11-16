---
name: progress-tracker
description: "Keep .notebook/PROGRESS.md as the live, evidence-backed mission checklist. Use for progress tracking. Do NOT use to promote unverified claims."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: progress-tracker

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Keep `.notebook/PROGRESS.md` as the live, evidence-backed source of truth for the current mission.

## State model
- `[ ]` pending
- `[~]` active
- `[x]` completed and verified
- `[!]` blocked

## Mandatory behavior
- Define mission, success criteria, current CodENavi phase and verification gates.
- Update at meaningful step/batch boundaries.
- Move an item to `[x]` only when its acceptance gate is satisfied.
- Record factual outcomes and evidence pointers, including material failed attempts/root-cause clues.
- Keep open decisions/blockers explicit.
- Do not copy durable memory or generalized learning into the progress log.
- Never persist secrets or private chain-of-thought.

## Output
`{"phase":"","pending":[],"active":[],"completed":[],"blocked":[],"verification":[],"evidence":[],"status":"PASS|WARN|BLOCKED"}`

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
