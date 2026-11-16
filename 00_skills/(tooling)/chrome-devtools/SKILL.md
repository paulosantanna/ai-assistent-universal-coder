---
name: chrome-devtools
description: "Debug and profile pages via Chrome DevTools MCP: console, network, performance. Use for 'debug this page'. Do NOT use for E2E (playwright-skill)."
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Chrome DevTools Agent

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Browser debugging, performance profiling, and automation via Chrome DevTools MCP.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Overview](references/instructions/02-overview.md) — when in scope.
- 3. [When to Use](references/instructions/03-when-to-use.md) — when in scope.
- 4. [Security Warning](references/instructions/04-security-warning.md) — before acting.
- 5. [Tool Categories](references/instructions/05-tool-categories.md) — when in scope.
- 6. [Workflow Patterns](references/instructions/06-workflow-patterns.md) — when choosing an output or matching a use case.
- 7. [Best Practices](references/instructions/07-best-practices.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
