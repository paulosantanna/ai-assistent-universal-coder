---
name: harness-eval
description: "Audit an agent harness (AGENTS.md, rules, skills) for broken paths and redundancy. Use for harness audits. Do NOT use for harness setup."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.8.3
  owner_agent: codenavi-agent
---

# Harness Eval

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Evaluate a repo agent harness (AGENTS.md, rules, skills, skill refs) for broken paths/commands, redundant instructions, and usefulness using a stack-agnostic dual-judge protocol with planted traps. HIGH PRIORITY questionnaires at top: Q1 optional docs, Q2 B/C budget before Track A (certainty/tokens). A always runs after Q2; B/C opt-in. ADRs/RFCs excluded from T2. Mixed apply uses 11-mixed-apply.md (KEEP/CUT).

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [User questionnaires (HIGH PRIORITY)](references/instructions/02-user-questionnaires-high-priority.md) — when in scope.
- 3. [Loading this skill's files](references/instructions/03-loading-this-skill-s-files.md) — when in scope.
- 4. [Critical rules](references/instructions/04-critical-rules.md) — before acting.
- 5. [Instructions](references/instructions/05-instructions.md) — when in scope.
- 6. [Examples](references/instructions/06-examples.md) — when choosing an output or matching a use case.
- 7. [Troubleshooting](references/instructions/07-troubleshooting.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
