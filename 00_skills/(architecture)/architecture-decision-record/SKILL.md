---
name: architecture-decision-record
description: Writes, supersedes and reviews one Architecture Decision Record (ADR), the record of a single architectural decision with its context, options, outcome and consequences, in MADR 4.0.0, Nygard or Y-statement format, then lints it. Use when the user says "write an ADR", "document this decision", "record why we chose X", "supersede ADR-0007", "review this ADR", "escreva um ADR", "registre a decisão arquitetural" or "crie um registro de decisão de arquitetura". Do NOT use for indexing or auditing the whole decision log (use architecture-decision-log), for judging whether a requirement is architecturally significant (use architecturally-significant-requirement), for an organization-wide decision practice (use architecture-knowledge-management), for making a still-open choice (use the-jury or technical-design-doc-creator), or for general documentation (use docs-writer).
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Architecture Decision Record (ADR)

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Writes, supersedes and reviews one Architecture Decision Record (ADR), the record of a single architectural decision with its context, options, outcome and consequences, in MADR 4.0.0, Nygard or Y-statement format, then lints it.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Critical rules](references/instructions/02-critical-rules.md) — before acting on this contract.
- 3. [Workflow](references/instructions/03-workflow.md) — at this step of execution.
- 4. [Review mode](references/instructions/04-review-mode.md) — when this domain or mode is in scope.
- 5. [Examples](references/instructions/05-examples.md) — when choosing an output or matching a use case.
- 6. [Troubleshooting](references/instructions/06-troubleshooting.md) — when an input, tool or check fails.
- 7. [Relationship to other skills](references/instructions/07-relationship-to-other-skills.md) — when this domain or mode is in scope.
- 8. [Continuity](references/instructions/08-continuity.md) — when reading or promoting continuity knowledge.
- 9. [Provenance and licenses](references/instructions/09-provenance-and-licenses.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Read [adr-practices.md](references/adr-practices.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [ORIGINAL_SKILL.md](references/ORIGINAL_SKILL.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
