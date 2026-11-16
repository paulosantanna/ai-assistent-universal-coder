---
name: python-expert
description: "Implement, diagnose, test and modernize Python projects with version-correct APIs. Use for Python work. Do NOT use for other languages."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Python Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [async-typing-testing.md](references/async-typing-testing.md) only when the domain workflow needs it; root governance and this entry take precedence.
Read [packaging-runtime.md](references/packaging-runtime.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
