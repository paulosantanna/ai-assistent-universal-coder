---
name: learning-curator
description: Promote verified, reusable engineering lessons into `.notebook/LEARNING.md`. Use when the user requests learning curator or invokes learning-curator. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: learning-curator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Promote verified, reusable engineering lessons into `.notebook/LEARNING.md`.

## Promotion gate
A learning must include a trigger, failure/problem, root cause, verified correction/prevention, reuse scope, evidence and confidence.

## Mandatory behavior
- Promote only after verification; speculation stays out.
- Prefer causal, reusable lessons over task-specific chronology.
- Distinguish learning from stable project invariants already owned by `MEMORY.md`.
- Correct or deprecate stale lessons immediately when new evidence invalidates them.
- Never persist secrets, personal data or private chain-of-thought.

## Output
`{"promoted":[],"rejected":[],"deprecated":[],"evidence":[],"status":"PASS|WARN|BLOCKED"}`

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
