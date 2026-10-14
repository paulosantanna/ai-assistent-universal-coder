---
name: automation-orchestrator
description: Design deterministic, idempotent multi-step engineering automations using existing AEOS skills/tools. Use when the user requests automation orchestrator or invokes automation-orchestrator. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Automation Orchestrator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Design deterministic, idempotent multi-step engineering automations using existing AEOS skills/tools.

## Rules
Explicit inputs/outputs, retries/timeouts, idempotency key, state transitions, stop conditions, evidence and compensation/rollback. Never bypass capability/approval gates. Prefer composition over creating another tool.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
