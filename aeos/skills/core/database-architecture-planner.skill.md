# Skill: database-architecture-planner

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
