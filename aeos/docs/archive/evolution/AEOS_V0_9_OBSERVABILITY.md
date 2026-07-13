# AEOS v0.9 — Observability

## Mission

Make every AEOS execution inspectable.

## Signals

```text
Logs
Metrics
Traces
Audit Events
Tool Calls
MCP Calls
Agent Messages
Task States
Token Usage
Cost Estimates
Cache Hits/Misses
Approval Events
Judge Decisions
```

## Required Files

```text
.aeos/observability/{execution_id}/execution.log.jsonl
.aeos/observability/{execution_id}/trace.jsonl
.aeos/observability/{execution_id}/metrics.json
.aeos/observability/{execution_id}/cost.json
.aeos/observability/{execution_id}/timeline.md
```

## Trace Span

```json
{
  "span_id": "...",
  "parent_span_id": "...",
  "execution_id": "...",
  "name": "skill.repo-scanner",
  "kind": "skill|tool|mcp|agent|judge|policy|permission",
  "started_at": "...",
  "ended_at": "...",
  "duration_ms": 0,
  "status": "ok|blocked|failed",
  "evidence_refs": []
}
```

## Metrics

- execution_duration_ms
- tool_call_count
- mcp_call_count
- agent_message_count
- permission_denied_count
- policy_block_count
- judge_block_count
- generated_artifacts_count
- cache_hit_count
- cache_miss_count
- tests_run_count
- tests_failed_count
