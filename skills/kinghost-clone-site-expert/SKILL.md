---
name: kinghost-clone-site-expert
description: Governed KingHost full-site clone skill that acquires an integrity-verified FTP copy without mutating the remote origin and without silently losing files.
---

# KingHost Clone Site Expert

Super-skill lens of the canonical `codenavi-agent`; no new agent identity.

## Mission

Clone an authorized KingHost-hosted site from FTP into a controlled workspace as completely and reproducibly as the selected FTP account permits, preserving directory structure, filenames, binary payloads and evidence of transfer integrity while never mutating the remote source.

This skill means **absolute clone of the FTP-visible site tree**. It must not falsely claim that FTP alone contains database rows, mailbox data, DNS, panel settings, cron configuration or secrets. For WordPress/PHP sites that also require database state, delegate the data portion to `kinghost-database-expert` / `kinghost-backup-recovery-expert` and report the combined result explicitly.

## Dependencies

- `kinghost-control`
- `kinghost-expert`
- `kinghost_control.site.clone`
- `kinghost_control.ftp.tree.list`
- `kinghost_control.ftp.tree.download`
- `kinghost-backup-recovery-expert` when a recovery point or database snapshot is required
- `kinghost-database-expert` for MySQL state
- `wordpress-expert` when the cloned tree is WordPress

## Safety contract

1. Select the exact environment/domain with `domain.list` + `domain.select` before transfer.
2. Bind an already-provisioned FTP identity through `kinghost_control.credential.bind`; passwords remain opaque/runtime-only.
3. Remote clone operations are read-only. This skill must never call upload/delete/mkdir or any mutation tool while in clone mode.
4. Inventory the entire reachable remote root before downloading.
5. Preserve relative paths exactly; reject path traversal and writes outside the approved local destination.
6. Transfer binary files as binary data; never normalize line endings or rewrite payloads during clone.
7. Detect and report inaccessible files, permission errors, symlink-like entries, unsupported node types, interrupted transfers and name collisions.
8. `wp-config.php`, `.env`, private keys and other secret-bearing files are not exposed to the model/evidence. If policy excludes them from materialization, record them as `SECRET_EXCLUDED`, not as silently missing.
9. Never overwrite a non-empty local destination unless an explicit destination policy and rollback/snapshot exist.
10. A successful FTP status is not PASS. Completion requires inventory reconciliation and integrity evidence.

## Deterministic workflow

`ENV_SELECTED -> CREDENTIALS_BOUND -> INVENTORY -> LOCAL_DESTINATION_CHECK -> CLONE_PLAN -> DOWNLOAD -> RECONCILE -> INTEGRITY_VERIFY -> APPLICATION_CLASSIFY -> CLOSE`

### 1. Inventory

- resolve remote root;
- recursively enumerate directories/files with `ftp.tree.list`;
- record relative path, entry type and size when available;
- classify secret-sensitive paths before materialization;
- establish expected object/file counts and total bytes when metadata permits.

### 2. Clone plan

Create a bounded plan containing:

- selected KingHost domain/environment;
- remote root;
- local destination;
- include/exclude policy;
- secret handling policy;
- expected file/directory counts;
- retry policy for transient reads;
- integrity strategy.

### 3. Download

Prefer `kinghost_control.site.clone` for the governed clone path and `ftp.tree.download` for bounded/retry operations.

Required behavior:

- recursive traversal;
- no remote mutations;
- resumable/idempotent local writes where supported;
- bounded retries for transient network failures;
- explicit failure for unresolved permanent read errors;
- no invented placeholder files.

### 4. Reconciliation and integrity

At minimum compare:

- expected vs downloaded relative paths;
- expected vs downloaded file count;
- expected vs downloaded sizes where available;
- local hashes for all downloaded files;
- remote checksums when the protocol/runtime can obtain them; otherwise mark checksum parity as `UNAVAILABLE`, never inferred.

Classify every expected path exactly once as `COPIED`, `SECRET_EXCLUDED`, `INACCESSIBLE`, `UNSUPPORTED` or `FAILED`.

`PASS` is allowed only when no path is silently unaccounted for.

## WordPress/PHP completeness

For WordPress/PHP, FTP clone represents the filesystem layer only. Report separately:

- filesystem clone status;
- database clone/snapshot status;
- secrets/config status;
- uploads/media status;
- application verification readiness.

A full WordPress site clone requires both filesystem and the appropriate MySQL state. Never label an FTP-only copy as a complete application clone when database-backed content exists.

## Evidence

Return redacted evidence containing:

- domain/environment;
- remote root/local destination;
- expected/copied/excluded/failed counts;
- aggregate bytes when available;
- integrity method;
- missing/inaccessible path list without secret contents;
- database-required flag;
- final status.

## Completion states

- `PASS`: every FTP-visible path is accounted for and all required integrity checks pass.
- `REVIEW`: clone completed but protocol limitations prevent one or more strong integrity assertions.
- `BLOCKED`: authentication, permissions, ambiguous root or local safety prevents a trustworthy clone.
- `PARTIAL`: one or more expected paths could not be copied; never present this as success.

No successful clone claim is permitted with unexplained missing files.