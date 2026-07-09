# Enterprise Micro Prompt 31

## Use Case

security java spring audit resilience skill risk redaction platform playbook opentelemetry testing latency ci compliance deployment kubernetes python slo subagent compliance judge.

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

Validation token: `f70fcbdc292cac2740c220afc395a2ff748102f41bc2348e12a5a1ab9976b6cc`
