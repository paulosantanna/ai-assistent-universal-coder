---
name: perf-web-optimization
description: 'Assimilated TLC web performance skill. Measure, then cut bundle size, images, caching, lazy loading and page speed. Triggers: web performance, bundle size, page speed, slow site, lazy loading. Do not use for CWV-only metric work (core-web-vitals), only running Lighthouse (perf-lighthouse), or Astro-only config (perf-astro).'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Perf Web Optimization

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Assimilated from installed `perf-web-optimization`. Original contract: `references/ORIGINAL_SKILL.md`. Topic files: `references/image-optimization.md`, `references/bundle-optimization.md`, `references/core-web-vitals.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

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

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
