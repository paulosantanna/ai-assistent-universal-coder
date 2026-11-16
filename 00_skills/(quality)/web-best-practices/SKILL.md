---
name: web-best-practices
description: "Apply modern web security, compatibility and code-quality checks. Use for web best-practice reviews. Do NOT use for accessibility, SEO or full audits."
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Best Practices

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Assimilated from installed `best-practices` 1.0 (web-quality-skills / TLC catalog). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

Apply modern web security, compatibility and code-quality checks. Use for web best-practice reviews. Do NOT use for accessibility, SEO or full audits.

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

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
