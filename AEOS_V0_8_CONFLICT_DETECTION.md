# AEOS v0.8 — Conflict Detection Model

## Purpose

Prevent unsafe parallel execution.

## Conflict Types

```text
WRITE_WRITE
READ_WRITE
TOOL_SIDE_EFFECT
APPROVAL_SCOPE
RESOURCE_LOCK
EVIDENCE_CHAIN
AGENT_AUTHORITY
```

## Examples

### WRITE_WRITE

Step A writes:

```text
.aeos/sandbox/123/docs/README.md
```

Step B writes:

```text
.aeos/sandbox/123/docs/README.md
```

Result: conflict.

### READ_WRITE

Step A reads `pom.xml`.
Step B proposes patch to `pom.xml`.

Result: Step A must run before Step B or after patch stage depending on intended semantics.

### TOOL_SIDE_EFFECT

Two test runners executing against same generated environment.

Result: requires lock.

## Conflict Decision

```json
{
  "conflict_id": "...",
  "type": "READ_WRITE",
  "task_a": "...",
  "task_b": "...",
  "decision": "serialize|block|allow",
  "reason": "...",
  "evidence_refs": []
}
```
