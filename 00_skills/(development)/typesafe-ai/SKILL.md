---
name: typesafe-ai
description: 'Build AI-powered software with TypeSafe: small units of AI intelligence you can use like programming primitives. Its System One models, including Jev, turn natural language and application state into typed judgments and probabilities that code can combine. Use when a feature needs programmable common sense, when brainstorming what AI could make possible in an app, or when an LLM prompt-and-parse step could become a structured decision. Applications include routing, ranking, extraction, verification, and interactive experiences; these are starting points, not the limits. Read live docs and cookbooks to find useful patterns and discover new combinations. Do NOT use for unrelated languages, domains or production deployment.'
license: MIT
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Build with TypeSafe

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Build AI-powered software with TypeSafe: small units of AI intelligence you can use like programming primitives. Its System One models, including Jev, turn natural language and application state into typed judgments and probabilities that code can combine.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Read the live docs](references/instructions/02-read-the-live-docs.md) — when this domain or mode is in scope.
- 3. [Find the useful shape](references/instructions/03-find-the-useful-shape.md) — when this domain or mode is in scope.
- 4. [Design the judgments](references/instructions/04-design-the-judgments.md) — when this domain or mode is in scope.
- 5. [Compose and verify](references/instructions/05-compose-and-verify.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
