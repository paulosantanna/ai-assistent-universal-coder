---
name: architecturally-significant-requirement
description: Decides whether a requirement, change request or design issue is an Architecturally Significant Requirement (ASR), a requirement with a measurable effect on the architecture and quality of a system, using the seven-criteria ASR Test, then makes it specific and measurable as a quality attribute scenario and hands the decisions it drives to an ADR. Use when the user asks "is this architecturally significant", "ASR", "requisito arquiteturalmente significativo", "does this need an ADR", "architectural drivers", "quality attribute scenario" or "priorize os requisitos que impactam a arquitetura". Do NOT use for writing the ADR itself (use architecture-decision-record), for full feature specification (use spec-driven), or for threat modeling (use security-threat-model).
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Architecturally Significant Requirement (ASR)

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Decides whether a requirement, change request or design issue is an Architecturally Significant Requirement (ASR), a requirement with a measurable effect on the architecture and quality of a system, using the seven-criteria ASR Test, then makes it specific and measurable as a quality attribute scenario and hands the decisions it drives to an ADR.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Critical rules](references/instructions/02-critical-rules.md) — before acting on this contract.
- 3. [Workflow](references/instructions/03-workflow.md) — at this step of execution.
- 4. [Examples](references/instructions/04-examples.md) — when choosing an output or matching a use case.
- 5. [Troubleshooting](references/instructions/05-troubleshooting.md) — when an input, tool or check fails.
- 6. [Relationship to other skills](references/instructions/06-relationship-to-other-skills.md) — when this domain or mode is in scope.
- 7. [Continuity](references/instructions/07-continuity.md) — when reading or promoting continuity knowledge.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Read [asr-test.md](references/asr-test.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
