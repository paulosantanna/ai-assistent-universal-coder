# Skill: dependency-updater
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
