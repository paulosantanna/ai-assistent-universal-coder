---
name: video-outreach
description: When the user wants to build video-first cold outreach, create personalized video at scale, implement async selling, or use AI demo generation for prospecting. Also use when the user mentions 'video outreach,' 'personalized video,' 'video prospecting,' 'Tavus,' 'Sendspark,' 'HeyGen,' 'video email,' 'async selling,' 'video demo,' or 'made this for you.' This skill covers video-first outreach systems from personalization through conversion optimization. Do NOT use for technical implementation, code review, or software architecture.
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# Video-First Cold Outreach

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

When the user wants to build video-first cold outreach, create personalized video at scale, implement async selling, or use AI demo generation for prospecting. Also use when the user mentions 'video outreach,' 'personalized video,' 'video prospecting,' 'Tavus,' 'Sendspark,' 'HeyGen,' 'video email,' 'async selling,' 'video demo,' or 'made this for you.' This skill covers video-first outreach systems from personalization through conversion optimization. Do NOT use for technical implementation, code review, or software architecture.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when this domain or mode is in scope.
- 3. [The "Made This For You" Framework](references/instructions/03-the-made-this-for-you-framework.md) — when this domain or mode is in scope.
- 4. [Personalized Video at Scale: The Tool Landscape](references/instructions/04-personalized-video-at-scale-the-tool-landscape.md) — when this domain or mode is in scope.
- 5. [Interactive Demo Tools for Async Selling](references/instructions/05-interactive-demo-tools-for-async-selling.md) — when this domain or mode is in scope.
- 6. [Video in the Sales Sequence](references/instructions/06-video-in-the-sales-sequence.md) — at this step of execution.
- 7. [Async Selling: Replacing Meetings with Video](references/instructions/07-async-selling-replacing-meetings-with-video.md) — when this domain or mode is in scope.
- 8. [Conversion Benchmarks](references/instructions/08-conversion-benchmarks.md) — when this domain or mode is in scope.
- 9. [The Video Prospecting Tech Stack](references/instructions/09-the-video-prospecting-tech-stack.md) — when this domain or mode is in scope.
- 10. [Recording Best Practices](references/instructions/10-recording-best-practices.md) — when this domain or mode is in scope.
- 11. [Measuring Performance](references/instructions/11-measuring-performance.md) — when this domain or mode is in scope.
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
