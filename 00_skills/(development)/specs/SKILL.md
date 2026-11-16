---
name: specs
description: "Require a spec before implementation: scope, checks, risks. Use for pre-implementation contracts. Do NOT use to override approved requirements."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# specs

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Prevent ad hoc creation and modification by requiring a specification gate before implementation. The gate must define what will change, why it should change, how success will be verified, which risks are in scope, which risks are excluded, and what evidence must exist before work proceeds.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [1. Identity](references/instructions/02-1-identity.md) — before acting.
- 3. [2. Mission](references/instructions/03-2-mission.md) — before acting.
- 4. [3. Activation](references/instructions/04-3-activation.md) — when in scope.
- 5. [4. Non-activation](references/instructions/05-4-non-activation.md) — when in scope.
- 6. [5. Scope](references/instructions/06-5-scope.md) — before acting.
- 7. [6. Inputs](references/instructions/07-6-inputs.md) — before acting.
- 8. [7. Outputs](references/instructions/08-7-outputs.md) — before acting.
- 9. [8. Workflow](references/instructions/09-8-workflow.md) — at this step.
- 10. [9. Evidence](references/instructions/10-9-evidence.md) — when in scope.
- 11. [10. Prompt Contract](references/instructions/11-10-prompt-contract.md) — before acting.
- 12. [11. Tool Policy](references/instructions/12-11-tool-policy.md) — before acting.
- 13. [12. Validation](references/instructions/13-12-validation.md) — before claiming completion.
- 14. [13. Stop conditions](references/instructions/14-13-stop-conditions.md) — when an input, tool or check fails.
- 15. [14. Failure behavior](references/instructions/15-14-failure-behavior.md) — when an input, tool or check fails.
- 16. [15. Completion](references/instructions/16-15-completion.md) — before claiming completion.
- 17. [16. Memory behavior](references/instructions/17-16-memory-behavior.md) — when reading or promoting continuity knowledge.
- 18. [17. Security restrictions](references/instructions/18-17-security-restrictions.md) — before acting.
- 19. [18. Source Basis](references/instructions/19-18-source-basis.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.
Read [SPEC_DRIVEN_SOURCES.md](references/SPEC_DRIVEN_SOURCES.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
