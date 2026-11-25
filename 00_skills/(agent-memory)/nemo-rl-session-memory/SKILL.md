---
name: nemo-rl-session-memory
description: "Checkpoint long coding sessions for resume. Use for session memory, handoff, or a checkpoint. Do NOT use for training."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Session Memory

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-rl-session-memory`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Keep a factual resume note for a long coding session without replacing the workspace continuity quartet.

## Workflow

1. If the repo is this CodENavi workspace, update `.notebook/` instead of creating `session/`.
2. If the user asked for session memory or the repo already has `session/`, reuse the latest directory.
3. Write state, timeline, files, and handoff from verified git and command output.
4. Checkpoint before long jobs and after meaningful edits.
5. On resume, re-check git status before trusting the note.

## Inputs, outputs, and stop

Inputs: the repo, the user goal, and whether session/ was requested
Outputs: updated continuity files with no secrets
Stop when a required tool, permission, or evidence check fails. Do not store credentials or treat the note as the only source of truth. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
