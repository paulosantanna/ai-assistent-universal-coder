---
name: documentation
description: Generate evidence-based documentation in sandbox. Use when the user requests documentation or invokes documentation. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: documentation

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Generate evidence-based documentation in sandbox.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Mission](references/instructions/02-mission.md) — before acting on this contract.
- 3. [Allowed Actions](references/instructions/03-allowed-actions.md) — at this step of execution.
- 4. [Forbidden Actions](references/instructions/04-forbidden-actions.md) — at this step of execution.
- 5. [Required Evidence](references/instructions/05-required-evidence.md) — when this domain or mode is in scope.
- 6. [Prompt Contract](references/instructions/06-prompt-contract.md) — before acting on this contract.
- 7. [Complete Documentation Workflow](references/instructions/07-complete-documentation-workflow.md) — before claiming completion.
- 8. [Mermaid Rules](references/instructions/08-mermaid-rules.md) — before acting on this contract.
- 9. [Architecture Package Rules](references/instructions/09-architecture-package-rules.md) — before acting on this contract.
- 10. [Quality Gates](references/instructions/10-quality-gates.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
