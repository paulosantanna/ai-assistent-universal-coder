---
name: spec-driven-eval
description: Scores how completely an implementation fulfills a PRD/spec, case by case, and produces a single comparable final grade. Invoke only when explicitly named (e.g. run spec-driven-eval); do not auto-trigger. Use when benchmarking spec-driven implementations, grading acceptance criteria, evaluating whether a feature was 100% implemented, comparing multiple implementations of the same PRD, or auditing implementation and test coverage (unit and e2e) against product requirements. Do NOT use for planning or building features (use tlc-spec-driven), writing PRDs, or general code review unrelated to a spec.
license: CC-BY-4.0
metadata:
  author: Waldemar Neto - github.com/waldemarnt
  version: 1.0.0
  owner_agent: codenavi-agent
disable-model-invocation: true
---

# Spec-Driven Implementation Evaluation

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Scores how completely an implementation fulfills a PRD/spec, case by case, and produces a single comparable final grade. Invoke only when explicitly named (e.g. run spec-driven-eval); do not auto-trigger.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [When to use](references/instructions/02-when-to-use.md) — when this domain or mode is in scope.
- 3. [Inputs required](references/instructions/03-inputs-required.md) — before acting on this contract.
- 4. [Quick start](references/instructions/04-quick-start.md) — when this domain or mode is in scope.
- 5. [Core rules (read first)](references/instructions/05-core-rules-read-first.md) — before acting on this contract.
- 6. [Reproducibility rules](references/instructions/06-reproducibility-rules.md) — before acting on this contract.
- 7. [Scoring model](references/instructions/07-scoring-model.md) — when this domain or mode is in scope.
- 8. [Elicitation `E` — how well the framework *extracts* requirements (reported beside; never folded into Final)](references/instructions/08-elicitation-e-how-well-the-framework-extracts-requirements-reported-besi.md) — when this domain or mode is in scope.
- 9. [Calibration (do this once per PRD, before trusting a benchmark)](references/instructions/09-calibration-do-this-once-per-prd-before-trusting-a-benchmark.md) — when this domain or mode is in scope.
- 10. [Process](references/instructions/10-process.md) — when this domain or mode is in scope.
- 11. [Output](references/instructions/11-output.md) — before acting on this contract.
- 12. [Worked example](references/instructions/12-worked-example.md) — when choosing an output or matching a use case.
- 13. [Anti-patterns](references/instructions/13-anti-patterns.md) — when choosing an output or matching a use case.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
