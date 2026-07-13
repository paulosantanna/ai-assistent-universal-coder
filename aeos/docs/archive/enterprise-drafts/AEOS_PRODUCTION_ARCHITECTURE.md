# AEOS Production Architecture

## Reference Architecture

```text
AEOS CLI / Desktop / API
        |
Kernel Runtime
        |
+----------------------+----------------------+------------------+
| Policy Engine        | Permission Engine    | Approval Gateway |
+----------------------+----------------------+------------------+
        |
Playbook Engine -> Agent Runtime -> Skill Engine
        |
Tool Router
        |
MCP Gateway
        |
Filesystem / Git / Test Runner / Package / CI / Observability
        |
Evidence Store -> Judge -> Reports -> Packages -> PR
```

## Production Modules

```text
aeos/core/kernel
aeos/core/policy
aeos/core/permissions
aeos/core/approval
aeos/core/tool_router
aeos/core/mcp_runtime
aeos/core/agent_runtime
aeos/core/playbook_engine
aeos/core/skill_engine
aeos/core/evidence
aeos/core/judge
aeos/core/observability
aeos/core/performance
aeos/core/security
aeos/core/supply_chain
aeos/core/compliance
aeos/core/release
```

## Deployment Modes

```text
local-dev
enterprise-workstation
devcontainer
ci-runner
controlled-cloud-runner
airgapped-review
```

## Strict Rule

AEOS must never require production secrets to produce analysis, documentation, patches, tests, review packages, or readiness reports.
