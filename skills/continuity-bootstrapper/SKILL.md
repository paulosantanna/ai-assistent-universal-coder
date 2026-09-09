# Skill: continuity-bootstrapper
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
- Create only missing artifacts from `templates/codenavi-continuity/`.
- Never overwrite populated continuity files merely to normalize formatting.
- Reconcile existing entries against project evidence before marking them current.
- Add/index the quartet in `.notebook/INDEX.md`.
- Fail closed on secret exposure, path escape, unsupported claims or conflicting canonical governance.

## Output
`{"created":[],"existing":[],"reconciled":[],"blocked":[],"evidence":[],"status":"PASS|WARN|BLOCKED"}`
