---
name: positioning-icp
description: When the user wants to define their ideal customer profile, position an AI product, build messaging architecture, or validate product-market fit. Also use when the user mentions 'ICP,' 'ideal customer profile,' 'positioning,' 'PMF,' 'product-market fit,' 'messaging,' 'buyer persona,' 'enrichment signals,' 'market positioning,' or 'competitive positioning.' This skill covers market positioning, ICP definition, messaging architecture, and PMF validation for AI-native products. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# Positioning, ICP & Messaging Architecture for AI Products

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

When the user wants to define their ideal customer profile, position an AI product, build messaging architecture, or validate product-market fit. Also use when the user mentions 'ICP,' 'ideal customer profile,' 'positioning,' 'PMF,' 'product-market fit,' 'messaging,' 'buyer persona,' 'enrichment signals,' 'market positioning,' or 'competitive positioning.' This skill covers market positioning, ICP definition, messaging architecture, and PMF validation for AI-native products. Do NOT use for technical implementation, code review, or software architecture.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when this domain or mode is in scope.
- 3. [1. Positioning Stack for AI Products](references/instructions/03-1-positioning-stack-for-ai-products.md) — when this domain or mode is in scope.
- 4. [2. Defining ICP with Enrichment Signals](references/instructions/04-2-defining-icp-with-enrichment-signals.md) — when this domain or mode is in scope.
- 5. [3. Competitive Positioning in Fast-Moving AI Markets](references/instructions/05-3-competitive-positioning-in-fast-moving-ai-markets.md) — when this domain or mode is in scope.
- 6. [4. Messaging Architecture](references/instructions/06-4-messaging-architecture.md) — when this domain or mode is in scope.
- 7. [5. The Buyer Shift: Business Leaders as AI Buyers](references/instructions/07-5-the-buyer-shift-business-leaders-as-ai-buyers.md) — when this domain or mode is in scope.
- 8. [6. Perishable PMF: Quarterly Revalidation](references/instructions/08-6-perishable-pmf-quarterly-revalidation.md) — before claiming completion.
- 9. [7. April Dunford's Positioning Framework Applied to AI](references/instructions/09-7-april-dunford-s-positioning-framework-applied-to-ai.md) — when this domain or mode is in scope.
- 10. [8. Implementation Playbook](references/instructions/10-8-implementation-playbook.md) — when this domain or mode is in scope.
- 11. [Examples](references/instructions/11-examples.md) — when choosing an output or matching a use case.
- 12. [Troubleshooting](references/instructions/12-troubleshooting.md) — when an input, tool or check fails.
- 13. [Related Skills](references/instructions/13-related-skills.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
