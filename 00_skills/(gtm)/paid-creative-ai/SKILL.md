---
name: paid-creative-ai
description: When the user wants to create AI-generated ad creative, test performance creative, manage creative fatigue, or optimize paid media with AI tools. Also use when the user mentions 'ad creative,' 'performance creative,' 'creative testing,' 'creative fatigue,' 'Meta ads,' 'Google ads,' 'TikTok ads,' 'AI ads,' 'ad budget,' 'ROAS,' 'Advantage+,' or 'Performance Max.' This skill covers AI-powered paid creative from generation through performance optimization. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# Paid Creative AI

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

When the user wants to create AI-generated ad creative, test performance creative, manage creative fatigue, or optimize paid media with AI tools. Also use when the user mentions 'ad creative,' 'performance creative,' 'creative testing,' 'creative fatigue,' 'Meta ads,' 'Google ads,' 'TikTok ads,' 'AI ads,' 'ad budget,' 'ROAS,' 'Advantage+,' or 'Performance Max.' This skill covers AI-powered paid creative from generation through performance optimization. Do NOT use for technical implementation, code review, or software architecture.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when this domain or mode is in scope.
- 3. [Section 1: Platform AI Creative Systems](references/instructions/03-section-1-platform-ai-creative-systems.md) — when this domain or mode is in scope.
- 4. [Section 2: AI Creative Generation Tools](references/instructions/04-section-2-ai-creative-generation-tools.md) — when this domain or mode is in scope.
- 5. [Section 3: Budget Allocation Framework](references/instructions/05-section-3-budget-allocation-framework.md) — when this domain or mode is in scope.
- 6. [Section 4: Modular Creative Testing Framework](references/instructions/06-section-4-modular-creative-testing-framework.md) — before claiming completion.
- 7. [Section 5: Creative Fatigue Management](references/instructions/07-section-5-creative-fatigue-management.md) — when this domain or mode is in scope.
- 8. [Section 6: Kill Criteria and Scaling Rules](references/instructions/08-section-6-kill-criteria-and-scaling-rules.md) — before acting on this contract.
- 9. [Section 7: Platform Cost Benchmarks (2025-2026)](references/instructions/09-section-7-platform-cost-benchmarks-2025-2026.md) — when this domain or mode is in scope.
- 10. [Section 8: Cross-Platform Creative Strategy](references/instructions/10-section-8-cross-platform-creative-strategy.md) — when this domain or mode is in scope.
- 11. [Section 9: Attribution and Measurement](references/instructions/11-section-9-attribution-and-measurement.md) — when this domain or mode is in scope.
- 12. [Section 10: AI Creative Compliance](references/instructions/12-section-10-ai-creative-compliance.md) — when this domain or mode is in scope.
- 13. [Examples](references/instructions/13-examples.md) — when choosing an output or matching a use case.
- 14. [Troubleshooting](references/instructions/14-troubleshooting.md) — when an input, tool or check fails.
- 15. [Related Skills](references/instructions/15-related-skills.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
