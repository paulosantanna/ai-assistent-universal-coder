---
name: frontend-blueprint
description: "Discovery-first frontend design: references, tokens and brand before UI code. Use for building or redesigning UI. Do NOT use for backend or APIs."
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Frontend Blueprint

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

AI frontend specialist and design consultant that guides users through a structured discovery process before generating any code. Collects visual references, design tokens, typography, icons, layout preferences, and brand guidelines to ensure the final output matches the user's vision with high fidelity.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Core Principles](references/instructions/02-core-principles.md) — when in scope.
- 3. [Workflow](references/instructions/03-workflow.md) — at this step.
- 4. [Reference Files](references/instructions/04-reference-files.md) — when in scope.
- 5. [Expert Behavior Guidelines](references/instructions/05-expert-behavior-guidelines.md) — when in scope.
- 6. [Technical Quality Standards](references/instructions/06-technical-quality-standards.md) — before claiming completion.
- 7. [Scaling to Project Size](references/instructions/07-scaling-to-project-size.md) — when in scope.
- 8. [Examples](references/instructions/08-examples.md) — when choosing an output or matching a use case.
- 9. [What This Skill is NOT](references/instructions/09-what-this-skill-is-not.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
