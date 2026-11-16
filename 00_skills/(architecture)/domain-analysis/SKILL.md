---
name: domain-analysis
description: "Map business domains and service boundaries with DDD strategy. Use for bounded contexts. Do NOT use to group existing components."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Subdomain Identification & Bounded Context Analysis

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Maps business domains and suggests service boundaries in any codebase using DDD Strategic Design.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [When to Use](references/instructions/02-when-to-use.md) — when in scope.
- 3. [Core Principles](references/instructions/03-core-principles.md) — when in scope.
- 4. [Analysis Process](references/instructions/04-analysis-process.md) — when in scope.
- 5. [Output Format](references/instructions/05-output-format.md) — before acting.
- 6. [Best Practices](references/instructions/06-best-practices.md) — when in scope.
- 7. [Analysis Checklist](references/instructions/07-analysis-checklist.md) — when in scope.
- 8. [Quick Reference](references/instructions/08-quick-reference.md) — when in scope.
- 9. [Anti-Patterns to Avoid](references/instructions/09-anti-patterns-to-avoid.md) — when choosing an output or matching a use case.
- 10. [Notes](references/instructions/10-notes.md) — when in scope.
- 11. [Validation Criteria](references/instructions/11-validation-criteria.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
