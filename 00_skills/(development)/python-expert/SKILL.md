---
name: python-expert
description: Implement, diagnose, test and modernize production Python projects with version-correct APIs and repository-native packaging, typing, async and framework conventions. Python is allowed in this workspace; AEOS kernel/runtime orchestration stays Node/TypeScript unless a later mission changes that surface. Use when the user requests python expert or invokes python-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Python Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi Full Workspace v2

## Mission
Implement, diagnose, test and modernize production Python projects with version-correct APIs and repository-native packaging, typing, async and framework conventions. Python is allowed in this workspace; AEOS kernel/runtime orchestration stays Node/TypeScript unless a later mission changes that surface.

## Recon
Detect interpreter constraint, `pyproject.toml`/lockfiles, environment manager, entry points, sync/async boundaries, frameworks, typing/lint/test stack and deployment runtime. Query `docs-python-current` narrowly for signatures/behavior when needed.

## Execute
Use idiomatic code for the declared Python version; preserve project conventions; avoid package additions if an existing dependency suffices; make surgical changes.

## Verify
Project-native type/lint/tests, import/package build, startup/runtime and security/performance checks when affected.

## Token discipline
Read `references/INDEX.md`; open at most the modules needed for the detected packaging/runtime/problem domain.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [async-typing-testing.md](references/async-typing-testing.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [packaging-runtime.md](references/packaging-runtime.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
