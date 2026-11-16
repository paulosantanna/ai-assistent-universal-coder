---
name: sentry
description: "Inspect Sentry issues and production errors via the read-only API. Use for 'check Sentry' reports. Do NOT use for SDK setup or alerts."
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Sentry (Read-only Observability)

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Inspect Sentry issues, summarize production errors, and pull health data via the Sentry API (read-only).

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Quick start](references/instructions/02-quick-start.md) — when in scope.
- 3. [Core tasks (use bundled script)](references/instructions/03-core-tasks-use-bundled-script.md) — when in scope.
- 4. [Skill path (set once)](references/instructions/04-skill-path-set-once.md) — when in scope.
- 5. [API requirements](references/instructions/05-api-requirements.md) — when in scope.
- 6. [Inputs and defaults](references/instructions/06-inputs-and-defaults.md) — before acting.
- 7. [Output formatting rules](references/instructions/07-output-formatting-rules.md) — before acting.
- 8. [Golden test inputs](references/instructions/08-golden-test-inputs.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
