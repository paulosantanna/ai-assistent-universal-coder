---
name: devops-pipeline-engineering
description: "Governed DevOps, Git and Actions lifecycle: CI recovery, merge readiness. Use for DevOps or Actions work. Do NOT use for unapproved prod changes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# DevOps Pipeline Engineering

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Create, harden, operate and recover Git/GitHub CI/CD safely until every required GitHub Actions workflow for the latest head SHA is complete and successful, or a deterministic stop condition requires human action.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Identity and inheritance](references/instructions/02-identity-and-inheritance.md) — before acting.
- 3. [Mission](references/instructions/03-mission.md) — before acting.
- 4. [Activation](references/instructions/04-activation.md) — when in scope.
- 5. [Non-activation](references/instructions/05-non-activation.md) — when in scope.
- 6. [Core invariants](references/instructions/06-core-invariants.md) — when in scope.
- 7. [Success contract](references/instructions/07-success-contract.md) — before acting.
- 8. [Guardian lenses](references/instructions/08-guardian-lenses.md) — when in scope.
- 9. [Recursive recovery lifecycle](references/instructions/09-recursive-recovery-lifecycle.md) — when in scope.
- 10. [Git/GitHub authority](references/instructions/10-git-github-authority.md) — before acting.
- 11. [Token economy](references/instructions/11-token-economy.md) — when in scope.
- 12. [Merge gate](references/instructions/12-merge-gate.md) — when in scope.
- 13. [Outputs](references/instructions/13-outputs.md) — before acting.
- 14. [Completion](references/instructions/14-completion.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
