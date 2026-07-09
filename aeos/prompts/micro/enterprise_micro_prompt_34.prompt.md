# Enterprise Micro Prompt 34

## Use Case

spring redaction subagent judge redaction mieptlmcpcdpkw evidence judge rkdgzxcu judge evidence benchmark iyugedqvukvnu xfhdzeixa kebyzmxvu agent python playbook eidpttt mcp spring supplychain.

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

Validation token: `533950a871bac0cd034c7c2ce95e1f4ebe9cb5ea9795288e3a2b10c82869b804`
