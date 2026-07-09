# AEOS Performance Engineering

## Performance Goals

AEOS must be efficient enough for large monorepos and multi-repo ecosystems.

## Key Budgets

```yaml
performance_budgets:
  repo_scan:
    p50_seconds: 30
    p95_seconds: 180
  stack_detection:
    p50_seconds: 10
    p95_seconds: 60
  dependency_analysis:
    p50_seconds: 45
    p95_seconds: 300
  evidence_verify:
    p50_seconds: 15
    p95_seconds: 120
  package_verify:
    p50_seconds: 20
    p95_seconds: 180
  judge_deterministic:
    p50_seconds: 5
    p95_seconds: 30
```

## Optimization Principles

- stream large files;
- hash incrementally;
- cache only with strong keys;
- avoid reading generated directories;
- avoid scanning binary artifacts unless required;
- index repo metadata;
- use parallel read-only steps only after conflict detection;
- keep LLM context minimal;
- pass file refs, not huge file bodies;
- separate deterministic checks from LLM reviews.

## Skip Defaults

```text
.git
node_modules
target
build
dist
.venv
venv
__pycache__
.gradle
.m2
.idea
.vscode
coverage
```

## Performance Evidence

Every heavy operation must emit:

- duration;
- files inspected;
- bytes read;
- cache hit/miss;
- skipped directories;
- p50/p95 estimate;
- bottlenecks;
- optimization recommendation.
