# Agent Runtime Implementation Guide

## Minimum Vertical Slice

Implement:

```text
aeos run agent-runtime-smoke-test --target <path>
```

Expected outputs:

```text
.aeos/evidence/{execution_id}/task-graph.json
.aeos/evidence/{execution_id}/agent-trace.jsonl
.aeos/reports/{execution_id}/agent-runtime-smoke-test.md
.aeos/reports/{execution_id}/judge-report.md
```

## Implementation Order

1. Load `aeos/config/agent.runtime.yaml`.
2. Load `aeos/config/delegation.policy.yaml`.
3. Load agent registry.
4. Validate agents and subagents.
5. Implement TaskDefinition and TaskGraph.
6. Implement DelegationPolicyEngine.
7. Implement ContextRouter.
8. Implement AgentTraceStore.
9. Implement AgentRuntime smoke test.
10. Implement Judge v7 validations.

## Do Not Implement Yet

- autonomous code mutation;
- self-approval;
- direct MCP calls from agents;
- secrets runtime;
- production mutation.
