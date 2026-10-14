---
name: progress-tracker
description: Keep `.notebook/PROGRESS.md` as the live, evidence-backed source of truth for the current mission. Use when the user requests progress tracker or invokes progress-tracker. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: progress-tracker

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Keep `.notebook/PROGRESS.md` as the live, evidence-backed source of truth for the current mission.

## State model
- `[ ]` pending
- `[~]` active
- `[x]` completed and verified
- `[!]` blocked

## Mandatory behavior
- Define mission, success criteria, current CodENavi phase and verification gates.
- Update at meaningful step/batch boundaries.
- Move an item to `[x]` only when its acceptance gate is satisfied.
- Record factual outcomes and evidence pointers, including material failed attempts/root-cause clues.
- Keep open decisions/blockers explicit.
- Do not copy durable memory or generalized learning into the progress log.
- Never persist secrets or private chain-of-thought.

## Output
`{"phase":"","pending":[],"active":[],"completed":[],"blocked":[],"verification":[],"evidence":[],"status":"PASS|WARN|BLOCKED"}`

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
