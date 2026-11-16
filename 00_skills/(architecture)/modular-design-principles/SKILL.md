---
name: modular-design-principles
description: "Modular design principles: bounded contexts, boundaries, contracts, splits. Use for module structure reviews. Do NOT use for decomposition pipelines."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Modular Design Principles

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Technology-agnostic guidance for modular systems: bounded contexts, clear boundaries, composability, state isolation, explicit contracts, failure containment, scaffolding workflows, split/merge criteria, sub-units inside a context, and compliance review signals.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [What to load](references/instructions/02-what-to-load.md) — when in scope.
- 3. [Layered mental model](references/instructions/03-layered-mental-model.md) — when in scope.
- 4. [The ten principles](references/instructions/04-the-ten-principles.md) — when in scope.
- 5. [Typical violations (stated abstractly)](references/instructions/05-typical-violations-stated-abstractly.md) — when in scope.
- 6. [Creating a bounded context (workflow)](references/instructions/06-creating-a-bounded-context-workflow.md) — at this step.
- 7. [When to split or merge](references/instructions/07-when-to-split-or-merge.md) — when in scope.
- 8. [Sub-units inside a bounded context](references/instructions/08-sub-units-inside-a-bounded-context.md) — when in scope.
- 9. [Architecture compliance pass](references/instructions/09-architecture-compliance-pass.md) — when in scope.
- 10. [Quick checklist (before proposing structure)](references/instructions/10-quick-checklist-before-proposing-structure.md) — when in scope.
- 11. [Relationship to stack-specific skills](references/instructions/11-relationship-to-stack-specific-skills.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
