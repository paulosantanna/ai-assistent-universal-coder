# AEOS Agent Orchestration

## Principle

AEOS agents are specialized workers with narrow authority. The system must avoid the "superagent" anti-pattern.

## Agent Hierarchy

```text
Root Agent
  ├── Planner Agent
  ├── Architect Agent
  ├── Coder Agent
  ├── Tester Agent
  ├── Security Agent
  ├── DevOps Agent
  ├── Documenter Agent
  ├── Researcher Agent
  ├── Incident Agent
  └── Judge Agent
```

## Separation of Duties

- Implementing agent cannot judge its own work.
- Security Agent can block execution.
- Judge Agent can block finalization.
- Root Agent coordinates but does not bypass policy.
- Planner Agent creates task graph but cannot execute tool calls directly.
- Coder Agent proposes code changes but cannot apply without policy and approval.
- Tester Agent validates tests but cannot ignore failing tests.
- DevOps Agent proposes environment changes but cannot deploy automatically.

## Agent Lifecycle

```text
REGISTERED
AVAILABLE
ASSIGNED
RUNNING
WAITING_CONTEXT
WAITING_TOOL_RESULT
WAITING_APPROVAL
COMPLETED
BLOCKED
FAILED
ESCALATED
```

## Agent Trace

Every agent operation must produce:

```text
.aeos/evidence/{execution_id}/agent-trace.jsonl
```

Each entry must include:

- execution_id
- agent_id
- task_id
- state
- input_refs
- output_refs
- decisions
- risks
- evidence_refs
- timestamp
