---
name: lora-qlora-dora-expert
description: "Implement LoRA, QLoRA or DoRA fine-tuning with reproducible experiments. Use for PEFT work. Do NOT use for unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# LoRA / QLoRA / DoRA Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Implement parameter-efficient fine-tuning for supported open-weight models with reproducible experiments.

## Workflow
Select base model/license → compatibility matrix → dataset/eval baseline → choose LoRA vs QLoRA vs DoRA based on memory/quality constraints → define target modules/rank/alpha/dropout/quantization → train with checkpoint/evidence → compare against baseline → merge/export only when justified → regression/safety eval.

Track seed, dataset hash, base revision, tokenizer, hyperparameters, hardware, precision, adapter hash and eval results.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
