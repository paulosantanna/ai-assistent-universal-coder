---
name: cursor-subagent-creator
description: "Assimilated TLC Cursor work-unit designer. Use when the user asks for a Cursor specialist, isolated-context workflow, verifier, debugger, or auditor. Triggers: cursor subagent, cursor agent, isolated work unit. Do not spawn or register another AEOS agent identity. Do not use for a simple one-off skill."
---

# Cursor Subagent Creator

Assimilated from installed `cursor-subagent-creator`. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity. Source "subagent" files are remapped to **lenses / sequential work units**.

## Mission

Design focused, isolated-context work units for complex multi-step Cursor workflows. Prefer a skill when the job is single-purpose and does not need isolation.

## Activation

- User asks to create a Cursor specialist, verifier, debugger, auditor, or isolated multi-step work unit.

## Non-activation

- Simple one-off tasks (use an existing skill).
- Generic (non-Cursor) work units (`subagent-creator`).
- Requests that would register a second AEOS agent id.

## Critical rules

1. Never create, register, or spawn another agent identity. `owner_agent` stays `codenavi-agent`.
2. Do not write `.cursor/agents/*.md` or `~/.cursor/agents/*.md` as AEOS agent constitutions.
3. Emit a **lens work unit** under `skills/<host-skill>/lenses/<name>.md` or, if the user explicitly wants a Cursor Task file, a file whose body states it is a lens of `codenavi-agent` and not a new agent.
4. One responsibility per work unit. Keep prompts concise. Define output format.
5. Follow structure, checklists, and examples in `references/ORIGINAL_SKILL.md`, with every "subagent" word remapped as above.

## Output

Report location, purpose, how to invoke as a lens of `codenavi-agent`, and that no new agent was registered.
