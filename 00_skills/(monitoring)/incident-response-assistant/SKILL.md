---
name: incident-response-assistant
description: Support human-led incident triage, RCA and recovery without replacing production authority. Use when the user requests incident response assistant or invokes incident-response-assistant. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Incident Response Assistant

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Support human-led incident triage, RCA and recovery without replacing production authority.

## Flow
Timeline → symptoms → affected capability → evidence → hypotheses ranked by falsifiability → blast radius → safe diagnostics → mitigation options → verification → root cause/contributors → corrective/preventive actions → runbook/notebook update.

Never hide uncertainty. Destructive remediation requires approval and rollback.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
