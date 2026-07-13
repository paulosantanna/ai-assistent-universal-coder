# Enterprise Micro Prompt 17

## Use Case

audit runtime runtime incident benchmark nirotvavzwg slo platform governance agent testing observability imfnfhkrvehuy python resilience java tmsmgvh opentelemetry judge platform judge subagent.

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

Validation token: `2741494c241f09f076a80b52dce634efe35591e7627e08736dcfef2546a6d281`

## Prompt Contract

- Keep the objective bounded to the requested task.
- Prefer file refs, registry refs and evidence refs over pasted context.
- Distinguish facts, assumptions, risks and recommendations.
- Require evidence for material claims and mark missing evidence as a blocker.
- Route tools through approved AEOS command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return `PASS`, `BLOCKED` or `REVIEW` with evidence refs and blocking conditions.
