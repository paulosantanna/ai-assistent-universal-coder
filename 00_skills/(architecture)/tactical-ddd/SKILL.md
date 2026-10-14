---
name: tactical-ddd
description: Detects anemic domain models, validates and refactors them into rich domain models, and enforces tactical DDD patterns (Entities, Value Objects, Aggregates, Domain Services, Domain Events). Use when the user asks to validate, review, or check domain models or DDD code; detect anemia; refactor domain objects; improve encapsulation; or mentions terms like "anemic model", "rich domain", "aggregate", "value object", "domain event", "ubiquitous language", "is this good DDD", "does this follow DDD", or "check my domain". Do NOT use for module or service boundary design, architectural decomposition, strategic DDD context mapping, or code outside the domain layer (DTOs, controllers, infrastructure adapters).
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Tactical DDD — Rich Domain Modeling

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Detects anemic domain models, validates and refactors them into rich domain models, and enforces tactical DDD patterns (Entities, Value Objects, Aggregates, Domain Services, Domain Events).

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Workflow](references/instructions/02-workflow.md) — at this step of execution.
- 3. [Quick Anemia Signals (scan first)](references/instructions/03-quick-anemia-signals-scan-first.md) — when this domain or mode is in scope.
- 4. [Golden Rules](references/instructions/04-golden-rules.md) — before acting on this contract.
- 5. [Output Format](references/instructions/05-output-format.md) — before acting on this contract.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
