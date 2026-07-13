# Playbook: performance-optimization

## Objective

Improve AEOS performance across Python core, runtime, LSP and project workflows without weakening governance, evidence, rollback or security gates.

## Required Skills

- performance-optimizer
- token-budget-governor
- change-trace-auditor
- test-generation
- chromatic-mega-brain

## Required MCPs

- filesystem-readonly
- filesystem-write-sandbox
- test-runner-controlled
- package-local

## Required LCPs

- global-rules
- token-economy
- security-governance

## Steps

1. Load performance budgets and identify hot paths.
2. Capture current evidence from tests, timing or code inspection.
3. Choose bounded optimizations with explicit invalidation and rollback.
4. Implement cache, batching, pruning, indexing or concurrency changes.
5. Run focused tests for each optimized subsystem.
6. Run full verification before declaring PASS.
7. Generate a traceable change set with rollback instructions.

## Blocking Conditions

- Optimization bypasses security, evidence, permission or Judge checks.
- Cache invalidation is undefined.
- Full verification fails.
- Change set is missing rollback instructions.

## Outputs

- performance optimization plan
- changed files list
- validation report
- rollback-aware change set
