---
name: dicom-metadata-extract
description: "Extract DICOM metadata without pixels. Use for dicom metadata extract. Do NOT use for diagnosis or series QA."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# DICOM Metadata Extract

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/dicom-metadata-extract`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Extract DICOM metadata from files the user is allowed to read, without pixels and without an impression.

## Workflow

1. Confirm authorization to read the DICOM and that the output may not leave the machine.
2. Run metadata extraction only. Do not decode pixel data.
3. Redact patient identifiers in any note or chat summary.
4. Return tag groups, transfer syntax, and missing tags.
5. Send series consistency checks to dicom-series-preflight.

## Inputs, outputs, and stop

Inputs: authorized DICOM paths
Outputs: metadata summary with identifiers redacted
Stop when a required tool, permission, or evidence check fails. Stop on a diagnostic question. This skill does not interpret images. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
