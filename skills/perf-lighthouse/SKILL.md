---
name: perf-lighthouse
description: "Assimilated TLC Lighthouse audit skill. Run Lighthouse via CLI or Node, parse reports, set performance budgets. Triggers: lighthouse, run lighthouse, lighthouse score, performance audit, performance budget. Do not use to implement CWV or generic speed fixes (core-web-vitals, perf-web-optimization) or Astro-only config (perf-astro)."
---

# Perf Lighthouse

Assimilated from installed `perf-lighthouse`. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

Measure with Lighthouse, interpret the report, and optionally wire budgets/CI. Do not invent scores. Prefer the project's existing Lighthouse/Chrome setup over a global install.

## Activation

- User asks to run Lighthouse, read a score, set a performance budget, or add an audit to CI.

## Non-activation

- Implementing LCP/INP/CLS fixes (`core-web-vitals`).
- Broad page-speed remediations (`perf-web-optimization`).
- Astro-only integration work (`perf-astro`).

## Critical rules

1. Use repo-local `npx lighthouse` or an existing script before installing globally.
2. Report category, form-factor, URL and whether the run was lab. Quote numbers from the report file.
3. Do not add CI workflow jobs without DevOps gates and explicit approval.
4. Follow CLI flags, budget.json and parse steps in `references/ORIGINAL_SKILL.md` after checking current Lighthouse docs.
5. Do not persist third-party tokens. Commits only with explicit authorization.

## Continuity

Promote only verified durable budgets (paths, thresholds) into `.notebook/MEMORY.md`.
