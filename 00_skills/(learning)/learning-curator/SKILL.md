---
name: learning-curator
description: "Promote verified, reusable engineering lessons into .notebook/LEARNING.md. Use for learning promotion. Do NOT use to promote unverified claims."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: learning-curator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Promote verified, reusable engineering lessons into `.notebook/LEARNING.md`.

## Promotion gate
A learning must include a trigger, failure/problem, root cause, verified correction/prevention, reuse scope, evidence and confidence.

## Mandatory behavior
- Promote only after verification; speculation stays out.
- Prefer causal, reusable lessons over task-specific chronology.
- Distinguish learning from stable project invariants already owned by `MEMORY.md`.
- Correct or deprecate stale lessons immediately when new evidence invalidates them.
- Never persist secrets, personal data or private chain-of-thought.

## Output
`{"promoted":[],"rejected":[],"deprecated":[],"evidence":[],"status":"PASS|WARN|BLOCKED"}`

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
