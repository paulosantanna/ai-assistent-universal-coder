---
name: kinghost-backup-recovery-expert
description: "Governed KingHost backup and rollback-safe restore: sites, databases, email. Use for KingHost backups. Do NOT use for unapproved prod changes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# KingHost Backup & Recovery Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Super-skill lens of the canonical `codenavi-agent`; no new agent identity.

## Mission

Plan, request, validate and restore KingHost backups for web/FTP content, supported databases and e-mail without destroying newer valid production state.

## Dependencies

- `kinghost-control`
- `kinghost-expert`
- governed `browser`/Playwright for panel-only backup requests
- `wordpress-expert` when WordPress/WooCommerce data is involved
- `00_skills/(cloud)/kinghost-expert/HOSTING_OPERATIONS.md`

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
