---
name: create-technical-design-doc
description: "Create architecture-level technical design docs via discovery. Use for 'write a design doc' or 'criar um TDD'. Do NOT use for README or API docs."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Technical Design Doc Creator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Assimilated from installed `technical-design-doc-creator`. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

Create architecture-level technical design docs via discovery. Use for 'write a design doc' or 'criar um TDD'. Do NOT use for README or API docs.

## Mission

Write a TDD that records architectural decisions and contracts, not implementation code. Match the user's language. Size sections to project scale.

## Activation

- User asks for a TDD, design doc, RFC, tech spec, or architecture document before implementation.

## Non-activation

- README, API reference, or general documentation (`docs-writer`).
- Feature execution (`spec-driven` / `spec-driven-lean`).

## Critical rules

1. Mandatory sections: header, context, problem, scope, technical solution, risks, implementation plan.
2. Security is mandatory for payments/auth/PII. Monitoring and rollback are mandatory for production.
3. Document decisions that survive a framework change. No CLI recipes or framework-specific code as the design.
4. Do not invent missing facts. Ask only for forks that change the outcome; otherwise state the assumption.
5. Follow templates and checklists in `references/ORIGINAL_SKILL.md`.

## Continuity

A TDD does not replace AEOS `specs` preflight when implementation will mutate the repo.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
