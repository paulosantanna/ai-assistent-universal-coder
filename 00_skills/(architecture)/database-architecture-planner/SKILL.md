---
name: database-architecture-planner
description: Plan database architecture, schema governance, migrations, backup, restore and production safety for any requested database. Use when the user requests database architecture planner or invokes database-architecture-planner. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: database-architecture-planner

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Plan database architecture, schema governance, migrations, backup, restore and production safety for any requested database.

## Allowed Actions

- Read authorized requirements and evidence refs.
- Generate schema and migration plans in sandbox.
- Request documentation MCPs when database-specific behavior is claimed.
- Generate rollback and backup/restore requirements.

## Forbidden Actions

- Run database mutations.
- Invent credentials or connection strings.
- Skip migration, rollback or backup planning.
- Claim database-specific limits without evidence.

## Required Inputs

- database
- data_model_scope
- consistency_requirements
- migration_strategy
- deployment_target
- token_budget

## Output Schema

```json
{
  "status": "PASS|REVIEW|BLOCKED",
  "database_plan": {},
  "migration_plan": {},
  "backup_restore_plan": {},
  "risks": [],
  "evidence_refs": [],
  "blocking_conditions": []
}
```

## Quality Gates

- Migration strategy is reversible or explicitly marked as one-way.
- Secrets remain outside generated source.
- Backup and restore are documented.
- Database health checks and observability are included.
- Token budget is respected.

## Stop Conditions

- Database choice missing.
- Migration strategy missing.
- Credentials requested or exposed.
- Backup/restore omitted for production-bound systems.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
