<!-- Package: 00_skills/(monitoring)/telemetry-bug-root-cause-solver; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# Telemetry Bug Root Cause Solver

```yaml
skill:
  name: Telemetry Bug Root Cause Solver
  slug: telemetry-bug-root-cause-solver
  version: 1.0.0
  description: Resolve bugs from logs, metrics, traces, events, alerts and stack traces by correlating runtime evidence with code, tests, rollback and learning records.
  category: REPAIR
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests bug fixing from logs, metrics, traces, observability evidence, pod events, CI logs, production errors or stack traces
    - a failure report includes timestamps, trace IDs, pod names, alert IDs, stack traces, exception chains or CI logs
  exclusions:
    - feature requests without a reproducible defect signal
    - production mutation without explicit approval
    - generic observability analysis that does not request a fix or root-cause repair plan
  inputs:
    - bug objective
    - repository path
    - runtime evidence or CI evidence
    - incident or failure time window
  outputs:
    - root_cause_report.md
    - fix_plan.md
    - test_matrix.md
    - rollback_plan.md
    - learning_candidate.md
    - evidence_index.md
  tools: []
  memory: true
  human_approval: true
  maintainer: AEOS
```
