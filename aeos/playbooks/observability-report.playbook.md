# Playbook: observability-report

## Objective

Generate execution observability report.

## Steps

1. Collect logs, traces, metrics and audit events.
2. Build timeline.
3. Count tool/MCP/agent/Judge events.
4. Summarize blocks and failures.
5. Generate observability report.
6. Run Judge.

## Outputs

- `.aeos/observability/{execution_id}/timeline.md`
- `.aeos/reports/{execution_id}/observability-report.md`
