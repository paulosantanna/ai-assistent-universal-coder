# Playbook: Test Recovery

## Objective

Analyze failing tests, identify root causes, and generate fixes to restore test suite health.

## Preconditions

- Workspace path exists.
- Test suite exists and has been run previously.
- MCPs for filesystem read/write, shell, git, and test runner available.
- Global rules LCP loaded.

## Agents

- Root Agent
- Tester Agent
- Coder Agent
- Judge Agent

## Skills

- test-generation
- repo-scanner

## MCPs

- filesystem-readonly
- filesystem-write-sandbox
- git-readonly
- shell-controlled
- test-runner

## Steps

1. Run existing test suite and capture results.
2. Identify failing tests and group by failure pattern.
3. Analyze test code and production code for root cause.
4. Generate fix proposals for each failure pattern.
5. Apply fixes to sandbox and re-run affected tests.
6. Run full test suite to verify no regressions.
7. Generate test recovery report with evidence.
8. Send outputs to Judge Agent.
9. Generate judge-report.md.

## Blocking Conditions

- Tests cannot be run (missing dependencies).
- No evidence of root cause analysis.
- Proposed fixes not validated by re-run.
- Fix introduced regressions.
- Rollback plan not available.

## Outputs

- .aeos/test-recovery-report.md
- .aeos/test-results-before.md
- .aeos/test-results-after.md
- .aeos/failure-analysis.md
- .aeos/judge-report.md
