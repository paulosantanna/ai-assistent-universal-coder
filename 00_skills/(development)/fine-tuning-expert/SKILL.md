---
name: fine-tuning-expert
description: Decide whether fine-tuning is justified and implement a governed training pipeline when supported by the selected model/provider. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Fine-Tuning Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Decide whether fine-tuning is justified and implement a governed training pipeline when supported by the selected model/provider.

## Techniques
SFT, preference optimization where supported, LoRA/QLoRA/DoRA PEFT for open-weight models, curriculum/data balancing, checkpointing, quantization compatibility and catastrophic-forgetting controls.

## Gate before training
Baseline eval → failure taxonomy → prove prompt/RAG/tooling alone is insufficient → curated train/validation/test split → dedup/contamination checks → safety/privacy/license review → training budget → rollback/base-model comparison.

Provider/model fine-tuning support changes over time and MUST be verified from current official documentation before implementation. Never invent an endpoint or train a model merely because fine-tuning sounds more advanced.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
