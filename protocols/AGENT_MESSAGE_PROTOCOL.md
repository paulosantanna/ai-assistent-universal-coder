# AGENT_MESSAGE_PROTOCOL.md

## Message envelope

```json
{
  "message_id": "uuid",
  "trace_id": "uuid",
  "parent_id": "uuid|null",
  "from": "agent_id",
  "to": "agent_id",
  "type": "task|evidence|finding|risk|decision|checkpoint|result|escalation",
  "priority": "low|normal|high|critical",
  "payload": {},
  "timestamp": "iso-8601"
}
```

## Rule

Agents communicate through structured messages, not vague prose when execution state matters.
