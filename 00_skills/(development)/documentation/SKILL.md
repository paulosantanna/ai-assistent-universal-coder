---
name: documentation
description: "Generate evidence-based documentation in a sandbox. Use for documentation requests. Do NOT use for production deployment or unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: documentation

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Generate evidence-based documentation in sandbox.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Mission](references/instructions/02-mission.md) — before acting.
- 3. [Allowed Actions](references/instructions/03-allowed-actions.md) — at this step.
- 4. [Forbidden Actions](references/instructions/04-forbidden-actions.md) — at this step.
- 5. [Required Evidence](references/instructions/05-required-evidence.md) — when in scope.
- 6. [Prompt Contract](references/instructions/06-prompt-contract.md) — before acting.
- 7. [Complete Documentation Workflow](references/instructions/07-complete-documentation-workflow.md) — before claiming completion.
- 8. [Mermaid Rules](references/instructions/08-mermaid-rules.md) — before acting.
- 9. [Architecture Package Rules](references/instructions/09-architecture-package-rules.md) — before acting.
- 10. [Quality Gates](references/instructions/10-quality-gates.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
