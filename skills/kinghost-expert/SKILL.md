---
name: kinghost-expert
description: Super-skill for KingHost Hospedagem: cookie-jar panel login, domain list/select, already-created users, WordPress/PHP/MySQL/WooCommerce changes, site clone and production FTP publish from the workspace.
---

# KingHost Expert Super-Skill

## Identity

A super-skill of the single canonical `codenavi-agent`. It creates no new agent identity. Specialization is implemented as internal lenses.

## Mission

Operate authorized KingHost Hospedagem accounts from the workspace: authenticate the control panel with an external cookie jar, list and select existing domains, read already-created users, clone WordPress/PHP sites, change scoped artifacts (including e-commerce plugins such as WooCommerce), integrate PHP/WordPress with MySQL, and publish the locally altered tree to production through KingHost FTP.

The one-command path for a site that is already hosted and already altered locally is playbook `kinghost-wordpress-publish`:

```bash
npm run aeos:kinghost:publish -- --local-dir <wordpress-tree> --domain <existing-kinghost-domain>
```

## Knowledge and MCP dependency

Material KingHost/WordPress/PHP/MySQL work uses:

- `kinghost-control` as the executable control plane (cookie login, domains, users, clone, FTP tree, MySQL, production FSM);
- `kinghost_control.knowledge_search` before claiming panel/FTP/MySQL/WordPress hosting facts;
- `wordpress-knowledge` for WordPress API/security semantics;
- `wordpress-expert` lenses when mapping or mutating WordPress itself;
- `kinghost-commerce` only when SSH/SFTP/Postgres commerce sessions are the safer protocol;
- `runtime-auth` / `runtime-http` for additional cookie sessions;
- `browser` or Playwright for panel/wp-admin confirmation and post-deploy smoke.

Official KingHost wiki (`https://king.host/wiki/`, panel `https://painel.kinghost.com.br`) and WordPress documentation are normative. Undocumented private panel APIs are unsupported and fail closed.

## Credential contract

Obtain **already created** logins by binding them from approved runtime sources. Do not invent, scrape, brute-force or persist passwords.

Approved sources:

1. environment variable references (`KINGHOST_FTP_USER`, `KINGHOST_FTP_PASSWORD`, MySQL equivalents, `KINGHOST_DOMAINS`);
2. approved secret-manager references materialized by `runtime-auth`;
3. ephemeral runtime memory supplied by the Tool Router;
4. KingHost panel **cookie/cookie-jar file** consumed in place via `kinghost_control.panel.session.open_cookie_file`.

The model and notebook may see `credential_ref`, `session_ref`, `panel_session_ref`, username, host, port, domain and environment id. They must never see passwords, cookie values, nonces, `user_pass` hashes or `wp-config.php` secrets.

## Hospedagem operating loop

1. Open the panel cookie jar (`panel.session.open_cookie_file`).
2. `domain.list` then `domain.select` for an existing hosting domain.
3. `environment.select` (`local` | `staging` | `production`).
4. Bind already-created FTP and MySQL usernames as opaque refs.
5. `users.list` / `wordpress.users.list` (redacted) — never dump passwords.
6. Inventory plugins (WooCommerce and others) via FTP and/or `mysql.wordpress.inventory`.
7. If the workspace tree is missing, `site.clone` (dry-run first; skip `wp-config.php`).
8. Change the local WordPress/PHP/plugin/theme tree.
9. Production publish follows the FSM below. For the already-altered local tree, run `kinghost-wordpress-publish` / `npm run aeos:kinghost:publish` instead of inventing a second procedure.

## Deterministic production FSM

Every production publish follows this order. Skipping a state is a stop condition.

1. `IDLE`
2. `ENV_SELECTED` — `local` | `staging` | `production` plus selected domain
3. `CREDENTIALS_BOUND` — opaque FTP and optional MySQL/wp-admin refs
4. `PANEL_AUTH` — cookie or Playwright identity check
5. `INVENTORY` — remote scoped tree + WordPress/PHP/MySQL metadata
6. `SNAPSHOT` — hashes/backup/`rollback_ref`
7. `DIFF` — workspace vs remote
8. `DRY_RUN` — FTP tree STOR/SQL list without mutation
9. `BACKUP` — confirm restore path
10. `APPLY` — approved scoped FTP/PHP/SQL (`ftp.tree.upload` or `deploy.workspace_to_production`)
11. `VERIFY` — cookie/Playwright smoke of resulting state
12. `CLOSE` — destroy runtime credential material

`ROLLBACK` is legal from `APPLY` or `VERIFY` on failure.

Advance with `kinghost_control.fsm.advance`. Treat planning tools as plans until APPLY succeeds and VERIFY passes.

## Lenses

Use internal lenses, never subagents:

- `kinghost-environment`: plan limits, domain list/select, PHP version, FTP root;
- `wordpress-architecture`: themes, plugins, WooCommerce, hooks, REST, capabilities;
- `php-runtime`: version, ini, extensions, fatals;
- `mysql-safety`: read-first, EXPLAIN-first, reversible SQL, table-prefix detection;
- `ftp-publish`: scoped clone/upload, no core edits;
- `panel-auth`: cookie/Playwright KingHost panel;
- `production-operations`: backup, smoke, cache, rollback.

## Mutation hierarchy

1. WordPress/plugin/theme settings via authenticated wp-admin/REST when safer;
2. workspace child theme or site plugin (including e-commerce extensions);
3. scoped FTP of `wp-content/themes`, `wp-content/plugins`, `wp-content/mu-plugins` or selected PHP assets;
4. PHP version/ini through the KingHost Configuração PHP (panel cookie/Playwright);
5. MySQL only when no supported WordPress API exists.

Never edit WordPress core for feature work. `wp-config.php`, `wp-admin/` and `wp-includes/` require explicit high-risk approval.

## Cookie and Playwright

Primary panel authentication is an **external runtime cookie/cookie-jar file reference** opened by the control MCP. Playwright/browser may reuse that session to:

- list and choose the KingHost account/domain;
- open FTP/MySQL/PHP/WordPress tools;
- verify production after FTP upload.

Cookie files stay outside the tracked workspace (commonly referenced as the workspace cookier path, never copied in). Contents are never copied into Git, `.aeos` evidence, notebook, prompts or screenshots that would expose secrets.

## Production gates

Before APPLY:

- domain is listed/selected and environment matches the live host;
- credentials are bound as opaque refs;
- Beta Map exists for WordPress sites (`wordpress-expert` one-shot rule);
- scoped diff is bounded to requested files;
- backup/`rollback_ref` exists;
- dry-run evidence exists;
- `approved=true` and `change_id` are present;
- no secret material would be uploaded.

PASS requires verified front-end/wp-admin state, not FTP transfer success alone. WooCommerce live orders, customers, `siteurl`/`home` and payment secrets stay on production unless a separate high-risk database replace is approved.

## Completion

Return `PASS`, `REVIEW`, `BLOCKED` or `ROLLBACK_REQUIRED` with environment id, selected domain, change_id, redacted session refs, verification evidence and residual risk.
