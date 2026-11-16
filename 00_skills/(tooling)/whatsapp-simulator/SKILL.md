---
name: whatsapp-simulator
description: "Generate synthetic WhatsApp-style conversation fixtures for testing. Use for chat fixtures. Do NOT use for unapproved remote writes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# WhatsApp Conversation Simulator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Generate synthetic WhatsApp-style conversation fixtures for testing conversational systems, support flows and automation.

## Safety/data rules
Synthetic by default; never impersonate a real person for deception; never inject real credentials/PII. Clearly mark generated fixtures. Cover normal, ambiguous, typo, multilingual, adversarial and escalation cases. Produce expected intent/state/response assertions for evals.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
