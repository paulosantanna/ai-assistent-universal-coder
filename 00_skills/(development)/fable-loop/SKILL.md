---
name: fable-loop
description: Orchestrated multi-stage workflow running parallel evidence internal lenses, single committed plan, surgical execution, and adversarial verification. Use when the user requests fable loop or invokes fable-loop. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: fable-loop

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Provide multi-agent orchestrated problem solving inside AEOS v1.1.

## Protocol

1. **Stage 1 - Plan:** Classify, define done, fan out evidence gatherers in parallel, produce plan artifact.
2. **Stage 2 - Execute:** Work checklist in main thread, intent gate before edits, fan out subagents for independent mechanical tasks.
3. **Stage 3 - Verify:** Run verifications, spawn 1-3 attacker subagents to refute work.
4. **Stage 4 - Audit & Report:** Self-audit, format outcome-first report with INTENT, AUTH, TWINS, and PENDING lines.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
