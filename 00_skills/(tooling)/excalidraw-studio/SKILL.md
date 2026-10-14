---
name: excalidraw-studio
description: Generate Excalidraw diagrams from natural language descriptions. Outputs .excalidraw JSON files openable in Excalidraw. Use when asked to "create a diagram", "make a flowchart", "visualize a process", "draw a system architecture", "create a mind map", "generate an Excalidraw file", "draw an ER diagram", "create a sequence diagram", or "make a class diagram". Supports flowcharts, relationship diagrams, mind maps, architecture, DFD, swimlane, class, sequence, and ER diagrams. Can use icon libraries (AWS, GCP, etc.) when set up. Do NOT use for code architecture analysis (use the architecture skills), Mermaid diagram rendering (use mermaid-studio), or non-visual documentation (use docs-writer).
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.1
  owner_agent: codenavi-agent
---

# Excalidraw Studio

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Generate Excalidraw diagrams from natural language descriptions. Outputs .excalidraw JSON files openable in Excalidraw.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Workflow](references/instructions/02-workflow.md) — at this step of execution.
- 3. [Templates](references/instructions/03-templates.md) — when this domain or mode is in scope.
- 4. [Icon Libraries](references/instructions/04-icon-libraries.md) — when this domain or mode is in scope.
- 5. [Best Practices](references/instructions/05-best-practices.md) — when this domain or mode is in scope.
- 6. [Validation Checklist](references/instructions/06-validation-checklist.md) — before claiming completion.
- 7. [Troubleshooting](references/instructions/07-troubleshooting.md) — when an input, tool or check fails.
- 8. [Limitations](references/instructions/08-limitations.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
