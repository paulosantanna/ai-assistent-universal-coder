---
name: create-rfc
description: "Create RFCs to propose and decide significant changes with stakeholders. Use for 'write an RFC'. Do NOT use for TDDs (technical-design-doc-creator)."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# RFC Creator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Creates structured Request for Comments (RFC) documents for proposing and deciding on significant changes.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [When to Use This Skill](references/instructions/02-when-to-use-this-skill.md) — when in scope.
- 3. [Language Adaptation](references/instructions/03-language-adaptation.md) — when in scope.
- 4. [RFC vs TDD](references/instructions/04-rfc-vs-tdd.md) — when in scope.
- 5. [Interactive Workflow](references/instructions/05-interactive-workflow.md) — at this step.
- 6. [Document Structure](references/instructions/06-document-structure.md) — when in scope.
- 7. [Section Templates](references/instructions/07-section-templates.md) — when in scope.
- 8. [RFC Quality Checklist](references/instructions/08-rfc-quality-checklist.md) — before claiming completion.
- 9. [Common Anti-Patterns to Avoid](references/instructions/09-common-anti-patterns-to-avoid.md) — when choosing an output or matching a use case.
- 10. [Output Summary Format](references/instructions/10-output-summary-format.md) — before acting.
- 11. [Important Notes](references/instructions/11-important-notes.md) — when in scope.
- 12. [Example Prompts that Trigger This Skill](references/instructions/12-example-prompts-that-trigger-this-skill.md) — when choosing an output or matching a use case.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
