---
name: perf-astro
description: "Assimilated TLC Astro performance skill. Optimize Astro sites for Lighthouse: critical CSS, compression, fonts, LCP. Triggers: Astro performance, Astro Lighthouse, astro-critters, optimize Astro. Do not use for non-Astro sites or as the only skill to run a Lighthouse audit."
---

# Perf Astro

Assimilated from installed `perf-astro`. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

Apply Astro-specific performance patterns: critical CSS inlining, build compression, font-display/preload, LCP image preload, deferred third-party scripts. Verify current Astro and integration APIs against the project and official docs before changing `astro.config`.

## Activation

- The repo is an Astro site (or the user is adding Astro) and they ask to improve performance or Lighthouse scores.

## Non-activation

- Non-Astro apps (`best-practices`, `core-web-vitals`, `perf-web-optimization`).
- Only run/report Lighthouse with no Astro config work (`perf-lighthouse`).

## Critical rules

1. Confirm `astro.config.*`, Astro version and existing integrations before adding packages. Do not add `astro-critters` or `@playform/compress` silently if the project already has an equivalent.
2. Check current official docs for those integrations; the original playbook may be stale.
3. Surgical changes only. Do not rewrite unrelated layouts.
4. Do not persist analytics IDs or secrets in the repo or notebook.
5. Follow layout, checklist and measure commands in `references/ORIGINAL_SKILL.md` after the live config is known.
6. Commits only with explicit user authorization.

## Continuity

Promote only verified durable Astro perf decisions (chosen integrations, LCP strategy) into `.notebook/MEMORY.md`.
