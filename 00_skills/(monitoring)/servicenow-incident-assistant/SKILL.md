---
name: servicenow-incident-assistant
description: "Turn incident evidence into ServiceNow triage, updates and RCA. Use for ServiceNow incident work. Do NOT use to mutate live systems unless authorized."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# ServiceNow Incident Assistant

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Convert incident evidence into ServiceNow-ready triage, updates, RCA and closure material.

## Rules
Do not invent incident numbers, assignment groups, SLAs or states. Redact secrets/PII. External read/write requires an authorized ServiceNow connector and AEOS policy. Preserve timeline, impact, evidence, mitigation, root cause and verification.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
