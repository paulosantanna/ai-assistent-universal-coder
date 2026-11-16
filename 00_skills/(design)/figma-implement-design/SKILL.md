---
name: figma-implement-design
description: "Translate Figma nodes into production code with 1:1 fidelity via Figma MCP. Use for Figma URLs to implement. Do NOT use for data fetching (figma)."
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Implement Design

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Translate Figma nodes into production-ready code with 1:1 visual fidelity using the Figma MCP workflow (design context, screenshots, assets, and project-convention translation).

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Overview](references/instructions/02-overview.md) — when in scope.
- 3. [Prerequisites](references/instructions/03-prerequisites.md) — when in scope.
- 4. [Required Workflow](references/instructions/04-required-workflow.md) — at this step.
- 5. [Implementation Rules](references/instructions/05-implementation-rules.md) — before acting.
- 6. [Examples](references/instructions/06-examples.md) — when choosing an output or matching a use case.
- 7. [Best Practices](references/instructions/07-best-practices.md) — when in scope.
- 8. [Common Issues and Solutions](references/instructions/08-common-issues-and-solutions.md) — when in scope.
- 9. [Understanding Design Implementation](references/instructions/09-understanding-design-implementation.md) — when in scope.
- 10. [Additional Resources](references/instructions/10-additional-resources.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
