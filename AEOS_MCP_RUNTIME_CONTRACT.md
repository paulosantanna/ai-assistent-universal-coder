# AEOS MCP Runtime Contract

## MCP Runtime Responsibilities

The MCP Runtime manages local and remote MCP-compatible adapters.

v0.6 only supports local controlled adapters and stdio-style process contracts.

## Required MCP Definition

```yaml
mcp:
  id:
  type:
  transport:
  command:
  args:
  working_dir:
  env:
  capabilities:
  tools:
  risk_level:
  timeout_seconds:
  retries:
  approval_required:
  sandbox_required:
  redaction_required:
  evidence_required:
  input_schema:
  output_schema:
```

## Runtime State

Each MCP server must have lifecycle state:

```text
UNINITIALIZED
STARTING
READY
DEGRADED
FAILED
STOPPING
STOPPED
```

## Health Check

Every MCP must expose or simulate:

```text
health.status
health.capabilities
health.tools
health.version
```

## Evidence

Every MCP invocation must append to:

```text
.aeos/evidence/{execution_id}/mcp-calls.jsonl
.aeos/evidence/{execution_id}/tool-calls.jsonl
.aeos/evidence/{execution_id}/permission-decisions.jsonl
.aeos/evidence/{execution_id}/policy-decisions.jsonl
```
