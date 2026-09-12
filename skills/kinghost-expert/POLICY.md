# KingHost Expert Policy

## Risk classes

- read_only: environment catalog, inventory, FTP list/read, MySQL SELECT/SHOW, panel identity.
- medium: scoped workspace FTP dry-run, local PHP/WordPress edits.
- high: production FTP APPLY, PHP version changes, plugin/theme deploy.
- destructive: FTP delete, MySQL mutation, wp-config/core; explicit high-risk approval plus backup.

## Environment policy

Select `local`, `staging` or `production` before mutation. Local never uses KingHost FTP. Production defaults to dry-run until `approved=true`.

## Credential policy

Bind already-provisioned credentials. Forbidden: discovery, scraping, stuffing, dumping, or storing passwords in Git, evidence, memory, PHP or SQL files.

Cookie jars and Playwright may authenticate the panel; they may not copy revealed FTP/MySQL passwords into model-facing output. Bind those values through env/secret/runtime-memory into `credential_ref`.

## FSM policy

`kinghost_control.fsm.advance` must walk the production order. Illegal transitions fail closed.

## WordPress policy

Reuse `wordpress-expert` Beta Mapping rules. Do not remap automatically. Do not edit WordPress core for feature work.

## Verification policy

Playwright or cookie-backed HTTP smoke must confirm the changed URL/state. FTP 226/transfer success is not PASS.
