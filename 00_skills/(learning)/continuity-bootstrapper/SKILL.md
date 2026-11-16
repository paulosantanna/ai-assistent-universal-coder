---
name: continuity-bootstrapper
description: "Bootstrap and validate the CodENavi quartet without inventing project state. Use for continuity setup. Do NOT use to promote unverified claims."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: continuity-bootstrapper

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Bootstrap and validate the CodENavi continuity quartet for a workspace without inventing project state.

## Required artifacts
- `.notebook/HANDOFF.md`
- `.notebook/MEMORY.md`
- `.notebook/PROGRESS.md`
- `.notebook/LEARNING.md`

## Mandatory behavior
- Read `AGENTS.md`, `.notebook/INDEX.md` and `references/CODENAVI_CONTINUITY_STANDARD.md`.
- Create only missing artifacts from [canonical templates](../chromatic-mega-brain/templates/continuity/INDEX.md).
- Never overwrite populated continuity files merely to normalize formatting.
- Reconcile existing entries against project evidence before marking them current.
- Add/index the quartet in `.notebook/INDEX.md`.
- Fail closed on secret exposure, path escape, unsupported claims or conflicting canonical governance.

## Output
`{"created":[],"existing":[],"reconciled":[],"blocked":[],"evidence":[],"status":"PASS|WARN|BLOCKED"}`

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
