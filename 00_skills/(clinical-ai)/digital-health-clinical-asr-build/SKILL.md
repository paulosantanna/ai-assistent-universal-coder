---
name: digital-health-clinical-asr-build
description: "Build a clinical ASR term manifest. Use for clinical asr build or IPA tags. Do NOT use for scoring."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.1.0"
  owner_agent: codenavi-agent
---

# Clinical ASR Build

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/digital-health-clinical-asr-build`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Build a NeMo manifest of clinical terms with IPA tags after disclosing any outbound generation.

## Workflow

1. Disclose hosted generation before any term is sent.
2. Interview the specialty only from sources the user provides. Do not invent a formulary.
3. Tag IPA with the two-tier method and keep the QA synthesis gate.
4. Write the manifest in the schema the procedure names.
5. Do not score it here.

## Inputs, outputs, and stop

Inputs: specialty scope and permission for hosted generation
Outputs: term seed, IPA tags, and manifest path
Stop when a required tool, permission, or evidence check fails. Stop when the QA synthesis gate fails. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
