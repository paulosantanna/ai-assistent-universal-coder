---
name: whatsapp-simulator
description: Generate synthetic WhatsApp-style conversation fixtures for testing conversational systems, support flows and automation. Use when the user requests whatsapp simulator or invokes whatsapp-simulator. Do NOT use for unrelated tools or unapproved remote writes.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# WhatsApp Conversation Simulator

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Generate synthetic WhatsApp-style conversation fixtures for testing conversational systems, support flows and automation.

## Safety/data rules
Synthetic by default; never impersonate a real person for deception; never inject real credentials/PII. Clearly mark generated fixtures. Cover normal, ambiguous, typo, multilingual, adversarial and escalation cases. Produce expected intent/state/response assertions for evals.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
