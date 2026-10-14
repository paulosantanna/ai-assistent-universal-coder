---
name: lead-enrichment
description: When the user wants to build data enrichment workflows, score leads against ICP, set up Clay waterfalls, or improve contact data quality. Also use when the user mentions 'enrichment,' 'data enrichment,' 'Clay,' 'waterfall enrichment,' 'ICP scoring,' 'lead scoring,' 'intent data,' 'contact verification,' 'Apollo,' 'ZoomInfo,' or 'data quality.' This skill covers lead enrichment waterfalls, ICP scoring frameworks, and contact verification systems. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# Lead Enrichment Skill

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

When the user wants to build data enrichment workflows, score leads against ICP, set up Clay waterfalls, or improve contact data quality. Also use when the user mentions 'enrichment,' 'data enrichment,' 'Clay,' 'waterfall enrichment,' 'ICP scoring,' 'lead scoring,' 'intent data,' 'contact verification,' 'Apollo,' 'ZoomInfo,' or 'data quality.' This skill covers lead enrichment waterfalls, ICP scoring frameworks, and contact verification systems. Do NOT use for technical implementation, code review, or software architecture.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when this domain or mode is in scope.
- 3. [Section 1: ICP Scoring Framework](references/instructions/03-section-1-icp-scoring-framework.md) — when this domain or mode is in scope.
- 4. [Section 2: Enrichment Waterfall Architecture](references/instructions/04-section-2-enrichment-waterfall-architecture.md) — when this domain or mode is in scope.
- 5. [Section 3: Clay Workflow Design](references/instructions/05-section-3-clay-workflow-design.md) — at this step of execution.
- 6. [Section 4: Contact Verification Pipeline](references/instructions/06-section-4-contact-verification-pipeline.md) — before claiming completion.
- 7. [Section 5: Performance Benchmarks](references/instructions/07-section-5-performance-benchmarks.md) — when this domain or mode is in scope.
- 8. [Section 6: Compliance](references/instructions/08-section-6-compliance.md) — when this domain or mode is in scope.
- 9. [Examples](references/instructions/09-examples.md) — when choosing an output or matching a use case.
- 10. [Troubleshooting](references/instructions/10-troubleshooting.md) — when an input, tool or check fails.
- 11. [Related Skills](references/instructions/11-related-skills.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
