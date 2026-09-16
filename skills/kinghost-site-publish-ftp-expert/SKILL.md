---
name: kinghost-site-publish-ftp-expert
description: Governed KingHost PHP/WordPress FTP publishing skill with bounded diffs, backup, approval, rollback and post-deploy verification.
---

# KingHost Site Publish FTP Expert

Super-skill lens of the canonical `codenavi-agent`; no new agent identity.

## Mission

Publish authorized PHP and WordPress site changes to KingHost over FTP without uncontrolled overwrites, secret leakage or unverified production state. The skill owns the FTP transport/publish workflow; application-specific engineering remains with `wordpress-expert` or the relevant PHP/application skill.

## Dependencies

- `kinghost-control`
- `kinghost-expert`
- `kinghost_control.ftp.tree.list`
- `kinghost_control.ftp.tree.upload`
- `kinghost_control.backup.plan`
- `kinghost_control.rollback.plan`
- `kinghost_control.publish.preflight`
- `kinghost-backup-recovery-expert`
- `wordpress-expert` for WordPress application logic
- `kinghost-security-expert` for security-sensitive production publication

## Non-negotiable production gates

1. Resolve the exact KingHost domain/environment with `domain.list` + `domain.select`.
2. Bind only already-provisioned FTP credentials as opaque refs.
3. Inventory the current remote tree and the candidate local tree.
4. Compute a bounded publish manifest/diff before any upload.
5. Reject path traversal and any destination outside the approved remote root.
6. Create/verify a backup or equivalent rollback point before destructive or overwrite publication.
7. Dry-run when supported and record the intended create/update/delete set.
8. Require approval/change id for production mutation.
9. Never upload credentials, raw cookies, private keys, local `.env`, editor metadata, build secrets or unintended database dumps.
10. Do not delete remote files merely because they are absent locally unless deletion is explicitly requested, reviewed and rollback-safe.
11. FTP transfer success is not deployment success. HTTP/application smoke is mandatory.

## Supported publication targets

### PHP site

May publish application code, public assets and approved runtime files under the selected remote root. Runtime-specific configuration must be validated separately against KingHost PHP capability and current application requirements.

### WordPress site

Default allowed publication scope is custom application content such as:

- `wp-content/themes/<approved-theme>`;
- `wp-content/plugins/<approved-plugin>`;
- approved `wp-content/mu-plugins`;
- static assets/uploads only when explicitly part of the change.

Default protected paths:

- `wp-config.php`;
- `.env` and secret-bearing config;
- `wp-admin/`;
- `wp-includes/`;
- WordPress core files;
- database dumps;
- server/private keys.

Protected paths require an explicit high-risk scope and owning-skill approval; ordinary feature publication must not touch them.

## Deterministic production workflow

`IDLE -> ENV_SELECTED -> CREDENTIALS_BOUND -> INVENTORY -> SNAPSHOT -> DIFF -> DRY_RUN -> BACKUP -> APPROVAL -> APPLY -> VERIFY -> CLOSE`

`ROLLBACK` is mandatory after APPLY/VERIFY failure when a safe rollback path exists.

### 1. Preflight

Use `kinghost_control.publish.preflight` and validate:

- selected domain/environment;
- local source root;
- remote destination root;
- FTP credential reference;
- protected/denied patterns;
- application type (`php|wordpress`);
- expected verification URLs/endpoints;
- backup/rollback readiness.

### 2. Inventory and diff

Build an explicit manifest with four categories:

- `CREATE`;
- `UPDATE`;
- `UNCHANGED`;
- `DELETE_CANDIDATE`.

`DELETE_CANDIDATE` is informational by default and is never executed without explicit destructive scope.

For changed files compare local/remote metadata and hashes when available. If remote checksum is unavailable, use the strongest available evidence such as size plus controlled post-upload readback; mark limitations explicitly.

### 3. Backup and rollback

Before overwrite/deletion:

- generate `backup.plan`;
- generate `rollback.plan`;
- snapshot all remote files that will be changed when the runtime supports it;
- keep rollback references outside public web roots when possible;
- ensure database rollback is handled separately when a release also contains schema/data changes.

### 4. Apply

Use `kinghost_control.ftp.tree.upload` under mutation gates.

Required behavior:

- upload only manifest-approved files;
- preserve binary files byte-for-byte;
- use bounded retries for transient failures;
- stop on permanent permission/path failures;
- never continue silently after partial critical upload;
- avoid partially exposing a release when an atomic/staged strategy is available;
- record per-file result without logging secret contents.

### 5. Verify

Verification must include the relevant subset of:

- remote manifest reconciliation;
- post-upload size/hash/readback where available;
- public HTTP status and expected page markers;
- PHP/application bootstrap smoke;
- WordPress front-end smoke;
- `wp-admin` reachability when authorized;
- plugin/theme activation/state checks when part of the change;
- WooCommerce cart/checkout/webhook smoke when commerce code is affected;
- cache purge/verification when stale content could mask the release;
- error/log review when available.

A successful FTP response alone must never produce `PASS`.

## Rollback triggers

Rollback or stop deployment on:

- incomplete critical upload;
- protected path mutation outside approved scope;
- HTTP 5xx/application fatal error after publish;
- integrity mismatch;
- missing expected files;
- WordPress/plugin/theme bootstrap failure;
- checkout/API/webhook regression for affected flows;
- inability to prove the deployed state matches the approved manifest.

## Completion states

Return one of:

- `PASS`: approved manifest published and application verification passed;
- `REVIEW`: publish succeeded but one non-critical verification dimension remains unavailable;
- `BLOCKED`: prerequisites, backup, approval, scope or credentials are unsafe/incomplete;
- `ROLLBACK_REQUIRED`: publish applied but verification failed or integrity is uncertain.

Evidence must include selected domain/environment, change id, redacted credential ref, manifest counts, backup/rollback refs, verification results and residual risk.