---
name: llm-model-selection-expert
description: Select the best current model/model-family for a concrete workload using live authoritative capability information plus project evals. Use when the user requests llm model selection expert or invokes llm-model-selection-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# LLM Model Selection Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Select the best current model/model-family for a concrete workload using live authoritative capability information plus project evals.

## Procedure
Define workload/safety/latency/cost/context/tooling/privacy constraints → enumerate currently available candidates from official provider/model docs → normalize harness → run representative eval set → compare quality, tool reliability, structured output, latency, throughput and cost → choose primary/fallback → document date/version and retirement trigger.

Never encode 'latest/best model' as permanent knowledge. Model availability and fine-tuning/tool support are freshness-sensitive.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
