---
name: subagent-creator
description: "Assimilated TLC agent-agnostic work-unit designer. Use for isolated-context specialists, verifiers, debuggers or orchestrators that are not Cursor-only. Triggers: create subagent, specialized assistant, create verifier. Do not spawn or register another AEOS agent identity. For Cursor-only files, use cursor-subagent-creator."
---

# Subagent Creator

Assimilated from installed `subagent-creator`. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity. Source "subagent" files are remapped to **lenses / sequential work units**.

## Mission

Design focused, isolated-context work units for complex multi-step workflows that are not Cursor-specific. Prefer a skill when the job is single-purpose and does not need isolation.

## Activation

- User asks for a generic specialist, verifier, debugger, orchestrator, or isolated multi-step work unit.

## Non-activation

- Cursor-only work-unit files (`cursor-subagent-creator`).
- Simple one-off tasks (use an existing skill).
- Requests that would register a second AEOS agent id.

## Critical rules

1. Never create, register, or spawn another agent identity. `owner_agent` stays `codenavi-agent`.
2. Do not add entries to `aeos/registries/agents.registry.yaml` or write AEOS agent constitutions.
3. Emit a **lens work unit** under `skills/<host-skill>/lenses/<name>.md`. The body must state it is a lens of `codenavi-agent`.
4. One responsibility per work unit. Keep prompts concise. Define output format.
5. Follow structure, checklists and examples in `references/ORIGINAL_SKILL.md`, with every "subagent" / "new agent" word remapped as above.

## Output

Report location, purpose, how to invoke as a lens of `codenavi-agent`, and that no new agent was registered.
