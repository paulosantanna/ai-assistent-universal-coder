---
name: architecture-decision-record
description: "Write, supersede or review one ADR (MADR, Nygard, Y-statement) and lint it. Use when asked to record a decision. Do NOT use for the ADR index."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Architecture Decision Record (ADR)

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Writes, supersedes and reviews one Architecture Decision Record (ADR), the record of a single architectural decision with its context, options, outcome and consequences, in MADR 4.0.0, Nygard or Y-statement format, then lints it.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Critical rules](references/instructions/02-critical-rules.md) — before acting.
- 3. [Workflow](references/instructions/03-workflow.md) — at this step.
- 4. [Review mode](references/instructions/04-review-mode.md) — when in scope.
- 5. [Examples](references/instructions/05-examples.md) — when choosing an output or matching a use case.
- 6. [Troubleshooting](references/instructions/06-troubleshooting.md) — when an input, tool or check fails.
- 7. [Relationship to other skills](references/instructions/07-relationship-to-other-skills.md) — when in scope.
- 8. [Continuity](references/instructions/08-continuity.md) — when reading or promoting continuity knowledge.
- 9. [Provenance and licenses](references/instructions/09-provenance-and-licenses.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md).

Read [adr-practices.md](references/adr-practices.md) only when the domain workflow needs it; root governance and this entry take precedence.
Read [ORIGINAL_SKILL.md](references/ORIGINAL_SKILL.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
