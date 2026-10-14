---
name: expansion-retention
description: When the user wants to reduce churn, build expansion revenue, automate customer success, or optimize net revenue retention. Also use when the user mentions 'churn,' 'retention,' 'expansion revenue,' 'upsell,' 'NRR,' 'net revenue retention,' 'customer success,' 'land and expand,' 'closed-lost,' or 'renewal.' This skill covers expansion and retention systems from usage triggers through automated customer success. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# Expansion & Retention Systems

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

When the user wants to reduce churn, build expansion revenue, automate customer success, or optimize net revenue retention. Also use when the user mentions 'churn,' 'retention,' 'expansion revenue,' 'upsell,' 'NRR,' 'net revenue retention,' 'customer success,' 'land and expand,' 'closed-lost,' or 'renewal.' This skill covers expansion and retention systems from usage triggers through automated customer success. Do NOT use for technical implementation, code review, or software architecture.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when this domain or mode is in scope.
- 3. [1. Net Revenue Retention: The Growth Multiplier](references/instructions/03-1-net-revenue-retention-the-growth-multiplier.md) — when this domain or mode is in scope.
- 4. [2. Land-and-Expand: Consumption-Based Upsell Triggers](references/instructions/04-2-land-and-expand-consumption-based-upsell-triggers.md) — when this domain or mode is in scope.
- 5. [3. Customer Health Scoring](references/instructions/05-3-customer-health-scoring.md) — when this domain or mode is in scope.
- 6. [4. Product-Qualified Accounts (PQAs)](references/instructions/06-4-product-qualified-accounts-pqas.md) — when this domain or mode is in scope.
- 7. [5. Automated Onboarding Sequences](references/instructions/07-5-automated-onboarding-sequences.md) — at this step of execution.
- 8. [6. Closed-Lost Re-engagement](references/instructions/08-6-closed-lost-re-engagement.md) — when this domain or mode is in scope.
- 9. [7. Usage-Based Billing Optimization](references/instructions/09-7-usage-based-billing-optimization.md) — when this domain or mode is in scope.
- 10. [8. Customer Advocacy and Renewal Management](references/instructions/10-8-customer-advocacy-and-renewal-management.md) — when this domain or mode is in scope.
- 11. [9. Churn Prevention Playbooks](references/instructions/11-9-churn-prevention-playbooks.md) — when this domain or mode is in scope.
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
