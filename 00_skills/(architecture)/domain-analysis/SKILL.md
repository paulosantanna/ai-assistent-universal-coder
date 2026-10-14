---
name: domain-analysis
description: Maps business domains and suggests service boundaries in any codebase using DDD Strategic Design. Use when asking "what are the domains in this codebase?", "where should I draw service boundaries?", "identify bounded contexts", "classify subdomains", "DDD analysis", or analyzing domain cohesion. Do NOT use for grouping existing components into domains (use domain-identification-grouping) or dependency analysis (use coupling-analysis).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Subdomain Identification & Bounded Context Analysis

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Maps business domains and suggests service boundaries in any codebase using DDD Strategic Design.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [When to Use](references/instructions/02-when-to-use.md) — when this domain or mode is in scope.
- 3. [Core Principles](references/instructions/03-core-principles.md) — when this domain or mode is in scope.
- 4. [Analysis Process](references/instructions/04-analysis-process.md) — when this domain or mode is in scope.
- 5. [Output Format](references/instructions/05-output-format.md) — before acting on this contract.
- 6. [Best Practices](references/instructions/06-best-practices.md) — when this domain or mode is in scope.
- 7. [Analysis Checklist](references/instructions/07-analysis-checklist.md) — when this domain or mode is in scope.
- 8. [Quick Reference](references/instructions/08-quick-reference.md) — when this domain or mode is in scope.
- 9. [Anti-Patterns to Avoid](references/instructions/09-anti-patterns-to-avoid.md) — when choosing an output or matching a use case.
- 10. [Notes](references/instructions/10-notes.md) — when this domain or mode is in scope.
- 11. [Validation Criteria](references/instructions/11-validation-criteria.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
