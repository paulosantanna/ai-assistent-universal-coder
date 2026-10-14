---
name: specs
description: 'Prevent ad hoc creation and modification by requiring a specification before implementation: scope, rationale, acceptance checks, risks and required evidence. Use when the user requests specs, a specification or a pre-implementation contract. Do NOT use to override approved requirements or expand the user request.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# specs

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Prevent ad hoc creation and modification by requiring a specification gate before implementation. The gate must define what will change, why it should change, how success will be verified, which risks are in scope, which risks are excluded, and what evidence must exist before work proceeds.

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
- 9. [8. Workflow](references/instructions/09-8-workflow.md) — at this step of execution.
- 10. [9. Evidence](references/instructions/10-9-evidence.md) — when this domain or mode is in scope.
- 11. [10. Prompt Contract](references/instructions/11-10-prompt-contract.md) — before acting on this contract.
- 12. [11. Tool Policy](references/instructions/12-11-tool-policy.md) — before acting on this contract.
- 13. [12. Validation](references/instructions/13-12-validation.md) — before claiming completion.
- 14. [13. Stop conditions](references/instructions/14-13-stop-conditions.md) — when an input, tool or check fails.
- 15. [14. Failure behavior](references/instructions/15-14-failure-behavior.md) — when an input, tool or check fails.
- 16. [15. Completion](references/instructions/16-15-completion.md) — before claiming completion.
- 17. [16. Memory behavior](references/instructions/17-16-memory-behavior.md) — when reading or promoting continuity knowledge.
- 18. [17. Security restrictions](references/instructions/18-17-security-restrictions.md) — before acting on this contract.
- 19. [18. Source Basis](references/instructions/19-18-source-basis.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [SPEC_DRIVEN_SOURCES.md](references/SPEC_DRIVEN_SOURCES.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
