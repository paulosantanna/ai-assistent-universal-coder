# Skill: kinghost-site-lifecycle

## Mission
Create, change, deploy, verify and roll back authorized KingHost-hosted sites through kinghost-commerce MCP.

## Uses MCP
- kinghost-commerce

## Operations
- CREATE_SITE
- MODIFY_SITE
- UPLOAD_FILES
- DEPLOY_RELEASE
- CONFIGURE_RUNTIME
- PLAN_DNS_SSL
- BACKUP
- RESTORE
- HEALTH_CHECK
- ROLLBACK

## Workflow
1. Obtain an opaque authenticated session from kinghost-secure-connection.
2. Inspect the real hosting plan, runtime, disk/database/resource constraints and current site state.
3. Snapshot/backup all mutation targets.
4. Produce deterministic diff/change-set and blast-radius analysis.
5. Execute CDC-style change-diff-control and dry-run/preflight.
6. Route production mutation through approval/Judge.
7. Apply the smallest atomic change possible.
8. Verify HTTP health, application behavior, logs, assets, DB compatibility and performance budget.
9. Roll back automatically when declared postconditions fail.
10. Write redacted evidence and close the session.

## Allowed Actions
Create directories/configuration supported by the plan; upload/update/delete explicitly scoped site files; publish releases; perform approved runtime/config changes; execute approved reversible migrations; restore a known-good release.

## Forbidden Actions
Unscoped recursive deletion; editing unrelated sites/accounts; exposing credentials; changing production without backup/preflight/approval; silently accepting failed health checks; bypassing provider limits.

## Output Schema
```json
{"status":"PASS|ROLLED_BACK|BLOCKED","change_set":[],"pre_state":{},"post_state":{},"verification":[],"rollback":{},"evidence_refs":[]}
```

## Quality Gates
Backup verified; diff bounded; approval present for production; health checks pass; no secret leakage; rollback tested or mechanically valid.