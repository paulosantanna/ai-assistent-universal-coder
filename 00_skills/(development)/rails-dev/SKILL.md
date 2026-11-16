---
name: rails-dev
description: "Rails conventions (rich models, concerns, Minitest). Use for any Rails model, schema or code topic. Do NOT use for non-Rails backends."
license: CC-BY-4.0
metadata:
  author: William Calderipe - github.com/wcalderipe
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Rails Conventions

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Opinionated Rails conventions: rich models, concerns, CRUD-everything, state-as-records, minimal dependencies, Minitest with fixtures. Load this skill BEFORE any code-level thinking, not only before editing a file. It is required the moment a task touches Rails code in ANY way: designing or even just discussing a data model, schema, migration, entity, association, field, validation, class, or method name; writing, planning, reviewing, analyzing, testing, debugging, or refactoring; or proposing any model, table, column, route, or code snippet inline in chat. If you are about to name a model or sketch a column you are already in scope, even in an exploratory back-and-forth where no file is written yet. Do not let a "we're just discussing" framing defer it. 

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Core Philosophy](references/instructions/02-core-philosophy.md) — when in scope.
- 3. [Reference Selection](references/instructions/03-reference-selection.md) — when in scope.
- 4. [Coding style](references/instructions/04-coding-style.md) — when in scope.
- 5. [Sources](references/instructions/05-sources.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
