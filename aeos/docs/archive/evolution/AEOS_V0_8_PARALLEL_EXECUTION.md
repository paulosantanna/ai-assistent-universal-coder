# AEOS v0.8 — Parallel Execution, Dependency Graph & Conflict Detection

## Mission

Enable controlled parallel execution for playbook steps and agent tasks without breaking determinism, evidence integrity, or safety.

## Why This Matters

Parallel execution is useful only after AEOS has:

- Task Graph;
- Evidence Store;
- Permission Engine;
- Policy Engine;
- Tool Router;
- Judge;
- read/write set detection;
- conflict checks.

Parallel execution without conflict detection creates non-deterministic automation.

## Core Concepts

```text
Task DAG
Read Set
Write Set
Resource Lock
Conflict Detector
Deterministic Scheduler
Parallel Step Runner
Barrier Step
Join Step
```

## Read/Write Set

Every step must declare:

```yaml
read_set:
  - "src/main/**"
  - "pom.xml"

write_set:
  - ".aeos/sandbox/{execution_id}/**"
```

If write sets overlap, steps cannot run in parallel.

If one step writes a path another step reads, the reader must wait.

## Scheduler Rules

- deterministic task ordering;
- no parallel writes to same path;
- no write outside sandbox without approval;
- high-risk steps default to sequential;
- security scans can run parallel with read-only analysis;
- Judge runs after all required tasks complete;
- evidence hash-chain must preserve event order.

## Blocking Conditions

- missing read_set/write_set;
- conflict not resolved;
- non-deterministic step result;
- missing task result;
- hash-chain gap;
- parallel step wrote outside approved scope;
- failed required dependency.
