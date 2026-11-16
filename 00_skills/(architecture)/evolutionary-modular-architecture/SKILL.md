---
name: evolutionary-modular-architecture
description: "Design modular monoliths: DDD contexts, ports and adapters, resilience. Use for platform design. Do NOT use for simple CRUD or tactical-ddd review."
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Evolutionary Modular Architecture

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Guides design and implementation of evolutionary modular-monolith platforms with DDD (strategic + tactical), flat-by-aggregate organization, an Anti-Corruption Layer for vendor independence, a transactional outbox for events, smart resilience (backoff with jitter, circuit breakers, idempotency), and a polished architecture HTML document with elegant SVG diagrams.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [When to use this skill](references/instructions/02-when-to-use-this-skill.md) — when in scope.
- 3. [When NOT to use it](references/instructions/03-when-not-to-use-it.md) — when in scope.
- 4. [The one rule that governs everything](references/instructions/04-the-one-rule-that-governs-everything.md) — before acting.
- 5. [Core model (load the matching reference when you go deep)](references/instructions/05-core-model-load-the-matching-reference-when-you-go-deep.md) — when in scope.
- 6. [Workflow](references/instructions/06-workflow.md) — at this step.
- 7. [Decision rules (cheat sheet)](references/instructions/07-decision-rules-cheat-sheet.md) — before acting.
- 8. [Hard rules (non-negotiable)](references/instructions/08-hard-rules-non-negotiable.md) — before acting.
- 9. [Automated checks](references/instructions/09-automated-checks.md) — when in scope.
- 10. [Examples](references/instructions/10-examples.md) — when choosing an output or matching a use case.
- 11. [Anti-patterns / red flags](references/instructions/11-anti-patterns-red-flags.md) — when choosing an output or matching a use case.
- 12. [Reference guide](references/instructions/12-reference-guide.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
