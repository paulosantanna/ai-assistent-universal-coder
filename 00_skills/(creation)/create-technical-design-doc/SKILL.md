---
name: create-technical-design-doc
description: 'Assimilated TLC TDD writer. Create architecture-level Technical Design Documents through discovery. Triggers: write a design doc, create a TDD, technical spec, architecture document, RFC, design proposal, criar um TDD. Do not use for README, API docs, or general docs (docs-writer).'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Technical Design Doc Creator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
