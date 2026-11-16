---
name: simulator-ai
description: "Build a governed AI medical simulator. Use for simulator construction. Never hallucinates or invents results; do NOT use for unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# simulator-ai

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Create ans entire constructor for an AI real world medical simulation. A skill that searches the entire internet to find AI real world medical simulator, to simulates patients and medical treatments 'till find THE CURE for diabetes. The skill needs to folow AGENT.md premisses: 4 agents and all layers of knowledge and the validator subagent, with all knowledge, extreme honest and never hallucinates to validate architecture, code, implemetation and the simulator itself. Skill must validates them a

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
- 11. [10. Stop conditions](references/instructions/11-10-stop-conditions.md) — when an input, tool or check fails.
- 12. [11. Completion](references/instructions/12-11-completion.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
