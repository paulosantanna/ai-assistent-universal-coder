---
name: continuity-bootstrapper
description: Bootstrap and validate the CodENavi continuity quartet for a workspace without inventing project state. Use when the user requests continuity bootstrapper or invokes continuity-bootstrapper. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: continuity-bootstrapper

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Bootstrap and validate the CodENavi continuity quartet for a workspace without inventing project state.

## Required artifacts
- `.notebook/HANDOFF.md`
- `.notebook/MEMORY.md`
- `.notebook/PROGRESS.md`
- `.notebook/LEARNING.md`

## Mandatory behavior
- Read `AGENT.md`, `.notebook/INDEX.md` and `references/CODENAVI_CONTINUITY_STANDARD.md`.
- Create only missing artifacts from [canonical templates](../chromatic-mega-brain/templates/continuity/INDEX.md).
- Never overwrite populated continuity files merely to normalize formatting.
- Reconcile existing entries against project evidence before marking them current.
- Add/index the quartet in `.notebook/INDEX.md`.
- Fail closed on secret exposure, path escape, unsupported claims or conflicting canonical governance.

## Output
`{"created":[],"existing":[],"reconciled":[],"blocked":[],"evidence":[],"status":"PASS|WARN|BLOCKED"}`

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
