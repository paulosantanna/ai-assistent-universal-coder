---
name: best-practices
description: "Assimilated TLC/web-quality best-practices skill. Apply modern web security, compatibility, and code-quality checks. Triggers: apply best practices, security audit, modernize code, code quality review, check for vulnerabilities. Do not use as the primary skill for accessibility, SEO (ai-seo), or a full multi-area audit."
---

# Best Practices

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
