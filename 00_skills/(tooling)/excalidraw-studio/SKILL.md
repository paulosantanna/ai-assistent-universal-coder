---
name: excalidraw-studio
description: "Generate .excalidraw diagrams from text: flowcharts, architecture, ER, sequence. Use for 'create a diagram'. Do NOT use for Mermaid (mermaid-studio)."
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.1
  owner_agent: codenavi-agent
---

# Excalidraw Studio

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Generate Excalidraw diagrams from natural language descriptions. Outputs .excalidraw JSON files openable in Excalidraw.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Workflow](references/instructions/02-workflow.md) — at this step.
- 3. [Templates](references/instructions/03-templates.md) — when in scope.
- 4. [Icon Libraries](references/instructions/04-icon-libraries.md) — when in scope.
- 5. [Best Practices](references/instructions/05-best-practices.md) — when in scope.
- 6. [Validation Checklist](references/instructions/06-validation-checklist.md) — before claiming completion.
- 7. [Troubleshooting](references/instructions/07-troubleshooting.md) — when an input, tool or check fails.
- 8. [Limitations](references/instructions/08-limitations.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
