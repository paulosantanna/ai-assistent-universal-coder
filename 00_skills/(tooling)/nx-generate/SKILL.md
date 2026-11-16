---
name: nx-generate
description: "Scaffold code with Nx generators: projects, libraries, features. Use for 'nx generate' tasks. Do NOT use for running tasks (nx-run-tasks)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Run Nx Generator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Generate code using Nx generators — scaffold projects, libraries, features, or run workspace-specific generators with proper discovery, validation, and verification.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Generator Discovery Flow](references/instructions/02-generator-discovery-flow.md) — when in scope.
- 3. [Pre-Execution Checklist](references/instructions/03-pre-execution-checklist.md) — at this step.
- 4. [Execution](references/instructions/04-execution.md) — at this step.
- 5. [Post-Generation](references/instructions/05-post-generation.md) — when in scope.
- 6. [Error Handling](references/instructions/06-error-handling.md) — when an input, tool or check fails.
- 7. [Key Principles](references/instructions/07-key-principles.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
