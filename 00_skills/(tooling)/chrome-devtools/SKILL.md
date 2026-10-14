---
name: chrome-devtools
description: Browser debugging, performance profiling, and automation via Chrome DevTools MCP. Use when user says "debug this page", "take a screenshot", "check network requests", "profile performance", "inspect console errors", or "analyze page load". Do NOT use for full E2E test suites (use playwright-skill) or non-browser debugging.
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Chrome DevTools Agent

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Browser debugging, performance profiling, and automation via Chrome DevTools MCP.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Overview](references/instructions/02-overview.md) — when this domain or mode is in scope.
- 3. [When to Use](references/instructions/03-when-to-use.md) — when this domain or mode is in scope.
- 4. [Security Warning](references/instructions/04-security-warning.md) — before acting on this contract.
- 5. [Tool Categories](references/instructions/05-tool-categories.md) — when this domain or mode is in scope.
- 6. [Workflow Patterns](references/instructions/06-workflow-patterns.md) — when choosing an output or matching a use case.
- 7. [Best Practices](references/instructions/07-best-practices.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
