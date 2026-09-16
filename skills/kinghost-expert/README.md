# kinghost-expert

Super-skill of `codenavi-agent` for complete KingHost Hospedagem operations.

- MCP: `kinghost-control` 1.3
- Super-skill registry: `kinghost-expert` 1.4
- Knowledge: current KingHost Wiki/live panel + official `@kinghost` YouTube learning with mutation corroboration
- Auth: external cookie jar (`panel.session.open_cookie_file`) or governed Playwright/browser
- Domains/DNS/SSL: create/select/manage through documented panel surfaces with snapshot + rollback
- FTP clone: dedicated `kinghost-clone-site-expert` for remote-read-only complete FTP-visible tree acquisition with path reconciliation and integrity evidence
- FTP publish: dedicated `kinghost-site-publish-ftp-expert` for PHP/WordPress manifest-driven upload with backup, approval, rollback and application smoke
- FTP/WebFTP/SSH/Git: clone, scoped publish and provider Git integration
- WordPress/PHP: `wordpress-expert` + hosting runtime configuration
- MySQL: opaque credentials, read-first SQL, controlled migrations/backups/recovery
- Backups: web/FTP, databases and e-mail recovery workflows
- Security: antivirus/quarantine, Smart WAF and SSL verification
- E-mail: mailbox/Webmail/client/DNS/recovery operations
- Performance: hosting resource metrics, Varnish/cache, PHP/runtime, SQL and PageSpeed-oriented tuning
- Publish: FTP tree upload with dry-run, approval, backup, rollback and smoke
- One command: `npm run aeos:kinghost:publish -- --local-dir <tree> --domain <existing-domain>` (`kinghost-wordpress-publish`)
- Credentials: bind already-created logins; never persist or print passwords/cookies/mailbox secrets

Companion skills:

- `kinghost-backup-recovery-expert`
- `kinghost-security-expert`
- `kinghost-domain-dns-ssl-expert`
- `kinghost-email-expert`
- `kinghost-performance-expert`
- `kinghost-database-expert`
- `kinghost-clone-site-expert`
- `kinghost-site-publish-ftp-expert`

Important completeness boundary: an FTP clone can be absolute for the FTP-visible filesystem but it cannot by itself clone MySQL/database state, DNS, e-mail or panel configuration. A complete WordPress application clone combines the filesystem clone with the appropriate governed database snapshot/clone.

Operational contract: `skills/kinghost-expert/HOSTING_OPERATIONS.md`.
