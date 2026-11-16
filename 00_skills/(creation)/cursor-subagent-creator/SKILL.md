---
name: cursor-subagent-creator
description: "Design Cursor work units: isolated workflows, verifiers, auditors. Use for isolated work units. Do NOT use for one-off skills or agent identities."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Cursor Subagent Creator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
