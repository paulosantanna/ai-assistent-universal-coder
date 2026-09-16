---
name: kinghost-backup-recovery-expert
description: Governed KingHost backup and recovery skill for sites/FTP, databases and email with rollback-safe restore verification.
---

# KingHost Backup & Recovery Expert

Super-skill lens of the canonical `codenavi-agent`; no new agent identity.

## Mission

Plan, request, validate and restore KingHost backups for web/FTP content, supported databases and e-mail without destroying newer valid production state.

## Dependencies

- `kinghost-control`
- `kinghost-expert`
- governed `browser`/Playwright for panel-only backup requests
- `wordpress-expert` when WordPress/WooCommerce data is involved
- `skills/kinghost-expert/HOSTING_OPERATIONS.md`

## Rules

1. `domain.list` + `domain.select` before any operation.
2. `knowledge_search("backup restore ftp database email")` before plan execution.
3. Capture current-state snapshot/hashes/schema metadata before restore.
4. Treat documented KingHost retention as a live-plan fact to confirm in panel, not a timeless guarantee.
5. Web/FTP and e-mail recovery may be differential; database recovery is dump-based according to current official documentation.
6. Never copy database dumps, mailbox content, passwords or cookies into evidence/model context.
7. Restore requires explicit approval, change_id and rollback_ref.
8. WooCommerce orders/customers are preserved unless recovery scope explicitly authorizes replacing them.

## Workflows

### Backup request
`INVENTORY -> SELECT_TYPE -> SELECT_RECOVERY_POINT -> REQUEST -> DELIVERY_REFERENCE -> VERIFY`

### Restore
`INVENTORY -> CURRENT_SNAPSHOT -> RECOVERY_POINT -> DIFF -> APPROVAL -> RESTORE -> APPLICATION_SMOKE -> DATA_SMOKE -> CLOSE`

## Verification

- FTP/site: expected files/hashes + HTTP smoke.
- Database: connectivity, schema/table counts, representative read queries, application smoke.
- E-mail: requested mailbox/folder recovery visible without exposing message contents.
- WordPress: front-end/wp-admin/plugin state and, for commerce, representative product/order integrity checks.

Return `PASS|REVIEW|BLOCKED|ROLLBACK_REQUIRED` with redacted evidence only.
