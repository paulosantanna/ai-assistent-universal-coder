---
name: ai-pricing
description: When the user wants to price an AI product, choose a charge metric, design pricing tiers, or optimize margins. Also use when the user mentions 'AI pricing,' 'usage-based pricing,' 'consumption pricing,' 'outcome pricing,' 'BYOK,' 'bring your own key,' 'per-seat pricing,' 'pricing tiers,' 'AI margins,' 'cost per token,' or 'pricing model.' This skill covers pricing strategy, packaging, and margin management for AI-native products. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# AI Pricing Skill

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

When the user wants to price an AI product, choose a charge metric, design pricing tiers, or optimize margins. Also use when the user mentions 'AI pricing,' 'usage-based pricing,' 'consumption pricing,' 'outcome pricing,' 'BYOK,' 'bring your own key,' 'per-seat pricing,' 'pricing tiers,' 'AI margins,' 'cost per token,' or 'pricing model.' This skill covers pricing strategy, packaging, and margin management for AI-native products. Do NOT use for technical implementation, code review, or software architecture.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when this domain or mode is in scope.
- 3. [The Three Charge Metrics](references/instructions/03-the-three-charge-metrics.md) — when this domain or mode is in scope.
- 4. [Three Product Archetypes and Their Pricing](references/instructions/04-three-product-archetypes-and-their-pricing.md) — when this domain or mode is in scope.
- 5. [Hybrid Pricing Model Design](references/instructions/05-hybrid-pricing-model-design.md) — when this domain or mode is in scope.
- 6. [Examples](references/instructions/06-examples.md) — when choosing an output or matching a use case.
- 7. [Troubleshooting](references/instructions/07-troubleshooting.md) — when an input, tool or check fails.
- 8. [Related Skills](references/instructions/08-related-skills.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
