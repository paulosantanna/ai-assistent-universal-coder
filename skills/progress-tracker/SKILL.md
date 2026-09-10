# Skill: progress-tracker
Governance: CodENavi v1

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
