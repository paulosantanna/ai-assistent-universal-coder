---
name: rag-blueprint
description: "Deploy or configure the NVIDIA RAG Blueprint. Use for rag blueprint deploy or troubleshoot. Do NOT use for model training."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "2.6.0"
  owner_agent: codenavi-agent
---

# RAG Blueprint

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/rag-blueprint`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Operate an authorized NVIDIA RAG Blueprint checkout: deploy, configure, troubleshoot, or shut down with evidence.

## Workflow

1. Confirm the RAG Blueprint checkout, target platform, and whether this request deploys, configures, troubleshoots, or shuts down.
2. Read the matching upstream module named in the procedure before changing a service.
3. Run read-only detection of GPU, Docker, and Kubernetes. Stop before deploy, shutdown, or deletion until the user confirms.
4. Apply only the confirmed change and verify the affected service.
5. Report commands, results, and anything that was not run.

## Inputs, outputs, and stop

Inputs: authorized blueprint checkout, target environment, and the feature to change
Outputs: verified service state or the exact unrun commands, plus remaining gaps
Stop when a required tool, permission, or evidence check fails. Do not deploy, tear down, or delete data without confirmation. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
