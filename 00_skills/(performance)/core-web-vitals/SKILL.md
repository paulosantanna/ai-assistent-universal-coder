---
name: core-web-vitals
description: "Fix LCP, INP and CLS to current Google thresholds. Use for Core Web Vitals or layout shifts. Do NOT use for bundles (perf-web-optimization)."
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Core Web Vitals

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Assimilated from installed `core-web-vitals` 1.0 (web-quality-skills / TLC catalog). Original contract: `references/ORIGINAL_SKILL.md`. LCP detail: `references/LCP.md`.

## Identity

Fix LCP, INP and CLS to current Google thresholds. Use for Core Web Vitals or layout shifts. Do NOT use for bundles (perf-web-optimization).

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

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
