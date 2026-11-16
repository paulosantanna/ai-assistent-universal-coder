---
name: mermaid-studio
description: "Create, validate and render Mermaid diagrams (SVG, PNG, ASCII). Use for diagrams or mermaid files. Do NOT use for chart plotting or image generation."
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.1
  owner_agent: codenavi-agent
---

# Mermaid Studio

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Expert Mermaid diagram creation, validation, and rendering with dual-engine output (SVG/PNG/ASCII). Supports all 20+ diagram types including C4 architecture, AWS architecture-beta with service icons, flowcharts, sequence, ERD, state, class, mindmap, timeline, git graph, sankey, and more. Features code-to-diagram analysis, batch rendering, 15+ themes, and syntax validation.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Golden Rules — Elegant Diagrams by Default](references/instructions/02-golden-rules-elegant-diagrams-by-default.md) — before acting.
- 3. [Modes of Operation](references/instructions/03-modes-of-operation.md) — when in scope.
- 4. [Step 1: Understand the Request](references/instructions/04-step-1-understand-the-request.md) — at this step.
- 5. [Step 2: Create the Diagram](references/instructions/05-step-2-create-the-diagram.md) — at this step.
- 6. [C4 Diagrams — Mandatory Styling Guide](references/instructions/06-c4-diagrams-mandatory-styling-guide.md) — when in scope.
- 7. [Step 3: Validate](references/instructions/07-step-3-validate.md) — before claiming completion.
- 8. [Step 4: Render](references/instructions/08-step-4-render.md) — at this step.
- 9. [Step 5: Code-to-Diagram (When Requested)](references/instructions/09-step-5-code-to-diagram-when-requested.md) — at this step.
- 10. [Troubleshooting Quick Reference](references/instructions/10-troubleshooting-quick-reference.md) — when an input, tool or check fails.
- 11. [Output Conventions](references/instructions/11-output-conventions.md) — before acting.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
