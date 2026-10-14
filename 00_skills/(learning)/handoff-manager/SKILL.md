---
name: handoff-manager
description: Maintain a concise, executable `.notebook/HANDOFF.md` representing only the last verified operational state. Use when the user requests handoff manager or invokes handoff-manager. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: handoff-manager

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Maintain a concise, executable `.notebook/HANDOFF.md` representing only the last verified operational state.

## Mandatory behavior
- Refresh on pause, session boundary, operator/tool context change, or incomplete debrief.
- Record objective, last verified state, touched paths, decisions, blockers/risks, evidence, exact next actions and remaining validation.
- Distinguish verified facts from pending/uncertain items.
- Link to `PROGRESS.md` instead of copying detailed logs.
- Never persist secrets, personal data or private chain-of-thought.
- Replace stale state rather than append endless historical diaries.

## Output
`{"objective":"","verified_state":[],"working_set":[],"decisions":[],"blockers":[],"evidence":[],"next_actions":[],"validation_remaining":[],"status":"PASS|WARN|BLOCKED"}`

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
