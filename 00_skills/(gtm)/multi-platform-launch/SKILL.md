---
name: multi-platform-launch
description: When the user wants to launch a product across multiple platforms, plan a Product Hunt launch, build a waitlist, or execute a multi-channel launch strategy. Also use when the user mentions 'product launch,' 'Product Hunt,' 'launch strategy,' 'waitlist,' 'beta launch,' 'BetaList,' 'Hacker News,' 'launch day,' 'AppSumo,' 'multi-channel launch.' This skill covers multi-platform launch execution from pre-launch through post-launch optimization. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# Multi-Platform Launch Skill

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

When the user wants to launch a product across multiple platforms, plan a Product Hunt launch, build a waitlist, or execute a multi-channel launch strategy. Also use when the user mentions 'product launch,' 'Product Hunt,' 'launch strategy,' 'waitlist,' 'beta launch,' 'BetaList,' 'Hacker News,' 'launch day,' 'AppSumo,' 'multi-channel launch.' This skill covers multi-platform launch execution from pre-launch through post-launch optimization. Do NOT use for technical implementation, code review, or software architecture.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when this domain or mode is in scope.
- 3. [Platform Landscape (2025-2026)](references/instructions/03-platform-landscape-2025-2026.md) — when this domain or mode is in scope.
- 4. [Launch Sequence Framework](references/instructions/04-launch-sequence-framework.md) — at this step of execution.
- 5. [Product Hunt Deep Dive](references/instructions/05-product-hunt-deep-dive.md) — when this domain or mode is in scope.
- 6. [Hacker News (Show HN) Deep Dive](references/instructions/06-hacker-news-show-hn-deep-dive.md) — when this domain or mode is in scope.
- 7. [Waitlist Building Playbook](references/instructions/07-waitlist-building-playbook.md) — when this domain or mode is in scope.
- 8. [Examples](references/instructions/08-examples.md) — when choosing an output or matching a use case.
- 9. [Troubleshooting](references/instructions/09-troubleshooting.md) — when an input, tool or check fails.
- 10. [Related Skills](references/instructions/10-related-skills.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
