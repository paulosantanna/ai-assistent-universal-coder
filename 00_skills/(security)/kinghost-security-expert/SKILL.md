---
name: kinghost-security-expert
description: "KingHost security: malware scans, quarantine, WAF, SSL. Use for KingHost security. Do NOT use outside authorized scope or to expose secrets."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# KingHost Security Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Super-skill lens of the canonical `codenavi-agent`; no new agent identity.

## Mission

Operate documented KingHost security controls safely: antivirus/malware scan, quarantine analysis, Smart WAF, SSL/HTTPS and hosting security verification.

## Dependencies

- `kinghost-control`
- governed `browser`/Playwright for panel-only features
- repository SAST/SCA/secret/CVE tooling for source-side validation
- `wordpress-expert` for WordPress/plugin remediation
- `00_skills/(cloud)/kinghost-expert/HOSTING_OPERATIONS.md`

## Antivirus workflow

1. Select exact domain/environment.
2. `knowledge_search("antivirus malware quarantine")`.
3. Inventory/hash remote tree or repository source before scan.
4. Run the panel antivirus only through authenticated governed UI.
5. Capture report metadata and quarantined paths, not file secrets/customer content.
6. Treat every detection as `candidate` until verified; false positives are documented by KingHost as possible.
7. Diff suspicious files against Git/vendor originals and inspect persistence vectors.
8. Restore from quarantine only with evidence; delete only with explicit high-risk approval.
9. Patch root cause, rotate compromised credentials where indicated, rescan and smoke test.

Do not exceed panel limits intentionally or automate repeated scans to bypass provider limits. For large trees, run local/repository scanners as the primary deep scan and use the hosting scan as a complementary control.

## WAF workflow

Prefer monitor-first. Observe blocked patterns, then enable/adjust protection. Scope exceptions narrowly by route/rule; never globally disable WAF merely to make an application work. Verify login, REST/API, checkout/payment callbacks and webhooks after changes.

## SSL workflow

Verify DNS/hostname prerequisites, activate/update only through documented panel flow, then validate certificate hostname/chain, HTTP->HTTPS and mixed-content behavior.

## Completion

Return findings as `confirmed|suspected|false_positive|unresolved`, with evidence references and rollback path. A scan finishing successfully is not proof that the application is uncompromised.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
