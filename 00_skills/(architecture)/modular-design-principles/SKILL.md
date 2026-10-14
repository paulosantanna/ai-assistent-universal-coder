---
name: modular-design-principles
description: 'Technology-agnostic guidance for modular systems: bounded contexts, clear boundaries, composability, state isolation, explicit contracts, failure containment, scaffolding workflows, split/merge criteria, sub-units inside a context, and compliance review signals. Use when designing or reviewing module structure, service boundaries, package layout, cross-cutting dependencies, "how should we split this?", modularity assessments, coupling between domains, greenfield context design, or architecture discussions without assuming a specific framework, language, or repository layout. Do NOT use for executing the full Patterns 1–5 repo decomposition pipeline or per-pattern inventories (use modular-decomposition), phased extraction roadmaps as the main deliverable (use decomposition-planning-roadmap), or end-to-end legacy migration strategy (use legacy-migration-planner).'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Modular Design Principles

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Technology-agnostic guidance for modular systems: bounded contexts, clear boundaries, composability, state isolation, explicit contracts, failure containment, scaffolding workflows, split/merge criteria, sub-units inside a context, and compliance review signals.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [What to load](references/instructions/02-what-to-load.md) — when this domain or mode is in scope.
- 3. [Layered mental model](references/instructions/03-layered-mental-model.md) — when this domain or mode is in scope.
- 4. [The ten principles](references/instructions/04-the-ten-principles.md) — when this domain or mode is in scope.
- 5. [Typical violations (stated abstractly)](references/instructions/05-typical-violations-stated-abstractly.md) — when this domain or mode is in scope.
- 6. [Creating a bounded context (workflow)](references/instructions/06-creating-a-bounded-context-workflow.md) — at this step of execution.
- 7. [When to split or merge](references/instructions/07-when-to-split-or-merge.md) — when this domain or mode is in scope.
- 8. [Sub-units inside a bounded context](references/instructions/08-sub-units-inside-a-bounded-context.md) — when this domain or mode is in scope.
- 9. [Architecture compliance pass](references/instructions/09-architecture-compliance-pass.md) — when this domain or mode is in scope.
- 10. [Quick checklist (before proposing structure)](references/instructions/10-quick-checklist-before-proposing-structure.md) — when this domain or mode is in scope.
- 11. [Relationship to stack-specific skills](references/instructions/11-relationship-to-stack-specific-skills.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
