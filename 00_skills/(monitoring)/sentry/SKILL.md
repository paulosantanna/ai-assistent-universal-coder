---
name: sentry
description: Inspect Sentry issues, summarize production errors, and pull health data via the Sentry API (read-only). Use when user says "check Sentry", "what errors in production?", "summarize Sentry issues", "recent crashes", or "production error report". Requires SENTRY_AUTH_TOKEN. Do NOT use for setting up Sentry SDK, configuring alerts, or non-Sentry error monitoring.
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Sentry (Read-only Observability)

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Inspect Sentry issues, summarize production errors, and pull health data via the Sentry API (read-only).

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Quick start](references/instructions/02-quick-start.md) — when this domain or mode is in scope.
- 3. [Core tasks (use bundled script)](references/instructions/03-core-tasks-use-bundled-script.md) — when this domain or mode is in scope.
- 4. [Skill path (set once)](references/instructions/04-skill-path-set-once.md) — when this domain or mode is in scope.
- 5. [API requirements](references/instructions/05-api-requirements.md) — when this domain or mode is in scope.
- 6. [Inputs and defaults](references/instructions/06-inputs-and-defaults.md) — before acting on this contract.
- 7. [Output formatting rules](references/instructions/07-output-formatting-rules.md) — before acting on this contract.
- 8. [Golden test inputs](references/instructions/08-golden-test-inputs.md) — before claiming completion.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
