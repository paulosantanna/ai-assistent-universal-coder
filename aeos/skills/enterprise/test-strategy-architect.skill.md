# Enterprise Skill: test-strategy-architect

## Mission

Build test strategy across unit/integration/contract/e2e/security/performance.

## Production Scope

This skill is intended for enterprise production governance. It must be bounded, evidence-based, policy-checked and performance-aware.

## Allowed Actions

- Read authorized files through Tool Router.
- Read evidence refs.
- Read config/registry metadata.
- Generate reports under `.aeos/reports`.
- Generate evidence under `.aeos/evidence`.
- Generate sandbox artifacts under `.aeos/sandbox`.
- Request MCP calls only through Skill Executor and Tool Router.

## Forbidden Actions

- Direct filesystem/Git/shell/MCP calls.
- Raw secret reading.
- Raw secret persistence.
- Auto-merge.
- Auto-deploy.
- Wildcard approval.
- Unsupported factual claims.
- Bypass of Permission Engine, Policy Engine or Judge.
- Mutating files outside approved sandbox/patch workflow.

## Required Inputs

```yaml
input:
  execution_id:
  target_path:
  profile:
  scope:
  evidence_refs:
  performance_budget:
  risk_tolerance:
```

## Required Output Schema

```json
{
  "skill_id": "test-strategy-architect",
  "status": "PASS|BLOCKED|REVIEW",
  "facts": [],
  "assumptions": [],
  "risks": [],
  "recommendations": [],
  "evidence_refs": [],
  "performance": {
    "duration_ms": 0,
    "files_inspected": 0,
    "bytes_read": 0,
    "cache_hit": false
  },
  "blocking_conditions": []
}
```

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates

- Facts cite evidence.
- Assumptions are explicit.
- Risks have severity.
- Recommendations have owner/action/impact.
- Performance budget is reported.
- No raw secrets.
- No unbounded work.
- Judge can validate deterministically.

## Stop Conditions

- Missing target path.
- Missing evidence for factual claim.
- Secret detected in output.
- Tool Router bypass detected.
- Permission denied.
- Policy denied.
- Performance budget exceeded without explanation.
