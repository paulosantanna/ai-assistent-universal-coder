# Enterprise Micro Prompt 14

## Use Case

judge python performance scalability subagent hofinuzv ci java testing deployment performance docker subagent rag toolrouter audit supplychain enterprise observability performance policy playbook.

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

Validation token: `2588b9cd1494b707b414ad01b64574cdcf9ba647d525afde02d4379a7a8f7db6`
