---
name: web-quality-audit
description: "Assimilated TLC/web-quality multi-area audit. Review performance, accessibility, SEO and best practices in one pass. Triggers: audit my site, review web quality, check page quality, optimize my website across areas. Do not use for a single-area job (core-web-vitals, ai-seo, best-practices, perf-lighthouse)."
---

# Web Quality Audit

Assimilated from installed `web-quality-audit` 1.0 (web-quality-skills / TLC catalog). Original contract: `references/ORIGINAL_SKILL.md`. Optional HTML scan: `scripts/analyze.sh`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity. Depth work is delegated to existing skills as lenses, not new agents.

## Mission

Run a multi-category quality review (Performance, Accessibility, SEO, Best Practices). Categorize findings by severity with file:line evidence and a prioritized fix order.

## Orchestration

Load the matching specialist only when that category has findings that need depth:

- Performance / CWV — `core-web-vitals`, `perf-web-optimization`, `perf-lighthouse`
- Astro-only config — `perf-astro`
- SEO — `ai-seo`
- Headers / modern web hygiene — `best-practices`

Original sibling links (`../seo`, `../accessibility`) are not in this workspace unless those skills are copied later.

## Activation

- User asks for a site/page quality audit across more than one area.

## Non-activation

- Only LCP/INP/CLS (`core-web-vitals`).
- Only Lighthouse CLI (`perf-lighthouse`).
- Only SEO (`ai-seo`) or only headers (`best-practices`).

## Critical rules

1. Measure or read the live HTML/repo. Do not invent Lighthouse scores.
2. Output the report shape in `references/ORIGINAL_SKILL.md` (Critical / High / Medium / Low + summary + recommended order).
3. Optional: run `scripts/analyze.sh <file-or-dir>` on HTML as a heuristic, then confirm in the files.
4. Verify current CWV thresholds and official a11y/SEO guidance; the original tables may be stale.
5. Do not persist secrets. Commits only with explicit authorization.

## Continuity

Promote only verified durable quality gates into `.notebook/MEMORY.md`.
