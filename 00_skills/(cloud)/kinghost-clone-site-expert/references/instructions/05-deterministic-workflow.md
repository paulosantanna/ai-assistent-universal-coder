<!-- Package: 00_skills/(cloud)/kinghost-clone-site-expert; relative command/resource examples resolve from that package or workspace root. -->

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
