---
name: rust-expert
description: Implement, diagnose, modernize and migrate real Rust projects with version-correct APIs, minimal diffs and evidence-backed verification. Use when the user requests rust expert or invokes rust-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: Tech Lead's Club / CodENavi
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Rust Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Implement, diagnose, modernize and migrate real Rust projects with version-correct APIs, minimal diffs and evidence-backed verification.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Mission](references/instructions/02-mission.md) — before acting on this contract.
- 3. [Routing](references/instructions/03-routing.md) — when this domain or mode is in scope.
- 4. [Execution](references/instructions/04-execution.md) — at this step of execution.
- 5. [Token Discipline](references/instructions/05-token-discipline.md) — when this domain or mode is in scope.
- 6. [Domain Expertise (Reference Index)](references/instructions/06-domain-expertise-reference-index.md) — when this domain or mode is in scope.
- 7. [Examples](references/instructions/07-examples.md) — when choosing an output or matching a use case.
- 8. [Troubleshooting](references/instructions/08-troubleshooting.md) — when an input, tool or check fails.
- 9. [Common Issues](references/instructions/09-common-issues.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).

Read [async-tokio.md](references/async-tokio.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [database-sqlx.md](references/database-sqlx.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [editions-toolchain.md](references/editions-toolchain.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [embedded.md](references/embedded.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [error-handling.md](references/error-handling.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [ffi.md](references/ffi.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [INDEX.md](references/INDEX.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [macros.md](references/macros.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [observability.md](references/observability.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [performance.md](references/performance.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [security.md](references/security.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [serialization.md](references/serialization.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [testing.md](references/testing.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [wasm.md](references/wasm.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [web-axum.md](references/web-axum.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [workspaces.md](references/workspaces.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
