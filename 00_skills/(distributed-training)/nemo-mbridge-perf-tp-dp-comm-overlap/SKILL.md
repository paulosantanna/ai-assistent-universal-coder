---
name: nemo-mbridge-perf-tp-dp-comm-overlap
description: "Overlap TP, DP, and PP communication. Use for comm overlap. Do NOT use for CUDA graphs."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# TP DP Communication Overlap

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-tp-dp-comm-overlap`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Enable one communication-overlap setting that the checkout still implements.

## Workflow

1. Identify which of TP, DP, or PP overlap the user needs.
2. Set only the knobs in the enablement section.
3. Compare those knobs with the current code anchors.
4. Run the verification or return it unrun.
5. Stop on a pitfall the procedure marks as a silent slowdown.

## Inputs, outputs, and stop

Inputs: parallelism config and the overlap target
Outputs: overlap config and verification status
Stop when a required tool, permission, or evidence check fails. Do not copy an overlap flag that the checkout has removed. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
