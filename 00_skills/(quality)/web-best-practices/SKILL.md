---
name: web-best-practices
description: 'Assimilated TLC/web-quality best-practices skill. Apply modern web security, compatibility, and code-quality checks. Triggers: apply best practices, security audit, modernize code, code quality review, check for vulnerabilities. Do not use as the primary skill for accessibility, SEO (ai-seo), or a full multi-area audit.'
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Best Practices

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Assimilated from installed `best-practices` 1.0 (web-quality-skills / TLC catalog). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

Audit and remediate web security, browser compatibility, deprecated APIs, and code-quality issues using current official guidance, not training memory.

## Activation

- User asks to apply best practices, run a security/quality review, or modernize frontend code.

## Non-activation

- Dedicated SEO (`ai-seo`).
- Accessibility-only work.
- Full multi-area site audit (`web-quality-audit`).

## Critical rules

1. Verify current header, CSP, and API guidance before calling anything "best".
2. Do not weaken tests or delete failing checks to pass.
3. Surgical fixes only. Do not rewrite unrelated files.
4. Follow checklists and examples in `references/ORIGINAL_SKILL.md`.
5. Secrets stay runtime-only.

## Continuity

Record only verified, durable security decisions in `.notebook/MEMORY.md`.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
