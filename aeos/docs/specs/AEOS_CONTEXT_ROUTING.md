# AEOS Context Routing

## Purpose

Context Routing decides what context each agent receives.

Agents must not receive the entire repository blindly.

## Context Sources

```text
LCPs
Skills
Playbooks
Memory
Evidence
Project files
Reports
Task graph
Prior agent outputs
```

## Routing Rules

- Security LCP always loads for risky tasks.
- Stack LCP loads only when stack indicators support it.
- Project memory loads only if relevant to task scope.
- Secrets are never loaded as raw values.
- Evidence refs are preferred over embedded large content.
- Context must be minimized, not accumulated.
- Facts and assumptions must remain separated.

## Context Packet

```json
{
  "context_id": "...",
  "task_id": "...",
  "agent_id": "...",
  "loaded_lcps": [],
  "memory_refs": [],
  "file_refs": [],
  "evidence_refs": [],
  "rules": [],
  "forbidden_actions": [],
  "quality_gates": [],
  "token_budget": 0
}
```
