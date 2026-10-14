---
name: mantis-researcher
description: Audits production source code files based on the strategy in workspace/plan.json. Use when a review plan exists and you need to perform static analysis and deep-dive reviews of targeted files. Don't use for planning, deduplicating, or writing patches.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# mantis-researcher

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Audits production source code files based on the strategy in workspace/plan.json. Use when a review plan exists and you need to perform static analysis and deep-dive reviews of targeted files. Don't use for planning, deduplicating, or writing patches.

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
- 11. [10. Prompt contract](references/instructions/11-10-prompt-contract.md) — before acting on this contract.
- 12. [11. Agent knowledge layers](references/instructions/12-11-agent-knowledge-layers.md) — when this domain or mode is in scope.
- 13. [12. Honest evaluator](references/instructions/13-12-honest-evaluator.md) — when this domain or mode is in scope.
- 14. [13. Stop conditions](references/instructions/14-13-stop-conditions.md) — when an input, tool or check fails.
- 15. [14. Completion](references/instructions/15-14-completion.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [ORIGINAL_SKILL.md](references/ORIGINAL_SKILL.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
