# Enterprise Micro Prompt 26

## Use Case

judge skill governance enterprise zrsye java rollback throughput platform enterprise production rollback mcp supplychain spring opentelemetry platform deployment throughput audit java latency.

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

Validation token: `eacc12a2bce3dd3c9c83e5fb21370556a89d1de6d2cc84f0ba8960b4073f03bc`

## Prompt Contract

- Keep the objective bounded to the requested task.
- Prefer file refs, registry refs and evidence refs over pasted context.
- Distinguish facts, assumptions, risks and recommendations.
- Require evidence for material claims and mark missing evidence as a blocker.
- Route tools through approved AEOS command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return `PASS`, `BLOCKED` or `REVIEW` with evidence refs and blocking conditions.
