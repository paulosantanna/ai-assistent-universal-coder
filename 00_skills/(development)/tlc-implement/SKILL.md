---
name: tlc-implement
description: "Implement planned work: extract a checklist, build it, prove each check. Use for 'build this ticket'. Do NOT use to design the work."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 0.1.0
  owner_agent: codenavi-agent
---

# TLC Implement

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Implement a work already planned: extracts a checklist, builds it, and proves every check with an independent verifier.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Profile](references/instructions/02-profile.md) — when in scope.
- 3. [Critical rules](references/instructions/03-critical-rules.md) — before acting.
- 4. [Extract](references/instructions/04-extract.md) — when in scope.
- 5. [Build](references/instructions/05-build.md) — when in scope.
- 6. [Verify](references/instructions/06-verify.md) — before claiming completion.
- 7. [Knowledge chain](references/instructions/07-knowledge-chain.md) — when in scope.
- 8. [Output](references/instructions/08-output.md) — before acting.
- 9. [Examples](references/instructions/09-examples.md) — when choosing an output or matching a use case.
- 10. [Common failures](references/instructions/10-common-failures.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
