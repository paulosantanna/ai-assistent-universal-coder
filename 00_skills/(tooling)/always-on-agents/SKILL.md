---
name: always-on-agents
description: "Code-only same-model workers. Use for always-on agents or agentes always-on. Do NOT use for Ollama, paid unlimited spawn, or new agent identities."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# always-on-agents

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Run one generation of same-host, same-model workers that write code and die. Paid or unknown models ask first and stay capped at three processes. A model is unlimited only when it is declared free and is not a priced family. Ollama never runs.

## Workflow

1. Read [usage](references/usage.md). Run `plan` with this window's host and model. Do not infer the model.
2. If `action` is `ask`, show only `question` and stop. Continue only after the user answers sim, yes or aprovo.
3. Follow [contract](references/contract.md): spec-driven, then spec-driven-lean, request-oracle tests, a DDD glossary, then the-fool and the-judge lenses as separate processes.
4. Workers write files. Uncertainty is one `QUESTION:` line. Anything else on stdout fails the silence check.
5. Score the generation. Below 9.5 it is dead. Paid recreation asks again. Free recreation uses a new id.

## Inputs and outputs

- Inputs: host (`cursor` or `opencode`), the model id this window is already using, the task, and a user answer when billing is not free.
- Outputs: one JSON object. Surface only `question`, or the score and the changed paths.

## Verification

From this package, run `python scripts/run_tests.py` (`py -3 scripts/run_tests.py` on Windows). The sum request, the paid gate and the negative proofs are executable checks.

## Stop conditions

Missing model, paid use without a user answer, Ollama, a score under 9.5, or a request to invent an agent identity.

## Modules

- Read [research](references/research.md) when citing Cursor, OpenCode, billing or the AGENT pillars.
- Read [contract](references/contract.md) before spawning or scoring.
- Read [usage](references/usage.md) before the first command.

## Response

Output: result first. Evidence is the JSON and the test command. A paid model stops on the question. Do not narrate the worker plan. Reply in the user's language.
