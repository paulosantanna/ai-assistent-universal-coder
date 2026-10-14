---
name: performance-optimizer
description: Measure, classify and improve AEOS hot paths across registry loading, skill execution, evidence writing, repository scanning, LSP indexing and TypeScript runtime execution. Use when the user requests performance optimizer or invokes performance-optimizer. Do NOT use for unrelated functionality or unmeasured speculative optimization.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: performance-optimizer

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Measure, classify and improve AEOS hot paths across registry loading, skill execution, evidence writing, repository scanning, LSP indexing and TypeScript runtime execution.

## Allowed Actions

- Read performance budgets, metrics and test output.
- Produce optimization plans tied to measured bottlenecks.
- Recommend cache, batching, pruning, indexing and concurrency improvements.
- Generate sandbox reports and performance evidence.
- Route risky implementation changes through Judge.

## Forbidden Actions

- Hide failing performance gates.
- Optimize by skipping required security, evidence, rollback or Judge checks.
- Expand task scope beyond performance work without approval.
- Treat anecdotal speedups as verified without tests or benchmark evidence.

## Required Inputs

- target_scope
- performance_budgets
- evidence_refs
- changed_files

## Output Schema

```json
{
  "status": "PASS|WARN|BREACHED|BLOCKED",
  "signals": [],
  "summary": {},
  "recommendations": [],
  "blocking_conditions": [],
  "evidence_refs": []
}
```

## Workflow

1. Identify the smallest useful performance scope.
2. Map hot paths to budget categories.
3. Prefer structural wins: cache reuse, directory pruning, batch I/O, indexed lookup and bounded parallelism.
4. Preserve governance, traceability, rollback, security and token-budget gates.
5. Add regression tests for behavior and performance contracts.
6. Record a rollback-aware change set for implemented optimizations.

## Quality Gates

- Every performance claim cites a test, benchmark or deterministic code path.
- Optimizations do not bypass governance.
- Cache invalidation is explicit.
- Large repository scanning has exclusion and large-file safeguards.
- Runtime caches can be invalidated.
- Rollback plan exists for modified files.

## Stop Conditions

- Missing performance budget.
- Requested optimization would bypass required evidence or approval.
- Benchmark cannot be reproduced.
- Rollback trace is missing.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
