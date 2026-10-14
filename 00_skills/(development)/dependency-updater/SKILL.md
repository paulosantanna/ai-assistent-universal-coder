---
name: dependency-updater
description: Update dependencies with minimal blast radius and evidence-backed compatibility. Use when the user requests dependency updater or invokes dependency-updater. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: dependency-updater

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
