# Enterprise Micro Prompt 37

## Use Case

policy cache opentelemetry skill security subagent approval toolrouter rollback production supplychain compliance deployment mcp skill rollback ci mcp risk policy artifact rag.

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

Validation token: `60c27cce8353deac27ba64e9533344d652770af84529660072a9a2e5607318b7`
