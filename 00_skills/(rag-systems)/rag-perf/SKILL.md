---
name: rag-perf
description: "Benchmark RAG latency and throughput from a config. Use for rag perf or a latency run. Do NOT use for training."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "2.6.0"
  owner_agent: codenavi-agent
---

# RAG Perf

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/rag-perf`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Run or specify a config-driven RAG performance benchmark without inventing latency numbers.

## Workflow

1. Confirm the perf config, query file, and CLI path in the user checkout.
2. Read the config schema before editing concurrency, prompt, or endpoint fields.
3. Execute only against an endpoint the user is allowed to load.
4. Report warmup, latency, throughput, and errors from the actual output.
5. Send quality scoring to rag-eval.

## Inputs, outputs, and stop

Inputs: perf config, authorized endpoint, and query set
Outputs: measured latency and throughput or the unrun command
Stop when a required tool, permission, or evidence check fails. Do not publish a number from an upstream sample as this run's result. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
