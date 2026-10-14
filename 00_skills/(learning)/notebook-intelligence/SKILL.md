---
name: notebook-intelligence
description: Maintain compact, fresh project intelligence in `.notebook/` using progressive disclosure. Use when the user requests notebook intelligence or invokes notebook-intelligence. Do NOT use to promote unverified claims or transient task status into durable memory.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: notebook-intelligence

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Maintain compact, fresh project intelligence in `.notebook/` using progressive disclosure.

## Rules
- Read `INDEX.md` first; load only notes relevant to the current mission.
- One concept per note; prefer pointers over pasted source.
- Categories: flows, patterns, gotchas, domain, graph.
- INDEX entries are one line, <= ~100-char summary, 2–4 discriminative tags.
- Every note has Entry and Updated date.
- Update/archive stale information immediately.
- Never promote guesses or raw logs into project intelligence.

## Debrief
After a material change, determine whether code/architecture/business behavior invalidated any indexed note and repair the knowledge in the same mission.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
