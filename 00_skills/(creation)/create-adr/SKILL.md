---
name: create-adr
description: "Create an ADR recording a made architectural decision and its rationale. Use for 'write an ADR'. Do NOT use for undecided choices (create-rfc)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ADR Creator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Creates Architecture Decision Records (ADRs) to document significant architectural choices and their rationale for future team members.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [When to Use This Skill](references/instructions/02-when-to-use-this-skill.md) — when in scope.
- 3. [ADR vs RFC — Critical Distinction](references/instructions/03-adr-vs-rfc-critical-distinction.md) — when in scope.
- 4. [Language Adaptation](references/instructions/04-language-adaptation.md) — when in scope.
- 5. [ADR Format Selection](references/instructions/05-adr-format-selection.md) — when in scope.
- 6. [Interactive Workflow](references/instructions/06-interactive-workflow.md) — at this step.
- 7. [Document Templates](references/instructions/07-document-templates.md) — when in scope.
- 8. [ADR Quality Checklist](references/instructions/08-adr-quality-checklist.md) — before claiming completion.
- 9. [ADR File Naming Convention](references/instructions/09-adr-file-naming-convention.md) — when in scope.
- 10. [Common Anti-Patterns to Avoid](references/instructions/10-common-anti-patterns-to-avoid.md) — when choosing an output or matching a use case.
- 11. [Important Notes](references/instructions/11-important-notes.md) — when in scope.
- 12. [Example Prompts that Trigger This Skill](references/instructions/12-example-prompts-that-trigger-this-skill.md) — when choosing an output or matching a use case.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
