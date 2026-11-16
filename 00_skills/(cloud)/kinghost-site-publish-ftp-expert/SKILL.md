---
name: kinghost-site-publish-ftp-expert
description: "Governed KingHost WordPress/PHP FTP publish with backup and rollback. Use for KingHost publishing. Do NOT use for unapproved production changes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# KingHost Site Publish FTP Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Publish authorized PHP and WordPress site changes to KingHost over FTP through a **manifest-driven** workflow without uncontrolled overwrites, secret leakage or unverified production state. The skill owns the FTP transport/publish workflow; application-specific engineering remains with `wordpress-expert` or the relevant PHP/application skill.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Mission](references/instructions/02-mission.md) — before acting.
- 3. [Dependencies](references/instructions/03-dependencies.md) — when in scope.
- 4. [Non-negotiable production gates](references/instructions/04-non-negotiable-production-gates.md) — before claiming completion.
- 5. [Supported publication targets](references/instructions/05-supported-publication-targets.md) — when in scope.
- 6. [Deterministic production workflow](references/instructions/06-deterministic-production-workflow.md) — at this step.
- 7. [Rollback triggers](references/instructions/07-rollback-triggers.md) — when in scope.
- 8. [Completion states](references/instructions/08-completion-states.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
