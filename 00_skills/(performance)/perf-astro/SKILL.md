---
name: perf-astro
description: "Optimize Astro sites for Lighthouse: critical CSS, fonts, LCP. Use for Astro performance. Do NOT use for non-Astro sites or Lighthouse-only audits."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Perf Astro

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Assimilated from installed `perf-astro`. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

Optimize Astro sites for Lighthouse: critical CSS, fonts, LCP. Use for Astro performance. Do NOT use for non-Astro sites or Lighthouse-only audits.

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

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
