# Enterprise Micro Prompt 35

## Use Case

benchmark mcp policy opentelemetry ci toolrouter production enterprise mcp evidence testing deployment scalability java redaction evidence agent judge runtime latency kubernetes judge.

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

Validation token: `158312b02c7ef51d4dc89f4d24dfdee1535c8046fe0bbc5780fbeae2bb5645da`
