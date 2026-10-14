---
name: memory-curator
description: Curate durable, evidence-backed project memory in `.notebook/MEMORY.md`. Use when the user requests memory curator or invokes memory-curator. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: memory-curator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Curate durable, evidence-backed project memory in `.notebook/MEMORY.md`.

## Promotion gate
An entry may be promoted only when it is stable enough to help future missions and is supported by project evidence or an explicitly authoritative source.

## Mandatory behavior
- Store validated facts, invariants, accepted decisions and durable source pointers.
- Include rationale for decisions, evidence/source pointer, status and Updated date.
- Reject transient task status, speculative hypotheses, raw logs and duplicated learning.
- Mark superseded/deprecated entries instead of silently preserving false memory.
- Never persist raw credentials, tokens, cookies, private keys, personal data or private chain-of-thought.

## Output
`{"promoted":[],"rejected":[],"superseded":[],"evidence":[],"status":"PASS|WARN|BLOCKED"}`

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
