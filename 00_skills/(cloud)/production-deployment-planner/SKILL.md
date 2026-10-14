---
name: production-deployment-planner
description: Plan production packaging, CI/CD, deployment, observability, rollback and operational readiness for any architecture. Use when the user requests production deployment planner or invokes production-deployment-planner. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: production-deployment-planner

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Plan production packaging, CI/CD, deployment, observability, rollback and operational readiness for any architecture.

## Allowed Actions

- Read authorized build, deployment and evidence refs.
- Generate deployment plans and sandbox artifacts.
- Generate CI/CD and rollback checklists.
- Route final deployment readiness through Judge.

## Forbidden Actions

- Deploy automatically.
- Generate or expose secrets.
- Skip rollback.
- Skip observability.
- Treat local success as production readiness.

## Required Inputs

- architecture
- languages
- databases
- deployment_target
- ci_provider
- token_budget

## Output Schema

```json
{
  "status": "PASS|REVIEW|BLOCKED",
  "deployment_plan": {},
  "ci_cd_plan": {},
  "observability_plan": {},
  "rollback_plan": {},
  "readiness_gates": [],
  "blocking_conditions": []
}
```

## Quality Gates

- Build artifact is explicit for every runtime.
- CI/CD includes test and security gates.
- Deployment target and rollback are explicit.
- Observability includes logs, metrics and traces when applicable.
- Token budget is respected.

## Stop Conditions

- Deployment target missing.
- CI provider missing or explicitly out of scope.
- Rollback missing.
- Secret handling undefined.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
