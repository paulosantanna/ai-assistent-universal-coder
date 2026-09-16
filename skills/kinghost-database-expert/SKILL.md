---
name: kinghost-database-expert
description: Governed KingHost MySQL/database engineering skill for creation, access, backup, query analysis, migration and recovery.
---

# KingHost Database Expert

Super-skill lens of the canonical `codenavi-agent`; no new agent identity.

## Mission

Create, inspect, access, back up, migrate, tune and recover authorized KingHost databases with read-first SQL, reversible changes and application verification.

## Dependencies

- `kinghost-control` MySQL session/query tools
- governed browser/Playwright for panel/phpMyAdmin provisioning
- `kinghost-backup-recovery-expert`
- `skills/kinghost-expert/HOSTING_OPERATIONS.md`

## Creation/access

1. select domain/environment;
2. create database/user only through documented panel flow;
3. configure the minimum network/IP exposure required;
4. bind credentials as opaque `credential_ref`;
5. verify connectivity with metadata/read-only query;
6. never persist DB passwords, wp-config secrets or connection strings containing credentials.

## Query policy

Read-only default: `SELECT`, `SHOW`, `DESCRIBE`, `EXPLAIN`. Mutation requires bounded SQL, parameterization where applicable, approval, `change_id`, `rollback_ref`, backup and dry-run evidence. `DROP`, `TRUNCATE`, privilege changes and bulk load are high risk.

## Migration

Prefer versioned migrations from the application repository. Validate schema version, row counts/checksums where suitable, indexes/constraints and application compatibility. Avoid ad-hoc production edits in phpMyAdmin when the same change belongs in versioned code.

## Performance

Use EXPLAIN/query evidence before adding indexes or rewriting SQL. Measure application latency and resource effect after changes; an index that accelerates reads but materially harms writes/storage is not automatically an improvement.

## Backup/recovery

Database backup is dump-based according to KingHost documentation. Restore is a production mutation and requires a snapshot of the current state plus post-restore schema/data/application smoke.

For WordPress/WooCommerce, preserve current production orders/customers/payment state unless the approved recovery scope explicitly requires replacing it.
