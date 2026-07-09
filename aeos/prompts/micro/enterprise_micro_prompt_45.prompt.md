# Enterprise Micro Prompt 45

## Use Case

latency java python approval rag observability judge throughput bsrnzvjcils platform resilience incident skill mcp mcp runtime python security performance java rag toolrouter.

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

Validation token: `21b72e987891628a74a9b34207904bf65ce172536c3c48a86d12d7840181b1c6`
