---
name: dicom-series-preflight
description: "Preflight a DICOM series before training. Use for dicom series preflight. Do NOT use for metadata-only extract."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# DICOM Series Preflight

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/dicom-series-preflight`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Check a DICOM series for training readiness and report failures without a clinical reading.

## Workflow

1. Confirm the series path and the training use the user intends.
2. Run the preflight checks in the procedure: consistency, geometry, and required tags.
3. Do not extract a full metadata dump; that is dicom-metadata-extract.
4. Write the pass or fail list. Do not describe a diagnosis.
5. Keep DICOM files out of git.

## Inputs, outputs, and stop

Inputs: authorized DICOM series
Outputs: preflight pass or fail with the failing checks
Stop when a required tool, permission, or evidence check fails. Stop if the series is not authorized or the tool is missing. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
