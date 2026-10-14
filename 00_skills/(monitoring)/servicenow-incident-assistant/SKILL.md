---
name: servicenow-incident-assistant
description: Convert incident evidence into ServiceNow-ready triage, updates, RCA and closure material. Use when the user requests servicenow incident assistant or invokes servicenow-incident-assistant. Do NOT use to restart, scale or mutate live systems without an authorized operations task.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ServiceNow Incident Assistant

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Convert incident evidence into ServiceNow-ready triage, updates, RCA and closure material.

## Rules
Do not invent incident numbers, assignment groups, SLAs or states. Redact secrets/PII. External read/write requires an authorized ServiceNow connector and AEOS policy. Preserve timeline, impact, evidence, mitigation, root cause and verification.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
