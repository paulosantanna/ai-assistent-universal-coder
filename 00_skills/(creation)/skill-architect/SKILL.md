---
name: "skill-architect"
description: "Design, build, evaluate, score and improve reusable skills through discovery, architecture and minimal evidence-based edits. Use for create a skill, review my skill, rate or score my skill, improve SKILL.md. Do NOT use to identify whether finished work deserves a skill (learning-opportunities), create agent identities, or write a technical design document."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.1"
  owner_agent: "codenavi-agent"
---

# skill-architect

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Workflow

1. Extract the outcome and constraints from the user request/history first. Ask only about material gaps; do not restart a completed discovery.
2. For a new skill, define 2–3 use cases with triggers, inputs, steps, tools and observable outputs. Identify document creation, workflow automation or MCP enhancement and freeze success criteria.
3. Choose a primary pattern from [patterns](references/patterns.md). Plan the folder, concrete what/when/not-when description, and three disclosure levels before writing instructions.
4. For ANY existing-skill evaluation or improvement, follow [existing-skill review](references/existing-skill-review.md): structural baseline, 0–100 grade, diagnosis, smallest scoped edit, validator and new grade. A review request authorizes the review; an update request authorizes the described local update.
5. Write kebab-case name matching the folder. Keep description on one physical YAML line, below 1024 characters, without angle brackets or block scalars. Preserve license/author, record version, and retain owner_agent: codenavi-agent.
6. Keep SKILL.md <=100 physical lines including frontmatter. References hold long procedures; scripts hold deterministic checks; assets/templates exist only when used. Do not hard-wrap prose. Link supporting modules with when-to-read conditions; references over 300 lines need a contents list.
7. Include concrete examples and realistic errors; use [examples](references/examples.md). Keep source attribution and existing working resources. Do not create additional identities or register agent profiles.
8. Run `python -X utf8 "00_skills/(creation)/skill-architect/scripts/validate_skill.py" "PATH" --format json --json-out "REPORT.json"`, use [quality checklist](references/quality-checklist.md), and record 3–5 positive/negative trigger assessments. Manual routing assessment is not measured trigger accuracy.
9. Verify helper behavior when applicable, package under 00_skills, synchronize native discovery/catalog and present before/after, actual checks and limitations. Complete authorized local work before any required final approval.

## Inputs, output and stop

Input: requested skill outcome or inspected existing package, source/license, tools and scope. Output: valid package, grade evidence, scoped changes and verification.
Missing source, permission, helper or required evidence blocks the dependent step. A grade does not authorize deployment, posting, dependency installation or another agent.
Source: photos IMG_2705–IMG_2715, photographed version 1.1.1; retained TLC source remains an immutable older snapshot.

## Retained resources

- Read [retained lenses](references/lenses) only for its matching mode; this entry and root governance take precedence.
- Read [retained ORIGINAL_SKILL](references/ORIGINAL_SKILL.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained package-notes](references/package-notes.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained provenance](references/provenance.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained tlc](references/tlc) only for its matching mode; this entry and root governance take precedence.
- Read [retained usage-and-verification](references/usage-and-verification.md) only for its matching mode; this entry and root governance take precedence.
