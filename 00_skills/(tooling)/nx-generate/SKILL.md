---
name: nx-generate
description: Generate code using Nx generators — scaffold projects, libraries, features, or run workspace-specific generators with proper discovery, validation, and verification. Use when user says "create a new library", "scaffold a component", "generate code with Nx", "run a generator", "nx generate", or any code scaffolding task in a monorepo. Prefers local workspace-plugin generators over external plugins. Do NOT use for running build/test/lint tasks (use nx-run-tasks) or workspace configuration (use nx-workspace).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Run Nx Generator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Generate code using Nx generators — scaffold projects, libraries, features, or run workspace-specific generators with proper discovery, validation, and verification.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Generator Discovery Flow](references/instructions/02-generator-discovery-flow.md) — when this domain or mode is in scope.
- 3. [Pre-Execution Checklist](references/instructions/03-pre-execution-checklist.md) — at this step of execution.
- 4. [Execution](references/instructions/04-execution.md) — at this step of execution.
- 5. [Post-Generation](references/instructions/05-post-generation.md) — when this domain or mode is in scope.
- 6. [Error Handling](references/instructions/06-error-handling.md) — when an input, tool or check fails.
- 7. [Key Principles](references/instructions/07-key-principles.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
