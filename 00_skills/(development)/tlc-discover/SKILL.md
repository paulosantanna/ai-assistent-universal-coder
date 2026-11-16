---
name: tlc-discover
description: "Interview an unshaped idea into a verdict and design doc. Use for 'should we build this' or discovery. Do NOT use to cut tasks or implement."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 0.9.0
  owner_agent: codenavi-agent
---

# TLC Discover

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Interviews an unshaped idea into a verdict and a design document - decisions, flows, schema, contracts - that anyone can plan from without having been in the room.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Critical rules](references/instructions/02-critical-rules.md) — before acting.
- 3. [The interview](references/instructions/03-the-interview.md) — when in scope.
- 4. [Situation](references/instructions/04-situation.md) — when in scope.
- 5. [Problem](references/instructions/05-problem.md) — when in scope.
- 6. [Verdict](references/instructions/06-verdict.md) — when in scope.
- 7. [Decide](references/instructions/07-decide.md) — when in scope.
- 8. [Format](references/instructions/08-format.md) — when in scope.
- 9. [Knowledge chain](references/instructions/09-knowledge-chain.md) — when in scope.
- 10. [Output](references/instructions/10-output.md) — before acting.
- 11. [Examples](references/instructions/11-examples.md) — when choosing an output or matching a use case.
- 12. [Common failures](references/instructions/12-common-failures.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
