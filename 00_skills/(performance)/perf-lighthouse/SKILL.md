---
name: perf-lighthouse
description: "Run Lighthouse via CLI or Node, parse reports, set budgets. Use for Lighthouse audits. Do NOT use for CWV fixes (core-web-vitals)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Perf Lighthouse

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Assimilated from installed `perf-lighthouse`. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

Run Lighthouse via CLI or Node, parse reports, set budgets. Use for Lighthouse audits. Do NOT use for CWV fixes (core-web-vitals).

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

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
