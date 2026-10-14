---
name: lora-qlora-dora-expert
description: Implement parameter-efficient fine-tuning for supported open-weight models with reproducible experiments. Use when the user requests lora qlora dora expert or invokes lora-qlora-dora-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# LoRA / QLoRA / DoRA Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Implement parameter-efficient fine-tuning for supported open-weight models with reproducible experiments.

## Workflow
Select base model/license → compatibility matrix → dataset/eval baseline → choose LoRA vs QLoRA vs DoRA based on memory/quality constraints → define target modules/rank/alpha/dropout/quantization → train with checkpoint/evidence → compare against baseline → merge/export only when justified → regression/safety eval.

Track seed, dataset hash, base revision, tokenizer, hyperparameters, hardware, precision, adapter hash and eval results.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
