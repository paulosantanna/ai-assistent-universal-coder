# AEOS Enterprise Architecture

## Top-Level Modules

```text
aeos/
  core/
    kernel/
    permissions/
    policy/
    tool_router/
    mcp_runtime/
    agent_runtime/
    playbook_engine/
    skill_engine/
    lcp_engine/
    evidence/
    judge/
    rollback/
    approval/
    observability/
    packaging/
    marketplace/
    evals/
    security/
    compliance/
    blueprints/
    profiles/

  registries/
  agents/
  skills/
  playbooks/
  lcps/
  mcps/
  packs/
  fixtures/
  templates/
  runbooks/
  docs/
```

## Execution Plane

```text
User Intent
  -> Kernel
  -> Profile Resolver
  -> Ecosystem Scanner
  -> LCP Resolver
  -> Playbook Planner
  -> Agent Runtime
  -> Skill Executor
  -> Tool Router
  -> MCP Gateway
  -> Evidence Store
  -> Judge
  -> Reports / Packages / PRs
```

## Control Plane

```text
Policy Engine
Permission Engine
Approval Gateway
Security Guardrails
Trust Policy
Compliance Layer
Evidence Integrity
Judge Layer
```

## Data Plane

```text
Project Files
Generated Artifacts
Evidence
Reports
Trace Logs
Metrics
Packages
Cache
Memory
Fixtures
```
