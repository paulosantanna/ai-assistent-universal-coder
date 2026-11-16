---
name: dependency-updater
description: "Update dependencies with minimal blast radius and evidence-backed compatibility. Use for dependency updates. Do NOT use for deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: dependency-updater

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Update dependencies with minimal blast radius and evidence-backed compatibility.

## Workflow
BRIEFING: target dependency, motivation, version policy, supported runtimes.
RECON: manifests, lockfiles, transitive graph, release notes, security advisories, current official docs, affected tests.
PLAN: smallest version movement that solves the requirement; migration notes; rollback.
EXECUTE: update manifest/lockfile only as required; no unrelated package churn.
VERIFY: install/build/type/static/unit/integration/contract/security checks applicable to the dependency.
DEBRIEF: record behavioral/API changes and update `.notebook/` when relevant.

## Rules
- Reuse existing dependencies before adding new ones.
- Never silently add packages.
- Never trust model memory for current signatures or deprecations.
- Flag breaking changes, CVEs, license changes and unsupported runtimes.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
