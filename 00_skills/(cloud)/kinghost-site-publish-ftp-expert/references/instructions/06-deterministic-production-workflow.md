<!-- Package: 00_skills/(cloud)/kinghost-site-publish-ftp-expert; relative command/resource examples resolve from that package or workspace root. -->

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
