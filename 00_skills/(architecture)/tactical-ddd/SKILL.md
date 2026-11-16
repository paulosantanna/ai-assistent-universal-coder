---
name: tactical-ddd
description: "Detect anemic domain models and refactor to rich DDD models. Use for DDD model reviews. Do NOT use for service boundaries or DTOs."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Tactical DDD — Rich Domain Modeling

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Detects anemic domain models, validates and refactors them into rich domain models, and enforces tactical DDD patterns (Entities, Value Objects, Aggregates, Domain Services, Domain Events).

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Workflow](references/instructions/02-workflow.md) — at this step.
- 3. [Quick Anemia Signals (scan first)](references/instructions/03-quick-anemia-signals-scan-first.md) — when in scope.
- 4. [Golden Rules](references/instructions/04-golden-rules.md) — before acting.
- 5. [Output Format](references/instructions/05-output-format.md) — before acting.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
