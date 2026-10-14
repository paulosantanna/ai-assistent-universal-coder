---
name: coupling-analysis
description: Analyzes coupling between modules using the three-dimensional model (strength, distance, volatility) from "Balancing Coupling in Software Design". Use when asking "are these modules too coupled?", "show me dependencies", "analyze integration quality", "which modules should I decouple?", "coupling report", or evaluating architectural health. Do NOT use for domain boundary analysis (use domain-analysis) or component sizing (use component-identification-sizing).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Coupling Analysis Skill

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Analyzes coupling between modules using the three-dimensional model (strength, distance, volatility) from "Balancing Coupling in Software Design".

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [When to Use](references/instructions/02-when-to-use.md) — when this domain or mode is in scope.
- 3. [Process](references/instructions/03-process.md) — when this domain or mode is in scope.
- 4. [Quick Reference: Pattern → Integration Strength](references/instructions/04-quick-reference-pattern-integration-strength.md) — when choosing an output or matching a use case.
- 5. [Quick Heuristics](references/instructions/05-quick-heuristics.md) — when this domain or mode is in scope.
- 6. [Known Limitations](references/instructions/06-known-limitations.md) — when this domain or mode is in scope.
- 7. [Book References](references/instructions/07-book-references.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
