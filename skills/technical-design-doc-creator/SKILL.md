---
name: technical-design-doc-creator
description: "Assimilated TLC TDD writer. Create architecture-level Technical Design Documents through discovery. Triggers: write a design doc, create a TDD, technical spec, architecture document, RFC, design proposal, criar um TDD. Do not use for README, API docs, or general docs (docs-writer)."
---

# Technical Design Doc Creator

Assimilated from installed `technical-design-doc-creator`. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

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
