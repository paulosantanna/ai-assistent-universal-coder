# Enterprise Micro Prompt 23

## Use Case

artifact approval security rag platform lagls skill toolrouter python incident platform benchmark opentelemetry rag playbook python opentelemetry latency omzbzo sandbox kubernetes slo.

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

Validation token: `965ff3f1de5959545de7b1978de7f7b86171ea7dafe9768947de129b1daf695b`

## Prompt Contract

- Keep the objective bounded to the requested task.
- Prefer file refs, registry refs and evidence refs over pasted context.
- Distinguish facts, assumptions, risks and recommendations.
- Require evidence for material claims and mark missing evidence as a blocker.
- Route tools through approved AEOS command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return `PASS`, `BLOCKED` or `REVIEW` with evidence refs and blocking conditions.
