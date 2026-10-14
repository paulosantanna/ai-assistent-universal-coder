---
name: kinghost-site-publish-ftp-expert
description: Governed KingHost PHP/WordPress FTP publishing skill with bounded diffs, backup, approval, rollback and post-deploy verification. Use when the user requests kinghost site publish ftp expert or invokes kinghost-site-publish-ftp-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# KingHost Site Publish FTP Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Publish authorized PHP and WordPress site changes to KingHost over FTP through a **manifest-driven** workflow without uncontrolled overwrites, secret leakage or unverified production state. The skill owns the FTP transport/publish workflow; application-specific engineering remains with `wordpress-expert` or the relevant PHP/application skill.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Mission](references/instructions/02-mission.md) — before acting on this contract.
- 3. [Dependencies](references/instructions/03-dependencies.md) — when this domain or mode is in scope.
- 4. [Non-negotiable production gates](references/instructions/04-non-negotiable-production-gates.md) — before claiming completion.
- 5. [Supported publication targets](references/instructions/05-supported-publication-targets.md) — when this domain or mode is in scope.
- 6. [Deterministic production workflow](references/instructions/06-deterministic-production-workflow.md) — at this step of execution.
- 7. [Rollback triggers](references/instructions/07-rollback-triggers.md) — when this domain or mode is in scope.
- 8. [Completion states](references/instructions/08-completion-states.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
