---
name: rag-eval
description: "Score an on-disk RAG corpus and train.json. Use for rag eval or retrieval metrics. Do NOT use for deployment."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "2.6.0"
  owner_agent: codenavi-agent
---

# RAG Eval

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/rag-eval`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Evaluate an on-disk RAG corpus with a declared dataset and report only metrics that were actually computed.

## Workflow

1. Confirm corpus/, train.json, and the evaluator entrypoint exist in the checkout the user names.
2. Read dataset conversion and CLI flags from the procedure. Do not invent metric definitions.
3. Run the evaluation only when the toolchain is present; otherwise return the command unrun.
4. Separate retrieval metrics from answer metrics and keep failed rows.
5. Hand latency work to rag-perf and deployment work to rag-blueprint.

## Inputs, outputs, and stop

Inputs: authorized corpus, train split, and evaluator checkout
Outputs: metric table with the command, dataset identity, and unrun checks
Stop when a required tool, permission, or evidence check fails. Do not deploy services or treat a missing CLI as a successful score. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
