# Playbook: agent-runtime-smoke-test

## Objective

Validate Agent Runtime without mutating the project.

## Steps

1. Load agent runtime config.
2. Load agent registry.
3. Validate delegation policy.
4. Create minimal task graph.
5. Route context to Root, Planner, Architect, Security and Judge.
6. Generate agent trace.
7. Validate no direct tool access.
8. Run Judge v7.

## Outputs

- `.aeos/evidence/{execution_id}/task-graph.json`
- `.aeos/evidence/{execution_id}/agent-trace.jsonl`
- `.aeos/reports/{execution_id}/agent-runtime-smoke-test.md`
- `.aeos/reports/{execution_id}/judge-report.md`

## Blocking Conditions

- missing agent trace;
- invalid delegation;
- self-judging;
- direct tool access;
- missing context routing;
- missing evidence.
