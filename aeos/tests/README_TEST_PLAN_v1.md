# AEOS Test Plan v1

## Required test categories

```text
unit/
integration/
policy/
permission/
judge/
tool_router/
mcp_runtime/
agent_runtime/
packaging/
approval/
evidence_integrity/
security/
```

## Must-have negative tests

- permission deny-all blocks unknown action;
- Tool Router blocks unregistered MCP;
- Judge blocks missing evidence;
- Judge blocks hash mismatch;
- package verify blocks path traversal;
- package verify blocks secret;
- approval validator blocks wildcard scope;
- branch manager blocks main/master/develop;
- direct tool bypass is detected;
- critical MCP disabled by default;
- auto-merge prohibited.
