---
name: lead-enrichment
description: "Lead enrichment waterfalls, ICP scoring and contact verification (Clay, Apollo). Use for enrichment or lead scoring. Do NOT use for code work."
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

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Lead enrichment waterfalls, ICP scoring and contact verification (Clay, Apollo). Use for enrichment or lead scoring. Do NOT use for code work.

  

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when in scope.
- 3. [Section 1: ICP Scoring Framework](references/instructions/03-section-1-icp-scoring-framework.md) — when in scope.
- 4. [Section 2: Enrichment Waterfall Architecture](references/instructions/04-section-2-enrichment-waterfall-architecture.md) — when in scope.
- 5. [Section 3: Clay Workflow Design](references/instructions/05-section-3-clay-workflow-design.md) — at this step.
- 6. [Section 4: Contact Verification Pipeline](references/instructions/06-section-4-contact-verification-pipeline.md) — before claiming completion.
- 7. [Section 5: Performance Benchmarks](references/instructions/07-section-5-performance-benchmarks.md) — when in scope.
- 8. [Section 6: Compliance](references/instructions/08-section-6-compliance.md) — when in scope.
- 9. [Examples](references/instructions/09-examples.md) — when choosing an output or matching a use case.
- 10. [Troubleshooting](references/instructions/10-troubleshooting.md) — when an input, tool or check fails.
- 11. [Related Skills](references/instructions/11-related-skills.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
