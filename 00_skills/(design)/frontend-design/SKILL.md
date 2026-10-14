---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications. Generates creative, polished code that avoids generic AI aesthetics. Do NOT use for design review or audit (use web-design-guidelines or web-quality-audit).
license: CC-BY-4.0
metadata:
  author: Impeccable (Paul Bakaus), based on Anthropic frontend-design
  version: 1.0.0
  owner_agent: codenavi-agent
source: https://github.com/pbakaus/impeccable
---

# Frontend Design

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications. Generates creative, polished code that avoids generic AI aesthetics. Do NOT use for design review or audit (use web-design-guidelines or web-quality-audit).

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Design Direction](references/instructions/02-design-direction.md) — when this domain or mode is in scope.
- 3. [Frontend Aesthetics Guidelines](references/instructions/03-frontend-aesthetics-guidelines.md) — when this domain or mode is in scope.
- 4. [The AI Slop Test](references/instructions/04-the-ai-slop-test.md) — before claiming completion.
- 5. [Examples](references/instructions/05-examples.md) — when choosing an output or matching a use case.
- 6. [Implementation Principles](references/instructions/06-implementation-principles.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
