# Enterprise Playbook: supply-chain-integrity-audit

## Objective

Audit dependency and artifact integrity.

## Operating Mode

Production-governed, fail-closed, evidence-first.

## Required Agents

- Root
- Planner
- Architect
- Security
- Judge

## Required LCPs

- global-rules
- security-governance
- enterprise-production

## Required Skills

- enterprise-repo-intelligence
- performance-profiler
- supply-chain-auditor
- release-readiness-judge

## Required MCPs

- filesystem-readonly
- git-readonly
- package-local
- test-runner-controlled, when tests are required

## Performance Budget

```yaml
p50_seconds: 60
p95_seconds: 300
max_file_mb: 5
skip_generated_dirs: true
cache_allowed: true
cache_requires_strong_key: true
```

## Steps

1. Load AEOS production enterprise config.
2. Resolve workbench profile.
3. Resolve LCPs.
4. Build task graph.
5. Compute read/write sets.
6. Run dry-run.
7. Validate permission and policy decisions.
8. Execute read-only/sandbox operations only.
9. Collect evidence.
10. Emit observability trace.
11. Generate report.
12. Verify evidence integrity.
13. Run deterministic Judge.
14. Package review bundle when requested.

## Blocking Conditions

- Missing evidence.
- Missing permission decision.
- Missing policy decision.
- Secret exposure.
- Tool Router bypass.
- Wildcard approval.
- Unverified package.
- Hash mismatch.
- Unbounded execution.
- Performance budget exceeded without report.
- Judge deterministic failure.

## Outputs

```text
.aeos/reports/{execution_id}/supply-chain-integrity-audit.md
.aeos/evidence/{execution_id}/
.aeos/observability/{execution_id}/
```

## Final Report Required Sections

- Executive summary
- Technical summary
- Facts
- Assumptions
- Risks
- Evidence
- Performance
- Security
- Recommendations
- Blocking conditions
- Judge decision
