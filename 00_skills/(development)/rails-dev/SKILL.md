---
name: rails-dev
description: 'Opinionated Rails conventions: rich models, concerns, CRUD-everything, state-as-records, minimal dependencies, Minitest with fixtures. Load this skill BEFORE any code-level thinking, not only before editing a file. It is required the moment a task touches Rails code in ANY way: designing or even just discussing a data model, schema, migration, entity, association, field, validation, class, or method name; writing, planning, reviewing, analyzing, testing, debugging, or refactoring; or proposing any model, table, column, route, or code snippet inline in chat. If you are about to name a model or sketch a column you are already in scope, even in an exploratory back-and-forth where no file is written yet. Do not let a "we''re just discussing" framing defer it. Do NOT use for non-Rails backends, NestJS, or general architecture (use nestjs-modular-monolith or coding-guidelines). Use when the user requests rails dev or invokes rails-dev.'
license: CC-BY-4.0
metadata:
  author: William Calderipe - github.com/wcalderipe
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Rails Conventions

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Opinionated Rails conventions: rich models, concerns, CRUD-everything, state-as-records, minimal dependencies, Minitest with fixtures. Load this skill BEFORE any code-level thinking, not only before editing a file. It is required the moment a task touches Rails code in ANY way: designing or even just discussing a data model, schema, migration, entity, association, field, validation, class, or method name; writing, planning, reviewing, analyzing, testing, debugging, or refactoring; or proposing any model, table, column, route, or code snippet inline in chat. If you are about to name a model or sketch a column you are already in scope, even in an exploratory back-and-forth where no file is written yet. Do not let a "we're just discussing" framing defer it. Do NOT use for non-Rails backends, NestJS, or general architecture (use nestjs-modular-monolith or coding-guidelines).

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Core Philosophy](references/instructions/02-core-philosophy.md) — when this domain or mode is in scope.
- 3. [Reference Selection](references/instructions/03-reference-selection.md) — when this domain or mode is in scope.
- 4. [Coding style](references/instructions/04-coding-style.md) — when this domain or mode is in scope.
- 5. [Sources](references/instructions/05-sources.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
