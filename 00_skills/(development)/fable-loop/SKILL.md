---
name: fable-loop
description: "Multi-stage workflow: evidence lenses, one plan, surgical execution, verification. Use for complex multi-stage work. Do NOT use for trivial tasks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: fable-loop

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Provide multi-agent orchestrated problem solving inside AEOS v1.1.

## Protocol

1. **Stage 1 - Plan:** Classify, define done, fan out evidence gatherers in parallel, produce plan artifact.
2. **Stage 2 - Execute:** Work checklist in main thread, intent gate before edits, fan out subagents for independent mechanical tasks.
3. **Stage 3 - Verify:** Run verifications, spawn 1-3 attacker subagents to refute work.
4. **Stage 4 - Audit & Report:** Self-audit, format outcome-first report with INTENT, AUTH, TWINS, and PENDING lines.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
