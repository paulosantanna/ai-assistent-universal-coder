# AEOS Agent Message Protocol

## Purpose

Standardize communication between AEOS agents, subagents, Kernel, Skill Executor, Tool Router, and Judge.

## Message Types

```text
goal.received
plan.proposed
task.created
task.assigned
task.started
context.requested
context.delivered
tool.requested
tool.result_observed
evidence.submitted
risk.reported
approval.requested
approval.received
judge.requested
judge.result
task.completed
task.blocked
task.failed
escalation.requested
```

## Message Envelope

```json
{
  "message_id": "...",
  "execution_id": "...",
  "parent_message_id": null,
  "task_id": "...",
  "from_agent": "root",
  "to_agent": "architect",
  "message_type": "task.assigned",
  "intent": "map_architecture",
  "payload": {},
  "context_refs": [],
  "evidence_refs": [],
  "risk_level": "low|medium|high|critical",
  "requires_ack": true,
  "created_at": "ISO-8601"
}
```

## Rules

- Messages must not include raw secrets.
- Large content must be referenced, not embedded.
- Evidence must be referenced by path/hash.
- Tool results must be redacted.
- Agent messages must be immutable once persisted.
