---
name: devops-pipeline-engineering
description: Governed DevOps, Git and GitHub Actions lifecycle with recursive CI recovery, per-workflow guardians, merge readiness and bundle handoff. Use when the user requests devops pipeline engineering or invokes devops-pipeline-engineering. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# DevOps Pipeline Engineering

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Create, harden, operate and recover Git/GitHub CI/CD safely until every required GitHub Actions workflow for the latest head SHA is complete and successful, or a deterministic stop condition requires human action.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Identity and inheritance](references/instructions/02-identity-and-inheritance.md) — before acting on this contract.
- 3. [Mission](references/instructions/03-mission.md) — before acting on this contract.
- 4. [Activation](references/instructions/04-activation.md) — when this domain or mode is in scope.
- 5. [Non-activation](references/instructions/05-non-activation.md) — when this domain or mode is in scope.
- 6. [Core invariants](references/instructions/06-core-invariants.md) — when this domain or mode is in scope.
- 7. [Success contract](references/instructions/07-success-contract.md) — before acting on this contract.
- 8. [Guardian lenses](references/instructions/08-guardian-lenses.md) — when this domain or mode is in scope.
- 9. [Recursive recovery lifecycle](references/instructions/09-recursive-recovery-lifecycle.md) — when this domain or mode is in scope.
- 10. [Git/GitHub authority](references/instructions/10-git-github-authority.md) — before acting on this contract.
- 11. [Token economy](references/instructions/11-token-economy.md) — when this domain or mode is in scope.
- 12. [Merge gate](references/instructions/12-merge-gate.md) — when this domain or mode is in scope.
- 13. [Outputs](references/instructions/13-outputs.md) — before acting on this contract.
- 14. [Completion](references/instructions/14-completion.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
