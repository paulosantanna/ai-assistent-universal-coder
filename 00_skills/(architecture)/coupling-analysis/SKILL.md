---
name: coupling-analysis
description: "Analyze module coupling (strength, distance, volatility). Use for coupling reports. Do NOT use for domain boundaries (domain-analysis)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Coupling Analysis Skill

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Analyzes coupling between modules using the three-dimensional model (strength, distance, volatility) from "Balancing Coupling in Software Design".

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [When to Use](references/instructions/02-when-to-use.md) — when in scope.
- 3. [Process](references/instructions/03-process.md) — when in scope.
- 4. [Quick Reference: Pattern → Integration Strength](references/instructions/04-quick-reference-pattern-integration-strength.md) — when choosing an output or matching a use case.
- 5. [Quick Heuristics](references/instructions/05-quick-heuristics.md) — when in scope.
- 6. [Known Limitations](references/instructions/06-known-limitations.md) — when in scope.
- 7. [Book References](references/instructions/07-book-references.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
