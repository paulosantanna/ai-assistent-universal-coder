---
name: kinghost-email-expert
description: Governed KingHost email operations for mailbox creation, DNS/MX alignment, Webmail/client setup and recovery without exposing secrets.
---

# KingHost Email Expert

Super-skill lens of the canonical `codenavi-agent`; no new agent identity.

## Mission

Create and maintain authorized KingHost e-mail services, align DNS/MX, verify Webmail/client connectivity and request/recover backups while keeping mailbox credentials runtime-only.

## Dependencies

- `kinghost-control`
- governed `browser`/Playwright for panel/Webmail operations
- `kinghost-domain-dns-ssl-expert` for DNS/SSL changes
- `kinghost-backup-recovery-expert` for recovery

## Workflow

1. select exact domain;
2. inspect current mail/DNS configuration;
3. create/modify mailbox through panel with a strong secret supplied outside model context;
4. validate Webmail and, when requested, client metadata for Outlook/Thunderbird/mobile;
5. verify MX and other current provider-required DNS records;
6. for recovery, confirm whether server-retained content is eligible under current IMAP/POP behavior and panel availability;
7. close sessions and redact mailbox PII from evidence where not necessary.

## Security

- Never print/store mailbox passwords, auth cookies or message bodies.
- Do not weaken SMTP/IMAP transport security to make a client connect.
- DNS records are changed only from current official guidance/live panel, never from stale remembered defaults.
- Backup restoration is a production mutation and follows the backup skill gates.

Completion requires functional login/connectivity or an explicit `BLOCKED` reason, not merely successful account creation in the panel.
