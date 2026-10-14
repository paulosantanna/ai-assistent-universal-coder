---
name: core-web-vitals
description: 'Assimilated TLC/web-quality Core Web Vitals skill. Fix LCP, INP and CLS against current Google thresholds. Triggers: improve Core Web Vitals, fix LCP, reduce CLS, optimize INP, page experience, layout shifts. Do not use for generic bundle/caching work (perf-web-optimization), only running Lighthouse (perf-lighthouse), or Astro-only config (perf-astro).'
license: MIT
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Core Web Vitals

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
