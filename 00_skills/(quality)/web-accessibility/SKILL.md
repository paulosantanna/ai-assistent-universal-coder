---
name: web-accessibility
description: Audit and improve web accessibility following WCAG 2.1 guidelines. Use when asked to "improve accessibility", "a11y audit", "WCAG compliance", "screen reader support", "keyboard navigation", or "make accessible". Do NOT use for SEO (use seo), performance (use core-web-vitals), or comprehensive site audits covering multiple areas (use web-quality-audit).
license: MIT
metadata:
  author: web-quality-skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Accessibility (a11y)

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Audit and improve web accessibility following WCAG 2.1 guidelines.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [WCAG Principles: POUR](references/instructions/02-wcag-principles-pour.md) — when this domain or mode is in scope.
- 3. [Conformance levels](references/instructions/03-conformance-levels.md) — when this domain or mode is in scope.
- 4. [Perceivable](references/instructions/04-perceivable.md) — when this domain or mode is in scope.
- 5. [Operable](references/instructions/05-operable.md) — when this domain or mode is in scope.
- 6. [Understandable](references/instructions/06-understandable.md) — when this domain or mode is in scope.
- 7. [Robust](references/instructions/07-robust.md) — when this domain or mode is in scope.
- 8. [Testing checklist](references/instructions/08-testing-checklist.md) — before claiming completion.
- 9. [Common issues by impact](references/instructions/09-common-issues-by-impact.md) — when this domain or mode is in scope.
- 10. [References](references/instructions/10-references.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
