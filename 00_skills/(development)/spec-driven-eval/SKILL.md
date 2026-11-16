---
name: spec-driven-eval
description: "Grade how fully an implementation fulfills a PRD, with one comparable score. Use when explicitly named. Do NOT use to build (tlc-spec-driven)."
license: CC-BY-4.0
metadata:
  author: Waldemar Neto - github.com/waldemarnt
  version: 1.0.0
  owner_agent: codenavi-agent
disable-model-invocation: true
---

# Spec-Driven Implementation Evaluation

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Scores how completely an implementation fulfills a PRD/spec, case by case, and produces a single comparable final grade. 

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [When to use](references/instructions/02-when-to-use.md) — when in scope.
- 3. [Inputs required](references/instructions/03-inputs-required.md) — before acting.
- 4. [Quick start](references/instructions/04-quick-start.md) — when in scope.
- 5. [Core rules (read first)](references/instructions/05-core-rules-read-first.md) — before acting.
- 6. [Reproducibility rules](references/instructions/06-reproducibility-rules.md) — before acting.
- 7. [Scoring model](references/instructions/07-scoring-model.md) — when in scope.
- 8. [Elicitation `E` — how well the framework *extracts* requirements (reported beside; never folded into Final)](references/instructions/08-elicitation-e-how-well-the-framework-extracts-requirements-reported-besi.md) — when in scope.
- 9. [Calibration (do this once per PRD, before trusting a benchmark)](references/instructions/09-calibration-do-this-once-per-prd-before-trusting-a-benchmark.md) — when in scope.
- 10. [Process](references/instructions/10-process.md) — when in scope.
- 11. [Output](references/instructions/11-output.md) — before acting.
- 12. [Worked example](references/instructions/12-worked-example.md) — when choosing an output or matching a use case.
- 13. [Anti-patterns](references/instructions/13-anti-patterns.md) — when choosing an output or matching a use case.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
