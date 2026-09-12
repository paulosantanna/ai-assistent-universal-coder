---
name: kinghost-expert
description: Super-skill for deterministic KingHost WordPress/PHP changes and production FTP publish from the workspace, using already-provisioned credentials, cookie jars or Playwright.
---

# KingHost Expert Super-Skill

## Identity

A super-skill of the single canonical `codenavi-agent`. It creates no new agent identity. Specialization is implemented as internal lenses.

## Mission

Change authorized KingHost-hosted WordPress and PHP sites from the workspace and publish scoped artifacts to production through KingHost FTP, with deterministic environment selection, opaque credential binding, backup, dry-run, verification and rollback.

## Knowledge and MCP dependency

Material KingHost/WordPress/PHP/MySQL work uses:

- `kinghost-control` for deterministic environment, credential, FTP, PHP, MySQL and production FSM actions;
- `wordpress-knowledge` for WordPress API/security semantics;
- `wordpress-expert` lenses when mapping or mutating WordPress itself;
- `kinghost-commerce` when SSH/SFTP/Postgres commerce sessions are the safer protocol;
- `runtime-auth` / `runtime-http` for cookie sessions;
- `browser` or Playwright for panel/wp-admin confirmation and post-deploy smoke.

Official KingHost and WordPress documentation is normative. Undocumented private panel APIs are unsupported.

## Credential contract

Obtain **already created** logins by binding them from approved runtime sources. Do not invent, scrape, brute-force or persist passwords.

Approved sources:

1. environment variable references (`KINGHOST_FTP_USER`, `KINGHOST_FTP_PASSWORD`, MySQL equivalents);
2. approved secret-manager references materialized by `runtime-auth`;
3. ephemeral runtime memory supplied by the Tool Router;
4. KingHost panel or wp-admin **cookie/cookie-jar file** consumed in place, or Playwright using that cookie session to confirm identity and then bind FTP/MySQL from (1)–(3).

The model and notebook may see `credential_ref`, `session_ref`, username, host, port and environment id. They must never see passwords, cookie values, nonces or `wp-config.php` secrets.

## Deterministic production FSM

Every production publish follows this order. Skipping a state is a stop condition.

1. `IDLE`
2. `ENV_SELECTED` — `local` | `staging` | `production`
3. `CREDENTIALS_BOUND` — opaque FTP and optional MySQL/wp-admin refs
4. `PANEL_AUTH` — cookie or Playwright identity check
5. `INVENTORY` — remote scoped tree + WordPress/PHP metadata
6. `SNAPSHOT` — hashes/backup/`rollback_ref`
7. `DIFF` — workspace vs remote
8. `DRY_RUN` — FTP STOR/SQL list without mutation
9. `BACKUP` — confirm restore path
10. `APPLY` — approved scoped FTP/PHP/SQL
11. `VERIFY` — cookie/Playwright smoke of resulting state
12. `CLOSE` — destroy runtime credential material

`ROLLBACK` is legal from `APPLY` or `VERIFY` on failure.

Advance with `kinghost_control.fsm.advance`. Treat planning tools as plans until APPLY succeeds and VERIFY passes.

## Lenses

Use internal lenses, never subagents:

- `kinghost-environment`: plan limits, domain, PHP version, FTP root;
- `wordpress-architecture`: themes, plugins, hooks, REST, capabilities;
- `php-runtime`: version, ini, extensions, fatals;
- `mysql-safety`: read-first, EXPLAIN-first, reversible SQL;
- `ftp-publish`: scoped `wp-content` upload, no core edits;
- `panel-auth`: cookie/Playwright KingHost panel;
- `production-operations`: backup, smoke, cache, rollback.

## Mutation hierarchy

1. WordPress/plugin/theme settings via authenticated wp-admin/REST when safer;
2. workspace child theme or site plugin;
3. scoped FTP of `wp-content/themes`, `wp-content/plugins`, `wp-content/mu-plugins` or selected assets;
4. PHP version/ini through the KingHost PHP manager (panel cookie/Playwright);
5. MySQL only when no supported WordPress API exists.

Never edit WordPress core for feature work. `wp-config.php`, `wp-admin/` and `wp-includes/` require explicit high-risk approval.

## Cookie and Playwright

Primary panel/wp-admin authentication is an **external runtime cookie/cookie-jar file reference**. Playwright/browser may reuse that session to:

- choose the KingHost account/domain/environment;
- open FTP/MySQL/PHP/WordPress tools;
- verify production after FTP upload.

Cookie files stay outside the tracked workspace. Contents are never copied into Git, `.aeos` evidence, notebook, prompts or screenshots that would expose secrets.

## Production gates

Before APPLY:

- environment is explicit and matches the live host;
- credentials are bound as opaque refs;
- Beta Map exists for WordPress sites (`wordpress-expert` one-shot rule);
- scoped diff is bounded to requested files;
- backup/`rollback_ref` exists;
- dry-run evidence exists;
- `approved=true` and `change_id` are present;
- no secret material would be uploaded.

PASS requires verified front-end/wp-admin state, not FTP transfer success alone.

## Completion

Return `PASS`, `REVIEW`, `BLOCKED` or `ROLLBACK_REQUIRED` with environment id, change_id, redacted session refs, verification evidence and residual risk.
