---
name: skill-hardener
description: Harden skills with contracts, forbidden actions and quality gates. Use when the user requests skill hardener or invokes skill-hardener. Do NOT use for ordinary one-off coding or human competency lists.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: skill-hardener

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Harden skills with contracts, forbidden actions and quality gates.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Mission](references/instructions/02-mission.md) — before acting on this contract.
- 3. [Production Scope](references/instructions/03-production-scope.md) — before acting on this contract.
- 4. [Allowed Actions](references/instructions/04-allowed-actions.md) — at this step of execution.
- 5. [Forbidden Actions](references/instructions/05-forbidden-actions.md) — at this step of execution.
- 6. [Required Inputs](references/instructions/06-required-inputs.md) — before acting on this contract.
- 7. [Required Output Schema](references/instructions/07-required-output-schema.md) — before acting on this contract.
- 8. [Prompt Contract](references/instructions/08-prompt-contract.md) — before acting on this contract.
- 9. [Quality Gates](references/instructions/09-quality-gates.md) — before claiming completion.
- 10. [Stop Conditions](references/instructions/10-stop-conditions.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
