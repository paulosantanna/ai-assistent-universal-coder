---
name: perf-web-optimization
description: "Measure, then cut bundle size, images, caching and page speed. Use for web performance work. Do NOT use for CWV-only work (core-web-vitals)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Perf Web Optimization

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Assimilated from installed `perf-web-optimization`. Original contract: `references/ORIGINAL_SKILL.md`. Topic files: `references/image-optimization.md`, `references/bundle-optimization.md`, `references/core-web-vitals.md`.

## Identity

Measure, then cut bundle size, images, caching and page speed. Use for web performance work. Do NOT use for CWV-only work (core-web-vitals).

## Mission

Systematic page-speed work: Measure → Identify → Prioritize → Implement → Verify. Use project-native tooling and current official guidance. Load the matching reference file only for the bottleneck in scope.

## Activation

- User says the site is slow, wants a smaller bundle, faster TTI, lazy loading, or general Lighthouse-oriented remediations.

## Non-activation

- Only LCP/INP/CLS diagnosis (`core-web-vitals`).
- Only run/parse Lighthouse (`perf-lighthouse`).
- Astro-only integrations (`perf-astro`).

## Critical rules

1. Measure first. Do not invent timings or scores.
2. Check lockfile before adding image/bundle tooling.
3. Surgical changes. Follow `references/ORIGINAL_SKILL.md` after the live stack is known.
4. Hand CWV-threshold claims to current Google docs, not training memory.
5. Commits only with explicit authorization. Do not persist CDN/analytics secrets.

## Continuity

Promote only verified durable perf strategies into `.notebook/MEMORY.md`.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
