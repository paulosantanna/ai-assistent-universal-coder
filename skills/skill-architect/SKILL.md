---
name: skill-architect
description: "Assimilated TLC skill architect (1.0.0). Guide Discovery → Architecture → Craft → Validate → Deliver when creating a new skill. Triggers: create a skill, design a skill, turn this into a skill, teach the agent to do X, SKILL.md. Do not use for Cursor work-unit files (cursor-subagent-creator) or TDDs (technical-design-doc-creator)."
---

# Skill Architect

Assimilated from installed `skill-architect` 1.0.0 (Felipe Rodrigues / Tech Lead's Club). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. New skills inherit `AGENTS.md` and cannot create another agent identity.

## Mission

Design a high-quality skill through Discovery and Architecture before writing `SKILL.md`. Prefer progressive disclosure and composability.

## Activation

- User wants to create, design, or automate a repeatable agent workflow as a skill.

## Non-activation

- Improving/evaluating an existing skill when `skill-factory` / skill-creator is the better fit.
- Creating a TDD (`technical-design-doc-creator`).
- Creating a Cursor work unit (`cursor-subagent-creator`).

## Critical rules

1. Do not generate `SKILL.md` until Discovery and Architecture exit criteria pass, unless the user insists; then compress, do not skip.
2. New skills must declare `owner_agent: codenavi-agent` and follow CodENavi lifecycle.
3. Run `scripts/validate_skill.py` against the generated skill before delivery.
4. Read `references/patterns.md`, `references/examples.md`, `references/quality-checklist.md` when those phases need them.
5. Follow `references/ORIGINAL_SKILL.md` for questions, folder layout, and frontmatter hard rules.

## Continuity

Promote only verified skill-design decisions into `.notebook/MEMORY.md`.
