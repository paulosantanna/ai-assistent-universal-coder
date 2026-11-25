---
name: tilegym-adding-cutile-kernel
description: "Add a cuTile kernel to TileGym. Use for cutile kernel or tilegym ops. Do NOT use for cuDF."
license: "CC-BY-4.0 AND Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# TileGym cuTile Kernel

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/tilegym-adding-cutile-kernel`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Register, implement, export, and test one new cuTile operator in TileGym.

## Workflow

1. Confirm the TileGym checkout and the operator name, rank, and dtype.
2. Register the dispatch, implement the cuTile backend, and export it from the package init.
3. Add the test the procedure requires before calling the operator done.
4. Run the test command from the checkout. If the GPU or toolchain is missing, return the command unrun.
5. Lint only the files this operator changed.

## Inputs, outputs, and stop

Inputs: TileGym checkout and the operator contract
Outputs: dispatch, backend, export, and test evidence
Stop when a required tool, permission, or evidence check fails. Do not claim the kernel passed when the test command did not run. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
