---
name: gtm-engineering
description: "Build GTM automation: workflow architecture, AI agents, n8n/Make/Zapier. Use for GTM engineering. Do NOT use for code review or architecture."
license: CC-BY-4.0
metadata:
  author: Chad Boyda / agent-gtm-skills
  version: 1.0.0
  original_author: Chad Boyda / agent-gtm-skills
  modified_by: Felipe Rodrigues - github.com/felipfr
  source: https://github.com/chadboyda/agent-gtm-skills
  owner_agent: codenavi-agent
---

# GTM Engineering: Automation, Architecture & Agent Orchestration

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

 Also use when the user mentions 'GTM engineering,' 'GTM automation,' 'n8n,' 'Make,' 'Zapier,' 'workflow automation,' 'Clay API,' 'instruction stacks,' 'AI agents for GTM,' or 'revenue automation.' This skill covers technical GTM infrastructure from workflow design through agent orchestration. 

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Before Starting](references/instructions/02-before-starting.md) — when in scope.
- 3. [1. The GTM Engineer Role](references/instructions/03-1-the-gtm-engineer-role.md) — when in scope.
- 4. [2. Architecture Over Tools](references/instructions/04-2-architecture-over-tools.md) — when in scope.
- 5. [3. Automation Platform Comparison](references/instructions/05-3-automation-platform-comparison.md) — when in scope.
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
