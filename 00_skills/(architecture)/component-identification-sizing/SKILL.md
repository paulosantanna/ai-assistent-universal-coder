---
name: component-identification-sizing
description: Maps architectural components in a codebase and measures their size to identify what should be extracted first. Use when asking "how big is each module?", "what components do I have?", "which service is too large?", "analyze codebase structure", "size my monolith", or planning where to start decomposing. Do NOT use for runtime performance sizing or infrastructure capacity planning.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Component Identification and Sizing

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Maps architectural components in a codebase and measures their size to identify what should be extracted first.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [How to Use](references/instructions/02-how-to-use.md) — when this domain or mode is in scope.
- 3. [When to Use](references/instructions/03-when-to-use.md) — when this domain or mode is in scope.
- 4. [Core Concepts](references/instructions/04-core-concepts.md) — when this domain or mode is in scope.
- 5. [Analysis Process](references/instructions/05-analysis-process.md) — when this domain or mode is in scope.
- 6. [Output Format](references/instructions/06-output-format.md) — before acting on this contract.
- 7. [Recommendations](references/instructions/07-recommendations.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
