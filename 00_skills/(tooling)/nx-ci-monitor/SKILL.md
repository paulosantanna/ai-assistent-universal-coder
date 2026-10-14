---
name: nx-ci-monitor
description: Monitor Nx Cloud CI pipeline status and handle self-healing fixes automatically. Use when user says "watch CI", "monitor pipeline", "check CI status", "fix CI failures", or "self-heal CI". Requires Nx Cloud connection. Do NOT use for local task execution (use nx-run-tasks) or general CI debugging outside Nx Cloud.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# CI Monitor Command

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Monitor Nx Cloud CI pipeline status and handle self-healing fixes automatically.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Context](references/instructions/02-context.md) — when this domain or mode is in scope.
- 3. [User Instructions](references/instructions/03-user-instructions.md) — when this domain or mode is in scope.
- 4. [Configuration Defaults](references/instructions/04-configuration-defaults.md) — when this domain or mode is in scope.
- 5. [Nx Cloud Connection Check](references/instructions/05-nx-cloud-connection-check.md) — when this domain or mode is in scope.
- 6. [Session Context Behavior](references/instructions/06-session-context-behavior.md) — when this domain or mode is in scope.
- 7. [Default Behaviors by Status](references/instructions/07-default-behaviors-by-status.md) — when this domain or mode is in scope.
- 8. [Exit Conditions](references/instructions/08-exit-conditions.md) — when this domain or mode is in scope.
- 9. [Main Loop](references/instructions/09-main-loop.md) — when this domain or mode is in scope.
- 10. [Status Reporting](references/instructions/10-status-reporting.md) — when this domain or mode is in scope.
- 11. [User Instruction Examples](references/instructions/11-user-instruction-examples.md) — when choosing an output or matching a use case.
- 12. [Error Handling](references/instructions/12-error-handling.md) — when an input, tool or check fails.
- 13. [Example Session](references/instructions/13-example-session.md) — when choosing an output or matching a use case.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
