---
name: skill-factory
description: Create, refactor, package and validate a reusable workspace skill with precise routing, entrypoint of at most 100 lines and local modules. Use when the user says criar skill, melhorar skills, refatorar SKILL.md or adicionar capacidade reutilizável. Do NOT use for one-off code fixes, human competency lists or new agent identities.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 2.0.0
  owner_agent: codenavi-agent
---

# Skill Factory

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Workflow

1. Read the actual user outcome, existing package, callers, `.notebook/INDEX.md` and relevant continuity state. Define concrete triggers, non-triggers, inputs, outputs and observable completion.
2. Use skill-architect for discovery and architecture. Prefer a short self-contained contract; choose modules only when substantial modes/resources need progressive disclosure.
3. Create or update `00_skills/(category)/kebab-case-name/`. Frontmatter order: name, description, license, metadata.author/version; preserve supported invocation/dependency fields.
4. Keep every physical line of SKILL.md within the 100-line cap. Put procedures/examples/schemas in local references, deterministic helpers in scripts, deliverable templates in templates/assets. Link each module with its load condition.
5. Preserve real operational invariants, actual user choices, runtime secret providers and permissions. Roles are internal lenses, never separate agents; no speculative files, fictional scripts or broad activation.
6. Run skill-architect `scripts/validate_skill.py` on the package, then `python "00_skills/(creation)/skill-factory/scripts/validate-workspace.py"` for workspace coverage and links. Run changed helpers and the smallest relevant functional behavior checks.
7. Record source/license/version provenance, hashes and explicit tool limitations. Update the catalog/discovery entries and durable continuity facts only after verification.

## Inputs and outputs

Inputs: reusable outcome, target workspace/package, constraints, inspected source and required tool interfaces.
Outputs: canonical package, linked modules actually used, valid discovery metadata, provenance and executable validation evidence.

## Stop and completion

Missing required source, tool, permission or failed gate blocks the dependent operation. Authorization for local skill creation does not authorize deployment, external publication or paid work. Do not request approval again for actions already authorized by the session.

Complete only when the structural checks and applicable helper/behavior checks pass. Report remaining external dependencies explicitly. Read [retained design details](references/instructions/INDEX.md) only for an applicable advanced mode; this entry supersedes legacy persona, README/scaffold and unavailable-validator requirements.

Source/freshness: [provenance](references/provenance.md).

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
