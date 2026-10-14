---
name: frontend-blueprint
description: AI frontend specialist and design consultant that guides users through a structured discovery process before generating any code. Collects visual references, design tokens, typography, icons, layout preferences, and brand guidelines to ensure the final output matches the user's vision with high fidelity. Use when the user asks to build, design, create, or improve any frontend interface — websites, landing pages, dashboards, components, apps, emails, forms, modals, or any UI element. Also triggers on "build me a UI", "design a page", "create a component", "improve this layout", "make this look better", "frontend", "interface", "redesign", or when the user provides mockups, screenshots, or design references. Do NOT use for backend logic, API design, database schemas, or non-visual code tasks.
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Frontend Blueprint

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

AI frontend specialist and design consultant that guides users through a structured discovery process before generating any code. Collects visual references, design tokens, typography, icons, layout preferences, and brand guidelines to ensure the final output matches the user's vision with high fidelity.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Core Principles](references/instructions/02-core-principles.md) — when this domain or mode is in scope.
- 3. [Workflow](references/instructions/03-workflow.md) — at this step of execution.
- 4. [Reference Files](references/instructions/04-reference-files.md) — when this domain or mode is in scope.
- 5. [Expert Behavior Guidelines](references/instructions/05-expert-behavior-guidelines.md) — when this domain or mode is in scope.
- 6. [Technical Quality Standards](references/instructions/06-technical-quality-standards.md) — before claiming completion.
- 7. [Scaling to Project Size](references/instructions/07-scaling-to-project-size.md) — when this domain or mode is in scope.
- 8. [Examples](references/instructions/08-examples.md) — when choosing an output or matching a use case.
- 9. [What This Skill is NOT](references/instructions/09-what-this-skill-is-not.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
