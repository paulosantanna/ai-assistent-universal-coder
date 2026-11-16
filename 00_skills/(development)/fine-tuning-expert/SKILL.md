---
name: fine-tuning-expert
description: "Decide if fine-tuning is justified; build a governed training pipeline. Use for fine-tuning decisions. Do NOT use for unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Fine-Tuning Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Decide whether fine-tuning is justified and implement a governed training pipeline when supported by the selected model/provider.

## Techniques
SFT, preference optimization where supported, LoRA/QLoRA/DoRA PEFT for open-weight models, curriculum/data balancing, checkpointing, quantization compatibility and catastrophic-forgetting controls.

## Gate before training
Baseline eval → failure taxonomy → prove prompt/RAG/tooling alone is insufficient → curated train/validation/test split → dedup/contamination checks → safety/privacy/license review → training budget → rollback/base-model comparison.

Provider/model fine-tuning support changes over time and MUST be verified from current official documentation before implementation. Never invent an endpoint or train a model merely because fine-tuning sounds more advanced.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
