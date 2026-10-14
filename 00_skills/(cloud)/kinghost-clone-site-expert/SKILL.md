---
name: kinghost-clone-site-expert
description: Governed KingHost full-site clone skill that acquires an integrity-verified FTP copy without mutating the remote origin and without silently losing files. Use when the user requests kinghost clone site expert or invokes kinghost-clone-site-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# KingHost Clone Site Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Clone an authorized KingHost-hosted site from FTP into a controlled workspace as completely and reproducibly as the selected FTP account permits, preserving directory structure, filenames, binary payloads and evidence of transfer integrity while never mutating the remote source.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Mission](references/instructions/02-mission.md) — before acting on this contract.
- 3. [Dependencies](references/instructions/03-dependencies.md) — when this domain or mode is in scope.
- 4. [Safety contract](references/instructions/04-safety-contract.md) — before acting on this contract.
- 5. [Deterministic workflow](references/instructions/05-deterministic-workflow.md) — at this step of execution.
- 6. [WordPress/PHP completeness](references/instructions/06-wordpress-php-completeness.md) — before claiming completion.
- 7. [Evidence](references/instructions/07-evidence.md) — when this domain or mode is in scope.
- 8. [Completion states](references/instructions/08-completion-states.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
