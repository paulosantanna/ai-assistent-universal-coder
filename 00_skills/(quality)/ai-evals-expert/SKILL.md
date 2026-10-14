---
name: ai-evals-expert
description: Turn AI quality claims into reproducible evaluation evidence. Use when the user requests ai evals expert or invokes ai-evals-expert. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI Evals Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Turn AI quality claims into reproducible evaluation evidence.

## Framework
SPECIFY → MEASURE → IMPROVE.

Define task claim, golden set, failure taxonomy, slices/edge cases, harness, model/reasoning/tool configuration, budgets and scoring. Use deterministic graders where possible; LLM graders require calibration and human audit. Test contamination, reward hacking, broken tasks, refusals and harness artifacts. Maintain regression gates for quality, safety, latency and cost.

Never report a single aggregate score without describing what it measures and the tested system configuration.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
