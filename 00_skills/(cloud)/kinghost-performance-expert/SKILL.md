---
name: kinghost-performance-expert
description: "Measured KingHost performance: resources, cache, PHP runtime, PageSpeed. Use for KingHost performance. Do NOT use for unapproved prod changes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# KingHost Performance Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Super-skill lens of the canonical `codenavi-agent`; no new agent identity.

## Mission

Improve KingHost-hosted site/application performance from measured bottlenecks, using hosting controls and application changes without guessing or masking root causes with plan upgrades.

## Dependencies

- `kinghost-control`
- governed `browser`/Playwright for panel metrics/Varnish/PHP controls
- `wordpress-expert` for WordPress/plugin/theme optimization
- `kinghost-database-expert` for query/index work
- `00_skills/(cloud)/kinghost-expert/HOSTING_OPERATIONS.md`

## Baseline

Collect before/after evidence: response latency, representative page/API timing, hosting CPU/memory/resource consumption when available, cache state, PHP version, database query evidence and external PageSpeed/Core Web Vitals where relevant.

## Optimization order

1. eliminate application errors/retry storms;
2. update supported PHP only after compatibility verification;
3. reduce expensive WordPress/plugin/theme/database work;
4. optimize SQL and indexes from EXPLAIN evidence;
5. optimize images/assets/build output and compression;
6. configure cache/Varnish with correct session/cookie/query exclusions;
7. purge only necessary cache after publish;
8. consider resource/plan scaling after software bottlenecks are understood.

## Varnish safeguards

KingHost documentation notes that Varnish activation can affect DNS in documented hosting scenarios. Capture custom DNS before activation. Never cache authenticated/admin/cart/checkout or other user-specific responses without explicit proof the configuration is safe.

## Completion

Report baseline, applied change, post-change measurement, regressions and rollback. `PASS` requires measurable improvement or a documented stability/security benefit without material regression.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
