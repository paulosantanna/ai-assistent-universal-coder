# KingHost Hospedagem — Governed Operations

Source registry: `aeos/knowledge/kinghost-control.sources.yaml`  
Executable control plane: `kinghost-control`  
Normative vendor source: KingHost Wiki/live panel  
Educational media source: official `@kinghost` YouTube channel

## Operating principle

Treat the KingHost panel as a documented UI surface, not as an undocumented private API. Use `kinghost-control` for deterministic FTP/MySQL/session/FSM operations and the governed browser/Playwright runtime for panel-only features. Any write follows `inventory -> snapshot -> diff/plan -> dry-run when possible -> backup/rollback -> approval -> apply -> verify`.

Video-derived instructions are learning evidence. Before a mutable action, corroborate them with the current KingHost Wiki or live panel because products and panel layouts change.

## Capability matrix

| Surface | Read/inventory | Mutation path | Mandatory safeguards |
|---|---|---|---|
| Domains/subdomains | panel + `domain.list/select` | browser/Playwright | prior state, DNS impact, verification |
| DNS | `knowledge_search` + panel | browser/Playwright | export/current records, TTL/diff, rollback |
| FTP/WebFTP | `ftp.*`, `ftp.tree.*` | MCP FTP tools | root scope, dry-run, rollback |
| SSH | plan-specific/KingHost tools when available | governed terminal/MCP only when plan exposes it | least privilege, no secret echo |
| Git publish | panel inventory | browser/Playwright/Git integration | branch/directory validation, backup, smoke |
| MySQL | `mysql.*` + panel metadata | MCP MySQL tools | read-first, parameterization, backup, approval |
| phpMyAdmin | panel confirmation | browser/Playwright only when required | no password capture, SQL review |
| WordPress | `wordpress-expert` + inventory | REST/wp-admin/FTP | Beta Map, plugin/theme boundaries, rollback |
| PHP | knowledge + panel inventory | browser/Playwright | compatibility matrix, staging, rollback |
| Cron | panel inventory | browser/Playwright | idempotency, lock/overlap prevention, logs |
| SSL/HTTPS | panel + external TLS verification | browser/Playwright | hostname/DNS preflight, mixed-content smoke |
| E-mail | panel/Webmail inventory | browser/Playwright | secret isolation, MX/DNS verification |
| Backup/restore | panel + MCP snapshot metadata | browser/Playwright + controlled restore | restore point, current-state snapshot, smoke |
| Antivírus | panel | browser/Playwright | pre-scan hashes, quarantine review, smoke |
| WAF | panel | browser/Playwright | monitor-first, scoped exceptions, API/checkout smoke |
| Varnish/cache | panel | browser/Playwright | DNS capture, cookie/session exclusions, purge verification |
| Performance | panel stats + browser metrics | config/app changes through owning skill | baseline before/after, no tuning by guess |

## Backup and recovery

KingHost documents backup for FTP/web, supported databases and e-mail. The documented standard retention flow can expose up to seven days of recoverable content; never assume that retention or product eligibility without checking the live panel.

- Web/FTP backup is differential.
- Database backup is a full dump.
- E-mail backup is differential and depends on mail remaining on the server (for example IMAP or POP retaining a server copy).
- A restore is a production mutation. Capture the current state first so rollback does not destroy newer valid data.
- Database restore must validate schema/table counts, application connectivity and representative business reads after restore.
- WordPress/WooCommerce restore must preserve live orders/customers unless the approved recovery scope explicitly includes them.

## Antivirus and malware response

The KingHost antivirus scans FTP content and may quarantine suspected files automatically. Current documentation states a limited number of panel scans per day and warns about false positives.

1. Inventory/hashes before scan.
2. Run panel scan only on the selected domain.
3. Record report metadata; do not copy secrets or arbitrary customer data into evidence.
4. Review quarantined paths before deletion.
5. Diff quarantined files against repository/vendor originals when possible.
6. Restore false positives only after evidence review.
7. Rotate affected credentials and patch vulnerable code/plugins if compromise is confirmed.
8. Run browser/API smoke after quarantine action.

Large trees should also be scanned in the source repository/local workspace using repository security tooling; panel antivirus is not a substitute for SAST/SCA/secret scanning.

## DNS, SSL and domains

DNS changes require a full record-set snapshot. Preserve A/AAAA/CNAME/MX/TXT and service-specific records that are outside the requested change. Do not reset DNS to defaults unless explicitly requested and a rollback record exists.

Before Let's Encrypt/HTTPS changes, confirm domain/hostname pointing requirements in current KingHost documentation and panel. After activation validate certificate chain/hostname, HTTP->HTTPS behavior and mixed content.

## Performance

Performance optimization is measurement-driven:

- capture page/load/API baseline and hosting resource consumption;
- check PHP version compatibility before upgrades;
- use application/page/object cache only with correct session/cookie exclusions;
- Varnish changes require awareness that DNS may be rewritten by activation in documented scenarios;
- optimize images/assets/build output and database queries before simply increasing plan resources;
- use PageSpeed/Core Web Vitals as external evidence, not as the only measure;
- for WordPress use `wordpress-expert` to inspect plugin/theme/query impact;
- after publish purge only necessary caches and verify authenticated, checkout and webhook flows.

## E-mail operations

Create or modify mailboxes through the panel without exposing mailbox passwords. Verify DNS/MX/SPF/DKIM/DMARC only against current plan documentation and actual records. Webmail/client configuration can be tested with non-secret connection metadata; secrets remain runtime-only.

## Creation workflows

### New domain/site

1. Confirm plan capacity and requested hostname.
2. Create/select domain/subdomain in panel.
3. Verify DNS and SSL readiness.
4. Choose application path: static/PHP, WordPress, or supported app/runtime.
5. Create database only if required.
6. Publish through Git/FTP/WordPress workflow.
7. Enable backup/security/performance controls appropriate to the site.
8. Verify external HTTP, TLS, application and observability state.

### New MySQL database

1. Create database in panel.
2. Configure minimum necessary network/IP policy.
3. Bind credential as opaque runtime reference.
4. Apply migrations through versioned code, not ad-hoc production SQL when avoidable.
5. Verify schema and application connectivity.
6. Establish backup/restore evidence.

### New WordPress

Delegate WordPress engineering to `wordpress-expert`. KingHost panel/installer can provision the installation, but all custom code follows the WordPress Clean Code/AI-assisted protocol and production gates.

## Stop conditions

- target domain/environment is ambiguous;
- requested capability is not present in current plan/panel;
- action would require an undocumented private KingHost endpoint;
- backup/rollback is missing for destructive/high-impact work;
- credential/cookie/password would need to be exposed to the model or repository;
- antivirus quarantine or WAF/cache behavior cannot be verified safely;
- database mutation scope is not bounded;
- the only evidence is an old video/article contradicted by the live panel or current docs.
