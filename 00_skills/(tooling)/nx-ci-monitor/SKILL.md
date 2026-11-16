---
name: nx-ci-monitor
description: "Monitor Nx Cloud CI status and handle self-healing fixes. Use for 'watch CI' on Nx. Do NOT use for local task runs (nx-run-tasks)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# CI Monitor Command

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Monitor Nx Cloud CI pipeline status and handle self-healing fixes automatically.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Context](references/instructions/02-context.md) — when in scope.
- 3. [User Instructions](references/instructions/03-user-instructions.md) — when in scope.
- 4. [Configuration Defaults](references/instructions/04-configuration-defaults.md) — when in scope.
- 5. [Nx Cloud Connection Check](references/instructions/05-nx-cloud-connection-check.md) — when in scope.
- 6. [Session Context Behavior](references/instructions/06-session-context-behavior.md) — when in scope.
- 7. [Default Behaviors by Status](references/instructions/07-default-behaviors-by-status.md) — when in scope.
- 8. [Exit Conditions](references/instructions/08-exit-conditions.md) — when in scope.
- 9. [Main Loop](references/instructions/09-main-loop.md) — when in scope.
- 10. [Status Reporting](references/instructions/10-status-reporting.md) — when in scope.
- 11. [User Instruction Examples](references/instructions/11-user-instruction-examples.md) — when choosing an output or matching a use case.
- 12. [Error Handling](references/instructions/12-error-handling.md) — when an input, tool or check fails.
- 13. [Example Session](references/instructions/13-example-session.md) — when choosing an output or matching a use case.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
