---
name: security-threat-model
description: "Repo-grounded threat model: trust boundaries, assets, attackers, abuse paths. Use for threat modeling. Do NOT use for architecture summaries."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Security Threat Model

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Assimilated from installed `security-threat-model` 1.0.0. Original contract: `references/ORIGINAL_SKILL.md`. Output contract: `references/prompt-template.md`. Controls: `references/security-controls-and-assets.md`.

## Identity

Repo-grounded threat model: trust boundaries, assets, attackers, abuse paths. Use for threat modeling. Do NOT use for architecture summaries.

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

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [package-notes.md](references/package-notes.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
