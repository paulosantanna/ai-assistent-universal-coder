---
name: component-common-domain-detection
description: Finds duplicate business logic spread across multiple components and suggests consolidation. Use when asking "where is this logic duplicated?", "find common code between services", "what can be consolidated?", "detect shared domain logic", or analyzing component overlap before refactoring. Do NOT use for code-level duplication detection (use linters) or dependency analysis (use coupling-analysis).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Common Domain Component Detection

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Finds duplicate business logic spread across multiple components and suggests consolidation.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [How to Use](references/instructions/02-how-to-use.md) — when this domain or mode is in scope.
- 3. [When to Use](references/instructions/03-when-to-use.md) — when this domain or mode is in scope.
- 4. [Core Concepts](references/instructions/04-core-concepts.md) — when this domain or mode is in scope.
- 5. [Analysis Process](references/instructions/05-analysis-process.md) — when this domain or mode is in scope.
- 6. [Output Format](references/instructions/06-output-format.md) — before acting on this contract.
- 7. [Analysis Checklist](references/instructions/07-analysis-checklist.md) — when this domain or mode is in scope.
- 8. [Implementation Notes](references/instructions/08-implementation-notes.md) — when this domain or mode is in scope.
- 9. [Fitness Functions](references/instructions/09-fitness-functions.md) — when this domain or mode is in scope.
- 10. [Best Practices](references/instructions/10-best-practices.md) — when this domain or mode is in scope.
- 11. [Common Patterns to Look For](references/instructions/11-common-patterns-to-look-for.md) — when choosing an output or matching a use case.
- 12. [Next Steps](references/instructions/12-next-steps.md) — at this step of execution.
- 13. [Notes](references/instructions/13-notes.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
