---
name: domain-identification-grouping
description: Groups existing components into logical business domains to plan service-based architecture. Use when asking "which components belong together?", "group these into services", "organize by domain", "component-to-domain mapping", or planning service extraction from an existing codebase. Do NOT use for identifying new domains from scratch (use domain-analysis) or analyzing coupling (use coupling-analysis).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Domain Identification and Grouping

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Groups existing components into logical business domains to plan service-based architecture.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [How to Use](references/instructions/02-how-to-use.md) — when this domain or mode is in scope.
- 3. [When to Use](references/instructions/03-when-to-use.md) — when this domain or mode is in scope.
- 4. [Core Concepts](references/instructions/04-core-concepts.md) — when this domain or mode is in scope.
- 5. [Analysis Process](references/instructions/05-analysis-process.md) — when this domain or mode is in scope.
- 6. [Domain Identification](references/instructions/06-domain-identification.md) — when this domain or mode is in scope.
- 7. [Component Domain Assignment](references/instructions/07-component-domain-assignment.md) — when this domain or mode is in scope.
- 8. [Namespace Refactoring Plan](references/instructions/08-namespace-refactoring-plan.md) — at this step of execution.
- 9. [Domain Map](references/instructions/09-domain-map.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
