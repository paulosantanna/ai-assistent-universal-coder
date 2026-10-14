---
name: create-adr
description: Creates Architecture Decision Records (ADRs) to document significant architectural choices and their rationale for future team members. Use when the user says "write an ADR", "document this decision", "record why we chose X", "add an architecture decision record", "create an ADR for", or wants to capture the reasoning behind a technical choice so the team understands it later. Do NOT use when the decision hasn't been made yet (use create-rfc instead), for implementation planning (use technical-design-doc-creator), or for general documentation.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ADR Creator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Creates Architecture Decision Records (ADRs) to document significant architectural choices and their rationale for future team members.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [When to Use This Skill](references/instructions/02-when-to-use-this-skill.md) — when this domain or mode is in scope.
- 3. [ADR vs RFC — Critical Distinction](references/instructions/03-adr-vs-rfc-critical-distinction.md) — when this domain or mode is in scope.
- 4. [Language Adaptation](references/instructions/04-language-adaptation.md) — when this domain or mode is in scope.
- 5. [ADR Format Selection](references/instructions/05-adr-format-selection.md) — when this domain or mode is in scope.
- 6. [Interactive Workflow](references/instructions/06-interactive-workflow.md) — at this step of execution.
- 7. [Document Templates](references/instructions/07-document-templates.md) — when this domain or mode is in scope.
- 8. [ADR Quality Checklist](references/instructions/08-adr-quality-checklist.md) — before claiming completion.
- 9. [ADR File Naming Convention](references/instructions/09-adr-file-naming-convention.md) — when this domain or mode is in scope.
- 10. [Common Anti-Patterns to Avoid](references/instructions/10-common-anti-patterns-to-avoid.md) — when choosing an output or matching a use case.
- 11. [Important Notes](references/instructions/11-important-notes.md) — when this domain or mode is in scope.
- 12. [Example Prompts that Trigger This Skill](references/instructions/12-example-prompts-that-trigger-this-skill.md) — when choosing an output or matching a use case.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
