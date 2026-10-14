---
name: react-best-practices
description: React and Next.js performance optimization guidelines from Vercel Engineering. Use when writing, reviewing, or refactoring React/Next.js code to ensure optimal performance patterns. Triggers on tasks involving React components, Next.js pages, data fetching, bundle optimization, or performance improvements. Do NOT use for component API architecture or composition patterns (use react-composition-patterns instead).
license: MIT
metadata:
  author: vercel
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Vercel React Best Practices

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

React and Next.js performance optimization guidelines from Vercel Engineering.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [When to Apply](references/instructions/02-when-to-apply.md) — when this domain or mode is in scope.
- 3. [Rule Categories by Priority](references/instructions/03-rule-categories-by-priority.md) — before acting on this contract.
- 4. [Quick Reference](references/instructions/04-quick-reference.md) — when this domain or mode is in scope.
- 5. [How to Use](references/instructions/05-how-to-use.md) — when this domain or mode is in scope.
- 6. [Full Compiled Document](references/instructions/06-full-compiled-document.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
