---
name: documentation-11-layer-mapper
description: Generate an 11-layer documentation package that explains what the project does, how it works, why decisions were made, how every endpoint and feature integrates end to end, and what is required to operate it safely. Use when the user requests documentation 11 layer mapper or invokes documentation-11-layer-mapper. Do NOT use to mutate production or invent architecture without source evidence.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# documentation-11-layer-mapper

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Generate an 11-layer documentation package that explains what the project does, how it works, why decisions were made, how every endpoint and feature integrates end to end, and what is required to operate it safely.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [1. Identity](references/instructions/02-1-identity.md) — before acting on this contract.
- 3. [2. Mission](references/instructions/03-2-mission.md) — before acting on this contract.
- 4. [3. Activation](references/instructions/04-3-activation.md) — when this domain or mode is in scope.
- 5. [4. Non-activation](references/instructions/05-4-non-activation.md) — when this domain or mode is in scope.
- 6. [5. Scope](references/instructions/06-5-scope.md) — before acting on this contract.
- 7. [6. Inputs](references/instructions/07-6-inputs.md) — before acting on this contract.
- 8. [7. Outputs](references/instructions/08-7-outputs.md) — before acting on this contract.
- 9. [8. The 11 Layers](references/instructions/09-8-the-11-layers.md) — when this domain or mode is in scope.
- 10. [9. Required Diagrams](references/instructions/10-9-required-diagrams.md) — when this domain or mode is in scope.
- 11. [10. Workflow](references/instructions/11-10-workflow.md) — at this step of execution.
- 12. [11. Evidence](references/instructions/12-11-evidence.md) — when this domain or mode is in scope.
- 13. [12. Prompt contract](references/instructions/13-12-prompt-contract.md) — before acting on this contract.
- 14. [13. Honest evaluator](references/instructions/14-13-honest-evaluator.md) — when this domain or mode is in scope.
- 15. [14. Stop conditions](references/instructions/15-14-stop-conditions.md) — when an input, tool or check fails.
- 16. [15. Completion](references/instructions/16-15-completion.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [SOURCES.md](references/SOURCES.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
