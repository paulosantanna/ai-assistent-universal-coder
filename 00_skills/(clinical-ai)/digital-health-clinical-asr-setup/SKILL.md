---
name: digital-health-clinical-asr-setup
description: "Set up the clinical ASR flywheel host. Use for clinical asr setup or NVCF. Do NOT use for scoring or fine-tune."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.1.0"
  owner_agent: codenavi-agent
---

# Clinical ASR Setup

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/digital-health-clinical-asr-setup`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Prepare the clinical ASR flywheel host and prove the stack with a smoke test that does not reveal the API key.

## Workflow

1. State which calls would leave the machine before installing or testing.
2. Check NVIDIA_API_KEY by length only. Never echo it.
3. Install Python dependencies only with permission.
4. Run the hosted smoke test only after that disclosure.
5. Hand manifest work to the build skill and scoring to the eval skill.

## Inputs, outputs, and stop

Inputs: permission to use the hosted stack and a runtime key that stays in the environment
Outputs: setup status and smoke result without the key
Stop when a required tool, permission, or evidence check fails. Do not print, commit, or pass the raw key on a command line. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
