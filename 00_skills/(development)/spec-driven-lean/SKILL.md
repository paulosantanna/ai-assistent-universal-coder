---
name: spec-driven-lean
description: 'Assimilated Tech Lead''s Club lean spec workflow (tlc-spec-lean 1.0.0). Freeze obligations in plan + proof-backed checks, then build, then independent verify. Triggers: spec-driven-lean, tlc-spec-lean, plan feature, write the checks, build this plan, verify work. Do not use when a formal task list already exists or for standalone design docs.'
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Spec-Driven Lean

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Freeze obligations, not the plan. Four moves: Plan → Checks → Build → Verify. One human-reviewed `plan.md`, then proof-backed `checks.md`, then implementation, then an independent verifier. No task catalogue and no component catalogue.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Identity](references/instructions/02-identity.md) — before acting on this contract.
- 3. [Mission](references/instructions/03-mission.md) — before acting on this contract.
- 4. [Relationship to AEOS `specs` and `spec-driven`](references/instructions/04-relationship-to-aeos-specs-and-spec-driven.md) — when this domain or mode is in scope.
- 5. [Activation](references/instructions/05-activation.md) — when this domain or mode is in scope.
- 6. [Non-activation](references/instructions/06-non-activation.md) — when this domain or mode is in scope.
- 7. [Critical rules](references/instructions/07-critical-rules.md) — before acting on this contract.
- 8. [Profile](references/instructions/08-profile.md) — when this domain or mode is in scope.
- 9. [Artifacts](references/instructions/09-artifacts.md) — when this domain or mode is in scope.
- 10. [Continuity](references/instructions/10-continuity.md) — when reading or promoting continuity knowledge.
- 11. [Lenses (never new agents)](references/instructions/11-lenses-never-new-agents.md) — when this domain or mode is in scope.
- 12. [Scripts](references/instructions/12-scripts.md) — when this domain or mode is in scope.
- 13. [Knowledge verification chain](references/instructions/13-knowledge-verification-chain.md) — before claiming completion.
- 14. [Output behavior](references/instructions/14-output-behavior.md) — before acting on this contract.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [build.md](references/build.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [memory.md](references/memory.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [ORIGINAL_SKILL.md](references/ORIGINAL_SKILL.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [verify.md](references/verify.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
