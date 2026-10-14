---
name: kinghost-performance-expert
description: Measurement-driven KingHost performance skill for resource consumption, Varnish/cache, PHP runtime, PageSpeed and application/database optimization. Use when the user requests kinghost performance expert or invokes kinghost-performance-expert. Do NOT use for unrelated application features or unapproved production changes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# KingHost Performance Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
