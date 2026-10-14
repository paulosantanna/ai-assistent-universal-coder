---
name: fable
description: Standard problem-solving loop (classify ask, define done, gather evidence, decide, act surgically, verify by observation, report outcome-first). Use for non-trivial multi-step tasks, diagnosis, planning, or auditing work. Use when the user requests fable or invokes fable. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: fable

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Provide enterprise-grade Fable Method problem-solving loop capability inside AEOS v1.1.

Refer to `.agents/skills/fable/SKILL.md` and `.agents/skills/fable/references/` for full method specifications.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
