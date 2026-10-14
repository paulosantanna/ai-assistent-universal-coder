---
name: evolutionary-modular-architecture
description: Guides design and implementation of evolutionary modular-monolith platforms with DDD (strategic + tactical), flat-by-aggregate organization, an Anti-Corruption Layer for vendor independence, a transactional outbox for events, smart resilience (backoff with jitter, circuit breakers, idempotency), and a polished architecture HTML document with elegant SVG diagrams. Use when designing a platform or backend, defining bounded contexts, organizing modules and folders, choosing monolith vs microservices, decoupling from an external service (ERP, storage, AI), making calls resilient, adding real-time push, picking a 2026 TypeScript stack (Nx, NestJS, React), or producing an architecture document or diagram. Also triggers on 'modular monolith', 'bounded contexts', 'flat-by-aggregate', 'ports and adapters', 'architecture diagram'. Do NOT use for simple CRUD, NestJS-only deep implementation (use nestjs-modular-monolith), or pure domain-model review (use tactical-ddd).
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Evolutionary Modular Architecture

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Guides design and implementation of evolutionary modular-monolith platforms with DDD (strategic + tactical), flat-by-aggregate organization, an Anti-Corruption Layer for vendor independence, a transactional outbox for events, smart resilience (backoff with jitter, circuit breakers, idempotency), and a polished architecture HTML document with elegant SVG diagrams.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [When to use this skill](references/instructions/02-when-to-use-this-skill.md) — when this domain or mode is in scope.
- 3. [When NOT to use it](references/instructions/03-when-not-to-use-it.md) — when this domain or mode is in scope.
- 4. [The one rule that governs everything](references/instructions/04-the-one-rule-that-governs-everything.md) — before acting on this contract.
- 5. [Core model (load the matching reference when you go deep)](references/instructions/05-core-model-load-the-matching-reference-when-you-go-deep.md) — when this domain or mode is in scope.
- 6. [Workflow](references/instructions/06-workflow.md) — at this step of execution.
- 7. [Decision rules (cheat sheet)](references/instructions/07-decision-rules-cheat-sheet.md) — before acting on this contract.
- 8. [Hard rules (non-negotiable)](references/instructions/08-hard-rules-non-negotiable.md) — before acting on this contract.
- 9. [Automated checks](references/instructions/09-automated-checks.md) — when this domain or mode is in scope.
- 10. [Examples](references/instructions/10-examples.md) — when choosing an output or matching a use case.
- 11. [Anti-patterns / red flags](references/instructions/11-anti-patterns-red-flags.md) — when choosing an output or matching a use case.
- 12. [Reference guide](references/instructions/12-reference-guide.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
