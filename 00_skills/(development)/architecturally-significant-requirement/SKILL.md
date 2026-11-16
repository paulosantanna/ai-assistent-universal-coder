---
name: architecturally-significant-requirement
description: "Judge if a requirement is architecturally significant (ASR). Use for ASR triage. Do NOT use to write ADRs (architecture-decision-record)."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Architecturally Significant Requirement (ASR)

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Decides whether a requirement, change request or design issue is an Architecturally Significant Requirement (ASR), a requirement with a measurable effect on the architecture and quality of a system, using the seven-criteria ASR Test, then makes it specific and measurable as a quality attribute scenario and hands the decisions it drives to an ADR.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Critical rules](references/instructions/02-critical-rules.md) — before acting.
- 3. [Workflow](references/instructions/03-workflow.md) — at this step.
- 4. [Examples](references/instructions/04-examples.md) — when choosing an output or matching a use case.
- 5. [Troubleshooting](references/instructions/05-troubleshooting.md) — when an input, tool or check fails.
- 6. [Relationship to other skills](references/instructions/06-relationship-to-other-skills.md) — when in scope.
- 7. [Continuity](references/instructions/07-continuity.md) — when reading or promoting continuity knowledge.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md).

Read [asr-test.md](references/asr-test.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
