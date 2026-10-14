---
name: create-rfc
description: Creates structured Request for Comments (RFC) documents for proposing and deciding on significant changes. Use when the user says "write an RFC", "create a proposal", "I need to propose a change", "draft an RFC", "document a decision", or needs stakeholder alignment before making a major technical or process decision. Do NOT use for TDDs/implementation docs (use technical-design-doc-creator instead), README files, or general documentation.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# RFC Creator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Creates structured Request for Comments (RFC) documents for proposing and deciding on significant changes.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [When to Use This Skill](references/instructions/02-when-to-use-this-skill.md) — when this domain or mode is in scope.
- 3. [Language Adaptation](references/instructions/03-language-adaptation.md) — when this domain or mode is in scope.
- 4. [RFC vs TDD](references/instructions/04-rfc-vs-tdd.md) — when this domain or mode is in scope.
- 5. [Interactive Workflow](references/instructions/05-interactive-workflow.md) — at this step of execution.
- 6. [Document Structure](references/instructions/06-document-structure.md) — when this domain or mode is in scope.
- 7. [Section Templates](references/instructions/07-section-templates.md) — when this domain or mode is in scope.
- 8. [RFC Quality Checklist](references/instructions/08-rfc-quality-checklist.md) — before claiming completion.
- 9. [Common Anti-Patterns to Avoid](references/instructions/09-common-anti-patterns-to-avoid.md) — when choosing an output or matching a use case.
- 10. [Output Summary Format](references/instructions/10-output-summary-format.md) — before acting on this contract.
- 11. [Important Notes](references/instructions/11-important-notes.md) — when this domain or mode is in scope.
- 12. [Example Prompts that Trigger This Skill](references/instructions/12-example-prompts-that-trigger-this-skill.md) — when choosing an output or matching a use case.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
