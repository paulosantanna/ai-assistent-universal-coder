---
name: frontend-design
description: "Create distinctive production UIs, avoiding generic AI looks. Use for pages or components. Do NOT use for design audits (web-design-guidelines)."
license: CC-BY-4.0
metadata:
  author: Impeccable (Paul Bakaus), based on Anthropic frontend-design
  version: 1.0.0
  owner_agent: codenavi-agent
source: https://github.com/pbakaus/impeccable
---

# Frontend Design

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Create distinctive, production-grade frontend interfaces with high design quality. Generates creative, polished code that avoids generic AI aesthetics. 

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Design Direction](references/instructions/02-design-direction.md) — when in scope.
- 3. [Frontend Aesthetics Guidelines](references/instructions/03-frontend-aesthetics-guidelines.md) — when in scope.
- 4. [The AI Slop Test](references/instructions/04-the-ai-slop-test.md) — before claiming completion.
- 5. [Examples](references/instructions/05-examples.md) — when choosing an output or matching a use case.
- 6. [Implementation Principles](references/instructions/06-implementation-principles.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
