---
name: kinghost-domain-dns-ssl-expert
description: "Governed KingHost domain, DNS and SSL changes with snapshot and rollback. Use for KingHost DNS or SSL. Do NOT use for unapproved production changes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# KingHost Domain / DNS / SSL Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Super-skill lens of the canonical `codenavi-agent`; no new agent identity.

## Mission

Create/select authorized domains and subdomains, manage documented DNS records and SSL/HTTPS safely through the KingHost panel without undocumented private APIs.

## Dependencies

- `kinghost-control`
- governed `browser`/Playwright
- `00_skills/(cloud)/kinghost-expert/HOSTING_OPERATIONS.md`

## DNS contract

Before mutation export/capture the complete visible record set and target hostname. Preserve unrelated A/AAAA/CNAME/MX/TXT and provider-specific records. Record intended diff and rollback values.

Supported learned concepts from current official material include A, CNAME, MX and TXT. Never infer that a record type/action exists if it is not present in the current panel.

## Domain/subdomain creation

1. verify plan capacity and selected account;
2. create the domain/subdomain through documented panel UI;
3. map the intended directory/redirect/application;
4. verify DNS state and external resolution;
5. attach SSL only after hostname prerequisites pass;
6. verify HTTP/TLS and application behavior.

## SSL

For Let's Encrypt or other documented certificates, validate current DNS/hosting prerequisites first. After activation verify hostname, certificate chain, redirects and mixed content. SSL success in the panel alone is insufficient.

## Gates

- explicit hostname/environment;
- pre-change DNS snapshot;
- rollback record set;
- approval for production DNS/SSL mutation;
- no reset-to-default unless explicitly requested;
- post-change resolution/TLS verification.

Return `PASS|PROPAGATING|REVIEW|BLOCKED|ROLLBACK_REQUIRED`.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
