---
name: kinghost-expert
description: Super-skill for complete KingHost Hospedagem operations: panel auth, domains/DNS/SSL, absolute FTP-visible site clone, governed FTP/SSH/Git publish, WordPress/PHP/MySQL, backups, email, antivirus/WAF, cache/performance and rollback-safe production changes.
---

# KingHost Expert Super-Skill

## Identity

A super-skill of the single canonical `codenavi-agent`. It creates no new agent identity. Specialization is implemented as internal lenses and companion skills.

## Mission

Operate authorized KingHost Hospedagem accounts from first inventory through production: authenticate the panel with an **external runtime cookie/cookie-jar** reference, list/select domains, create/manage supported hosting resources through documented panel surfaces, clone the complete FTP-visible site tree with integrity reconciliation, inspect and mutate FTP/MySQL safely, operate WordPress/PHP, publish code, manage DNS/SSL/e-mail, request/restore backups, run antivirus/WAF controls, tune cache/performance and verify/rollback changes.

Full hosting operating contract: `skills/kinghost-expert/HOSTING_OPERATIONS.md`.

## Knowledge and media learning

Material KingHost work uses `kinghost_control.knowledge_search` and `aeos/knowledge/kinghost-control.sources.yaml` before claims or mutations.

Authority order:

1. current KingHost official documentation and live authenticated panel;
2. official `@kinghost` YouTube videos as educational evidence;
3. WordPress official documentation for WordPress internals;
4. first-party repository engineering evidence.

The repository media-analysis model is `aura-voice`. When an official transcript or authorized media input is available, apply its provenance rules: preserve technical terminology, retain source/timestamps when available, separate facts from assumptions and never promote uncertain content into executable truth. Video-only operational claims must be corroborated by current KingHost documentation or the live panel before mutation.

Undocumented private KingHost panel APIs are unsupported and fail closed.

## Executable dependencies

- `kinghost-control`: cookie panel session, domains, credentials, FTP, MySQL, clone, production FSM, knowledge.
- governed `browser`/Playwright: panel-only tools such as DNS, SSL, backup request, antivirus, WAF, e-mail, Varnish/performance, Git integration and resource creation.
- `wordpress-expert`: WordPress themes/plugins/blocks/content and WordPress production engineering.
- `kinghost-commerce`: only when SSH/SFTP/Postgres commerce sessions are the safer documented protocol.
- `runtime-auth` / `runtime-http`: extra authenticated runtime sessions without exposing secrets.

### Compatibility contract

Existing integrations remain stable while the hosting surface expands:

- bind **already created** FTP/MySQL/WordPress identities as opaque runtime references; never rediscover their passwords;
- use `kinghost_control.site.clone` for governed site clone planning/execution;
- use `kinghost_control.ftp.tree.upload` for governed FTP publication under mutation gates;
- preserve playbook id `kinghost-wordpress-publish` and command `npm run aeos:kinghost:publish` for the one-command WordPress publish path;
- keep `domain.list` / `domain.select` as the canonical domain-selection contract.

## Companion skills

- `kinghost-backup-recovery-expert`: web/FTP, database and e-mail backup/restore.
- `kinghost-security-expert`: antivirus, quarantine, WAF and SSL security operations.
- `kinghost-domain-dns-ssl-expert`: domains, subdomains, DNS and certificate lifecycle.
- `kinghost-email-expert`: mailbox/Webmail/client/DNS/recovery workflows.
- `kinghost-performance-expert`: hosting/app/database performance, Varnish/cache and PHP runtime.
- `kinghost-database-expert`: MySQL creation/access/migration/query/backup/recovery.
- `kinghost-clone-site-expert`: integrity-reconciled, remote-read-only clone of the entire FTP-visible site tree, with explicit database completeness boundaries.
- `kinghost-site-publish-ftp-expert`: manifest-driven PHP/WordPress FTP publication with backup, approval, rollback and application smoke.

These are skill lenses of `codenavi-agent`, not independent agent identities.

## Credential contract

Obtain already-provisioned logins from approved runtime sources. Do not invent, scrape, brute-force or persist passwords.

Approved sources:

1. environment variable references (`KINGHOST_FTP_USER`, `KINGHOST_FTP_PASSWORD`, MySQL equivalents, `KINGHOST_DOMAINS`);
2. approved secret-manager references materialized by `runtime-auth`;
3. ephemeral runtime memory supplied by the Tool Router;
4. KingHost panel cookie/cookie-jar file consumed in place via `kinghost_control.panel.session.open_cookie_file`.

The model/notebook may see opaque refs, usernames, host, port, domain and environment id when necessary. They must never see passwords, raw cookies, nonces, `user_pass` hashes, mailbox secrets or `wp-config.php` secrets.

## Hospedagem operating loop

1. open panel session;
2. `domain.list` / `domain.select`;
3. select `local|staging|production`;
4. `knowledge_search` for the requested hosting surface;
5. inventory current state and plan capability availability;
6. bind required secrets as opaque refs;
7. snapshot current state and establish rollback;
8. create bounded diff/operation plan and dry-run when supported;
9. obtain required approval;
10. mutate through documented MCP tool or governed panel UI;
11. verify resulting external/application/data state;
12. rollback on verification failure;
13. close sessions and ephemeral credentials.

## Deterministic production FSM

For code/data production publish:

`IDLE -> ENV_SELECTED -> CREDENTIALS_BOUND -> PANEL_AUTH -> INVENTORY -> SNAPSHOT -> DIFF -> DRY_RUN -> BACKUP -> APPLY -> VERIFY -> CLOSE`

`ROLLBACK` is legal after APPLY/VERIFY failure. Advance with `kinghost_control.fsm.advance`.

The existing one-command WordPress path remains:

```bash
npm run aeos:kinghost:publish -- --local-dir <wordpress-tree> --domain <existing-kinghost-domain>
```

## Hosting lenses

Use internal lenses, never subagents:

- `kinghost-environment`: plan/domain/service availability;
- `domain-dns-ssl`: hostname, records, certificates and propagation;
- `ftp-clone`: complete FTP-visible inventory/download/reconciliation with no remote mutation;
- `ftp-publish`: manifest-driven upload with protected paths, rollback and verification;
- `wordpress-architecture`: WordPress/plugins/WooCommerce;
- `php-runtime`: PHP compatibility/configuration/cron;
- `mysql-safety`: read-first SQL, migrations, backups and recovery;
- `email-operations`: mailbox/Webmail/DNS/backup;
- `hosting-security`: antivirus/quarantine/WAF/SSL;
- `hosting-performance`: resource metrics, Varnish/cache, PageSpeed and query/app bottlenecks;
- `production-operations`: backup, smoke, rollback and incident recovery.

## Mutation hierarchy

1. supported application/panel settings;
2. WordPress REST/wp-admin/plugin/theme settings through `wordpress-expert`;
3. versioned workspace code + Git/FTP scoped publish;
4. documented PHP/runtime/panel configuration;
5. database mutation only when no safer application migration/API exists.

Never edit WordPress core for feature work. `wp-config.php`, `wp-admin/` and `wp-includes/` require explicit high-risk approval.

## Service-specific invariants

- FTP clone: remote side is read-only; every FTP-visible path must be reconciled as copied, secret-excluded, inaccessible, unsupported or failed; an FTP-only WordPress copy is not database-complete.
- FTP publish: use an approved manifest; no implicit remote deletion; protected paths fail closed; transfer success alone is not PASS.
- DNS: snapshot all records before write; preserve unrelated records; verify authoritative resolution.
- SSL: confirm hostname/DNS prerequisites; verify certificate and mixed content after activation.
- Backup: restore never begins without current-state snapshot and rollback.
- Antivirus: detections are candidates until analyzed; quarantine is not automatic proof of malware; false positives require safe restoration path.
- WAF: monitor-first and narrow exceptions; verify login/API/checkout/webhooks.
- Varnish/cache: capture DNS when activation may affect it; never cache user-specific/authenticated flows without proof.
- Email: mailbox passwords and message contents remain outside model/evidence; verify MX/current provider requirements.
- MySQL: SELECT/SHOW/DESCRIBE/EXPLAIN default; mutations are bounded, reversible and approved.
- Git/FTP publish: successful transfer/webhook is not PASS until application smoke succeeds.

## Production gates

Before any high-impact production write:

- domain/environment identity confirmed;
- capability exists in current plan/panel;
- authoritative knowledge refreshed;
- credentials remain opaque;
- current-state inventory/snapshot exists;
- rollback path exists;
- bounded diff/operation plan exists;
- approval/change id recorded where required;
- secret material cannot leak into uploaded artifacts/evidence;
- post-change verification is defined.

## Completion

Return `PASS`, `REVIEW`, `BLOCKED` or `ROLLBACK_REQUIRED` with selected environment/domain, redacted refs, operation/change id, verification evidence, source references and residual risk. Never claim success from a panel toast, FTP status, scan completion or database command alone.
