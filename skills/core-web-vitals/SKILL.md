---
name: core-web-vitals
description: "Assimilated TLC/web-quality Core Web Vitals skill. Fix LCP, INP and CLS against current Google thresholds. Triggers: improve Core Web Vitals, fix LCP, reduce CLS, optimize INP, page experience, layout shifts. Do not use for generic bundle/caching work (perf-web-optimization), only running Lighthouse (perf-lighthouse), or Astro-only config (perf-astro)."
---

# Core Web Vitals

Assimilated from installed `core-web-vitals` 1.0 (web-quality-skills / TLC catalog). Original contract: `references/ORIGINAL_SKILL.md`. LCP detail: `references/LCP.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

Diagnose and remediate the three ranking-relevant vitals (LCP, INP, CLS) using field or lab evidence from this run. Verify current Google thresholds before citing numbers.

## Activation

- User asks to fix LCP, INP, CLS, layout shifts, or Core Web Vitals / page experience.

## Non-activation

- Broad bundle/cache/image program (`perf-web-optimization`).
- Only run/parse Lighthouse (`perf-lighthouse`).
- Astro integration-only work (`perf-astro`).

## Critical rules

1. Measure first. Do not invent scores or field percentiles.
2. Prefer the 75th-percentile definition Google uses; say whether the number is lab or field.
3. Surgical fixes. Load `references/LCP.md` when LCP is the failing metric.
4. Follow `references/ORIGINAL_SKILL.md` for metric tables and patterns after the live page is known.
5. Do not persist analytics secrets. Commits only with explicit authorization.

## Continuity

Promote only verified durable vital budgets or strategies into `.notebook/MEMORY.md`.
