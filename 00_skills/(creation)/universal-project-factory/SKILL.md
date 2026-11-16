---
name: universal-project-factory
description: "Plan and generate sandbox-first projects from zero to production for any stack. Use for project generation. Do NOT use for ordinary one-off coding."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: universal-project-factory

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Plan and generate a sandbox-first project from zero to production for any requested architecture, language set and database set.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Mission](references/instructions/02-mission.md) — before acting.
- 3. [Allowed Actions](references/instructions/03-allowed-actions.md) — at this step.
- 4. [Forbidden Actions](references/instructions/04-forbidden-actions.md) — at this step.
- 5. [Required Inputs](references/instructions/05-required-inputs.md) — before acting.
- 6. [Output Schema](references/instructions/06-output-schema.md) — before acting.
- 7. [Workflow](references/instructions/07-workflow.md) — at this step.
- 8. [Quality Gates](references/instructions/08-quality-gates.md) — before claiming completion.
- 9. [Stop Conditions](references/instructions/09-stop-conditions.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
