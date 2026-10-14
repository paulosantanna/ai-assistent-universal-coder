---
name: figma-implement-design
description: Translate Figma nodes into production-ready code with 1:1 visual fidelity using the Figma MCP workflow (design context, screenshots, assets, and project-convention translation). Use when the user provides Figma URLs or node IDs and asks to implement designs or components that must match Figma specs. Requires a working Figma MCP server connection. Do NOT use for general Figma data fetching, variable exploration, or MCP troubleshooting (use figma instead).
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Implement Design

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Translate Figma nodes into production-ready code with 1:1 visual fidelity using the Figma MCP workflow (design context, screenshots, assets, and project-convention translation).

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Overview](references/instructions/02-overview.md) — when this domain or mode is in scope.
- 3. [Prerequisites](references/instructions/03-prerequisites.md) — when this domain or mode is in scope.
- 4. [Required Workflow](references/instructions/04-required-workflow.md) — at this step of execution.
- 5. [Implementation Rules](references/instructions/05-implementation-rules.md) — before acting on this contract.
- 6. [Examples](references/instructions/06-examples.md) — when choosing an output or matching a use case.
- 7. [Best Practices](references/instructions/07-best-practices.md) — when this domain or mode is in scope.
- 8. [Common Issues and Solutions](references/instructions/08-common-issues-and-solutions.md) — when this domain or mode is in scope.
- 9. [Understanding Design Implementation](references/instructions/09-understanding-design-implementation.md) — when this domain or mode is in scope.
- 10. [Additional Resources](references/instructions/10-additional-resources.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
