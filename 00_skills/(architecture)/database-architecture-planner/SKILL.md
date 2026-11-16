---
name: database-architecture-planner
description: "Plan database architecture: schema governance, migrations, backup, restore. Use for DB planning. Do NOT use for implementation or deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: database-architecture-planner

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
