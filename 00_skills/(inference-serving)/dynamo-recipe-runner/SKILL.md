---
name: dynamo-recipe-runner
description: "Select and deploy an existing Dynamo Kubernetes recipe. Use for dynamo recipe or GPU serving. Do NOT use for training."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Dynamo Recipe Runner

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/dynamo-recipe-runner`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Select, validate, and optionally deploy an existing Dynamo recipe without inventing manifests.

## Workflow

1. Collect model, framework, mode, GPU shape, namespace, and whether commands may run.
2. Preflight with read-only kubectl and the checkout's recipe tool.
3. Select an existing recipe and patch only the values the procedure allows.
4. Deploy only after confirmation. If the cluster is down, return exact commands.
5. Smoke-test the named service and report what did not run.

## Inputs, outputs, and stop

Inputs: Dynamo checkout, recipe identity, and authorized cluster context
Outputs: selected recipe, diff, and deploy or smoke evidence
Stop when a required tool, permission, or evidence check fails. Do not invent a recipe or claim a deploy that did not run. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
