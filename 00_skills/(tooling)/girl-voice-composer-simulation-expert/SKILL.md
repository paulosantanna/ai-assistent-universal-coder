---
name: girl-voice-composer-simulation-expert
description: "Direct TTS to synthesize a generic fictional child voice (6-8), pt-BR and en-US. Use for synthetic voice profiles. Do NOT use to clone a real child."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Girl Voice Composer — Simulation Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Given a target language, a perceived age (6–8), and a target engine, produce:

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [1. Identity](references/instructions/02-1-identity.md) — before acting.
- 3. [2. Mission](references/instructions/03-2-mission.md) — before acting.
- 4. [3. Activation rules](references/instructions/04-3-activation-rules.md) — before acting.
- 5. [4. Non-activation rules](references/instructions/05-4-non-activation-rules.md) — before acting.
- 6. [5. Authority and scope](references/instructions/06-5-authority-and-scope.md) — before acting.
- 7. [6. Preconditions (fail closed)](references/instructions/07-6-preconditions-fail-closed.md) — when an input, tool or check fails.
- 8. [7. Inputs](references/instructions/08-7-inputs.md) — before acting.
- 9. [8. Outputs](references/instructions/09-8-outputs.md) — before acting.
- 10. [9. Acoustic parameter model (generic, public characteristics)](references/instructions/10-9-acoustic-parameter-model-generic-public-characteristics.md) — when in scope.
- 11. [10. Workflow](references/instructions/11-10-workflow.md) — at this step.
- 12. [11. Tool policy](references/instructions/12-11-tool-policy.md) — before acting.
- 13. [12. Evidence policy](references/instructions/13-12-evidence-policy.md) — before acting.
- 14. [13. Validation](references/instructions/14-13-validation.md) — before claiming completion.
- 15. [14. Stop conditions (BLOCKED)](references/instructions/15-14-stop-conditions-blocked.md) — when an input, tool or check fails.
- 16. [15. Failure behavior](references/instructions/16-15-failure-behavior.md) — when an input, tool or check fails.
- 17. [16. Completion criteria](references/instructions/17-16-completion-criteria.md) — before claiming completion.
- 18. [17. Memory behavior](references/instructions/18-17-memory-behavior.md) — when reading or promoting continuity knowledge.
- 19. [18. Security and safety restrictions](references/instructions/19-18-security-and-safety-restrictions.md) — before acting.
- 20. [19. Examples](references/instructions/20-19-examples.md) — when choosing an output or matching a use case.
- 21. [20. Version and maintenance](references/instructions/21-20-version-and-maintenance.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md).

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
