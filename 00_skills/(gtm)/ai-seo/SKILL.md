---
name: ai-seo
description: "Programmatic SEO, competitor pages, AI Overviews/GEO, keyword strategy. Use for SEO or organic traffic. Do NOT use for code review or architecture."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI SEO

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Assimilated from installed `ai-seo` 1.0.0 (Chad Boyda / Felipe Rodrigues). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

Programmatic SEO, competitor pages, AI Overviews/GEO, keyword strategy. Use for SEO or organic traffic. Do NOT use for code review or architecture.

## Mission

Plan and produce AI-assisted SEO systems: BOFU alternative pages, programmatic templates, GEO/AI Overview optimization, and measurement. Strategy and content contracts, not app-code architecture.

## Activation

- User asks for SEO, programmatic pages, competitor alternatives, AI Overviews, or keyword strategy.

## Non-activation

- Technical implementation of the product (`spec-driven`, language experts).
- Web security/compatibility only (`best-practices`).

## Critical rules

1. Confirm stack, goal, domain authority, CMS, and competitor set before recommending spend or scale.
2. Never paste API keys, GSC tokens, or DataForSEO credentials into prompts, files, or notebook.
3. Verify current tool pricing and SERP behavior with dated search; do not treat the 2025 table as live truth.
4. Quality floor for programmatic pages: unique helpful content, not boilerplate swaps.
5. Follow playbooks in `references/ORIGINAL_SKILL.md`.

## Continuity

Do not store customer PII or SEO API secrets in `.notebook/` or `.specs/`.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
