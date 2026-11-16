---
name: ai-pricing
description: "Price AI products: charge metric, tiers, packaging, margins. Use for AI pricing or BYOK. Do NOT use for code or architecture work."
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

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Price AI products: charge metric, tiers, packaging, margins. Use for AI pricing or BYOK. Do NOT use for code or architecture work.

  

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when in scope.
- 3. [The Three Charge Metrics](references/instructions/03-the-three-charge-metrics.md) — when in scope.
- 4. [Three Product Archetypes and Their Pricing](references/instructions/04-three-product-archetypes-and-their-pricing.md) — when in scope.
- 5. [Hybrid Pricing Model Design](references/instructions/05-hybrid-pricing-model-design.md) — when in scope.
- 6. [Examples](references/instructions/06-examples.md) — when choosing an output or matching a use case.
- 7. [Troubleshooting](references/instructions/07-troubleshooting.md) — when an input, tool or check fails.
- 8. [Related Skills](references/instructions/08-related-skills.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
