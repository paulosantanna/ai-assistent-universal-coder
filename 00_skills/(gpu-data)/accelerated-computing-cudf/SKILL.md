---
name: accelerated-computing-cudf
description: "Accelerate pandas with cuDF or dask-cuDF. Use for cudf joins or GPU dataframes. Do NOT use for model training."
license: "CC-BY-4.0 AND Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# cuDF

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/accelerated-computing-cudf`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Move a pandas-style workload to cuDF, cudf.pandas, or dask-cuDF with an explicit parity check.

## Workflow

1. Read the installed cuDF version and choose cudf.pandas, explicit cuDF, or dask-cuDF from the data size and the requested control.
2. Keep intermediate frames on GPU and convert only at a real CPU boundary.
3. Compare shape, nulls, order, and sample values against pandas on a representative slice before claiming parity.
4. Move to dask-cuDF with spill when the working set exceeds GPU memory.
5. Report the version, path, and any API that was not covered.

## Inputs, outputs, and stop

Inputs: authorized data sample, current cuDF install, and the operation to accelerate
Outputs: GPU code path plus the parity comparison that was run
Stop when a required tool, permission, or evidence check fails. Do not claim a speedup without a measurement on representative data. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
