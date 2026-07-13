# Enterprise Micro Prompt 55

## Use Case

ci testing incident evidence redaction audit ci governance artifact scalability redaction latency deployment observability observability spring python observability skill playbook production runtime.

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

Validation token: `9778ca291e60972127c9e1865af7adbbc812acf82734fc38b020938405e31dfd`

## Prompt Contract

- Keep the objective bounded to the requested task.
- Prefer file refs, registry refs and evidence refs over pasted context.
- Distinguish facts, assumptions, risks and recommendations.
- Require evidence for material claims and mark missing evidence as a blocker.
- Route tools through approved AEOS command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return `PASS`, `BLOCKED` or `REVIEW` with evidence refs and blocking conditions.
