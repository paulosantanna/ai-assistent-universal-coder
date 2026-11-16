---
name: automation-orchestrator
description: "Design idempotent multi-step automations from existing skills. Use for automation orchestration. Do NOT use for unapproved remote writes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Automation Orchestrator

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Design deterministic, idempotent multi-step engineering automations using existing AEOS skills/tools.

## Rules
Explicit inputs/outputs, retries/timeouts, idempotency key, state transitions, stop conditions, evidence and compensation/rollback. Never bypass capability/approval gates. Prefer composition over creating another tool.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
