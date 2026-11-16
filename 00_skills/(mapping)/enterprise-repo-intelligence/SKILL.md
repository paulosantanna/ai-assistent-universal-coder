---
name: enterprise-repo-intelligence
description: "Map enterprise repos with budgets and evidence. Use for repo mapping. Do NOT use to mutate production or invent architecture without source evidence."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: enterprise-repo-intelligence

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Map large enterprise repositories with performance budgets and evidence.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Mission](references/instructions/02-mission.md) — before acting.
- 3. [Production Scope](references/instructions/03-production-scope.md) — before acting.
- 4. [Allowed Actions](references/instructions/04-allowed-actions.md) — at this step.
- 5. [Forbidden Actions](references/instructions/05-forbidden-actions.md) — at this step.
- 6. [Required Inputs](references/instructions/06-required-inputs.md) — before acting.
- 7. [Required Output Schema](references/instructions/07-required-output-schema.md) — before acting.
- 8. [Prompt Contract](references/instructions/08-prompt-contract.md) — before acting.
- 9. [Quality Gates](references/instructions/09-quality-gates.md) — before claiming completion.
- 10. [Stop Conditions](references/instructions/10-stop-conditions.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
