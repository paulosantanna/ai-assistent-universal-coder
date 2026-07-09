# AEOS Tool Router Runtime

## Purpose

The Tool Router is the only gateway between AEOS logic and external execution.

It must:

- resolve tools by capability;
- verify permissions;
- enforce policy;
- route to MCP Runtime;
- apply timeout;
- redact output;
- persist tool-call evidence;
- reject direct access bypass.

## Tool Call Contract

```json
{
  "execution_id": "...",
  "request_id": "...",
  "agent_id": "...",
  "skill_id": "...",
  "playbook_id": "...",
  "mcp_id": "...",
  "tool_name": "...",
  "action": "...",
  "capability": "...",
  "input": {},
  "risk_level": "low|medium|high|critical",
  "requires_approval": false,
  "approval_id": null
}
```

## Tool Result Contract

```json
{
  "request_id": "...",
  "status": "success|blocked|failed|timeout",
  "output": {},
  "redacted": true,
  "evidence_refs": [],
  "duration_ms": 0,
  "policy_decision": {},
  "permission_decision": {},
  "errors": []
}
```

## Mandatory Blocking

Block if:

- MCP not registered;
- capability missing;
- tool not allowlisted;
- permission denied;
- policy denied;
- approval missing;
- action is destructive;
- output includes secrets;
- output schema invalid;
- timeout exceeded;
- direct tool bypass detected.
