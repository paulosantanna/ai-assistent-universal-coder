# Enterprise Micro Prompt 16

## Use Case

redaction skill agent rollback throughput redaction skill ci deployment redaction benchmark redaction resilience security observability slo throughput artifact agent latency ci approval.

## Prompt

Perform the task with strict enterprise controls.

Constraints:
- use evidence refs;
- avoid raw secrets;
- route tools through Tool Router;
- report performance;
- stop on missing policy/permission;
- distinguish Fact, Assumption, Risk, Recommendation.

Output:
```json
{
  "status": "PASS|BLOCKED|REVIEW",
  "facts": [],
  "assumptions": [],
  "risks": [],
  "recommendations": [],
  "evidence_refs": [],
  "performance": {}
}
```

Validation token: `deb426532c6d0351745b200310403f416629ca5ce0534cdcd53b78ac1cff09d0`
