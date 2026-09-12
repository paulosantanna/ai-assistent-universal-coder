---
name: security-threat-model
description: "Assimilated OpenAI/TLC repo-grounded threat model. Enumerate trust boundaries, assets, attacker capabilities, abuse paths and mitigations into Markdown. Triggers: threat model, abuse paths, AppSec threat modeling. Do not use for architecture summaries, security-best-practices reviews, or ownership maps."
---

# Security Threat Model

Assimilated from installed `security-threat-model` 1.0.0. Original contract: `references/ORIGINAL_SKILL.md`. Output contract: `references/prompt-template.md`. Controls: `references/security-controls-and-assets.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

Produce an AppSec-grade threat model anchored to this repository (or an in-scope path). Every architectural claim needs evidence. Assumptions stay explicit.

## Relationship to AEOS

Existing `threat-modeler` / `security-audit` remain available. Use this skill when the user asked for the TLC/OpenAI threat-model workflow. It does not waive `specs`, security-governance or human-approval gates.

## Activation

- User asks to threat-model a codebase or path, enumerate abuse paths, or do AppSec threat modeling.

## Non-activation

- Generic architecture write-up (`technical-design-doc-creator`).
- Language best-practice report (`security-best-practices`).
- Git ownership map (`security-ownership-map`).

## Critical rules

1. Do not claim components, flows or controls without repo evidence.
2. Pause for 1–3 targeted scope questions before the final report when deployment/auth/exposure is unknown. If the user declines, keep assumptions explicit.
3. Write `<repo-or-dir-name>-threat-model.md` using `references/prompt-template.md`.
4. Load `references/security-controls-and-assets.md` when classifying assets and controls.
5. Follow the eight-step workflow in `references/ORIGINAL_SKILL.md`.
6. Do not persist secrets. Redact credentials in the model.

## Continuity

Promote only verified durable trust-boundary decisions into `.notebook/MEMORY.md`.
