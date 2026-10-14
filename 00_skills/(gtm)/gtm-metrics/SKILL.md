---
name: gtm-metrics
description: When the user wants to define GTM metrics, build a metrics dashboard, measure pipeline efficiency, or track AI product performance. Also use when the user mentions 'GTM metrics,' 'revenue latency,' 'pipeline metrics,' 'TTFV,' 'time-to-first-value,' 'data health,' 'attribution,' 'conversion rate,' 'CAC,' 'LTV,' 'NRR,' 'GTM dashboard,' 'magic number,' 'pipeline velocity,' or 'funnel metrics.' This skill covers GTM measurement from metric selection through dashboard design, including AI-specific cost metrics, attribution models, and weekly review cadences. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# GTM Metrics, Dashboards & Measurement for AI Products

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

When the user wants to define GTM metrics, build a metrics dashboard, measure pipeline efficiency, or track AI product performance. Also use when the user mentions 'GTM metrics,' 'revenue latency,' 'pipeline metrics,' 'TTFV,' 'time-to-first-value,' 'data health,' 'attribution,' 'conversion rate,' 'CAC,' 'LTV,' 'NRR,' 'GTM dashboard,' 'magic number,' 'pipeline velocity,' or 'funnel metrics.' This skill covers GTM measurement from metric selection through dashboard design, including AI-specific cost metrics, attribution models, and weekly review cadences. Do NOT use for technical implementation, code review, or software architecture.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when this domain or mode is in scope.
- 3. [1. Core GTM Metrics Dashboard](references/instructions/03-1-core-gtm-metrics-dashboard.md) — when this domain or mode is in scope.
- 4. [2. Funnel Metrics by GTM Motion](references/instructions/04-2-funnel-metrics-by-gtm-motion.md) — when this domain or mode is in scope.
- 5. [3. AI Product-Specific Metrics](references/instructions/05-3-ai-product-specific-metrics.md) — when this domain or mode is in scope.
- 6. [4. Data Health Scoring](references/instructions/06-4-data-health-scoring.md) — when this domain or mode is in scope.
- 7. [5. Attribution Models](references/instructions/07-5-attribution-models.md) — when this domain or mode is in scope.
- 8. [6. Dashboard Architecture](references/instructions/08-6-dashboard-architecture.md) — when this domain or mode is in scope.
- 9. [7. Leading vs. Lagging Indicators](references/instructions/09-7-leading-vs-lagging-indicators.md) — when this domain or mode is in scope.
- 10. [8. Weekly GTM Review Cadence](references/instructions/10-8-weekly-gtm-review-cadence.md) — when this domain or mode is in scope.
- 11. [9. PQL Scoring](references/instructions/11-9-pql-scoring.md) — when this domain or mode is in scope.
- 12. [Examples](references/instructions/12-examples.md) — when choosing an output or matching a use case.
- 13. [Troubleshooting](references/instructions/13-troubleshooting.md) — when an input, tool or check fails.
- 14. [Quick Reference](references/instructions/14-quick-reference.md) — when this domain or mode is in scope.
- 15. [Questions to Ask](references/instructions/15-questions-to-ask.md) — when this domain or mode is in scope.
- 16. [Related Skills](references/instructions/16-related-skills.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
