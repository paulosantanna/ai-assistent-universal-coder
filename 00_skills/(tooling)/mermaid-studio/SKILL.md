---
name: mermaid-studio
description: Expert Mermaid diagram creation, validation, and rendering with dual-engine output (SVG/PNG/ASCII). Supports all 20+ diagram types including C4 architecture, AWS architecture-beta with service icons, flowcharts, sequence, ERD, state, class, mindmap, timeline, git graph, sankey, and more. Features code-to-diagram analysis, batch rendering, 15+ themes, and syntax validation. Use when users ask to create diagrams, visualize architecture, render mermaid files, generate ASCII diagrams, document system flows, model databases, draw AWS infrastructure, analyze code structure, or anything involving "mermaid", "diagram", "flowchart", "architecture diagram", "sequence diagram", "ERD", "C4", "ASCII diagram". Do NOT use for non-Mermaid image generation, data plotting with chart libraries, or general documentation writing.
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.1
  owner_agent: codenavi-agent
---

# Mermaid Studio

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Expert Mermaid diagram creation, validation, and rendering with dual-engine output (SVG/PNG/ASCII). Supports all 20+ diagram types including C4 architecture, AWS architecture-beta with service icons, flowcharts, sequence, ERD, state, class, mindmap, timeline, git graph, sankey, and more. Features code-to-diagram analysis, batch rendering, 15+ themes, and syntax validation.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Golden Rules — Elegant Diagrams by Default](references/instructions/02-golden-rules-elegant-diagrams-by-default.md) — before acting on this contract.
- 3. [Modes of Operation](references/instructions/03-modes-of-operation.md) — when this domain or mode is in scope.
- 4. [Step 1: Understand the Request](references/instructions/04-step-1-understand-the-request.md) — at this step of execution.
- 5. [Step 2: Create the Diagram](references/instructions/05-step-2-create-the-diagram.md) — at this step of execution.
- 6. [C4 Diagrams — Mandatory Styling Guide](references/instructions/06-c4-diagrams-mandatory-styling-guide.md) — when this domain or mode is in scope.
- 7. [Step 3: Validate](references/instructions/07-step-3-validate.md) — before claiming completion.
- 8. [Step 4: Render](references/instructions/08-step-4-render.md) — at this step of execution.
- 9. [Step 5: Code-to-Diagram (When Requested)](references/instructions/09-step-5-code-to-diagram-when-requested.md) — at this step of execution.
- 10. [Troubleshooting Quick Reference](references/instructions/10-troubleshooting-quick-reference.md) — when an input, tool or check fails.
- 11. [Output Conventions](references/instructions/11-output-conventions.md) — before acting on this contract.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
