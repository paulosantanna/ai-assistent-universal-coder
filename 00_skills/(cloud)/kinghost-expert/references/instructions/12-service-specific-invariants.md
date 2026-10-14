<!-- Package: 00_skills/(cloud)/kinghost-expert; relative command/resource examples resolve from that package or workspace root. -->

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
