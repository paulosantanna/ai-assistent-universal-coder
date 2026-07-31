---
name: fable-loop
description: Orchestrated multi-stage workflow running parallel evidence subagents, single committed plan, surgical execution, and adversarial verification.
---

# Enterprise Skill: fable-loop

## Mission

Provide multi-agent orchestrated problem solving inside AEOS v1.1.

## Protocol

1. **Stage 1 - Plan:** Classify, define done, fan out evidence gatherers in parallel, produce plan artifact.
2. **Stage 2 - Execute:** Work checklist in main thread, intent gate before edits, fan out subagents for independent mechanical tasks.
3. **Stage 3 - Verify:** Run verifications, spawn 1-3 attacker subagents to refute work.
4. **Stage 4 - Audit & Report:** Self-audit, format outcome-first report with INTENT, AUTH, TWINS, and PENDING lines.
