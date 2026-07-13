# AEOS Kernel

## Purpose

The Kernel is the operational control plane of AEOS.

It does not implement business logic. It coordinates controlled execution.

## Services

```text
KernelRuntime
ConfigLoader
SchemaValidator
RegistryLoader
ContextService
LCPResolver
PermissionEngine
PolicyEngine
ToolRouter
MCPRegistry
SkillExecutor
PlaybookEngine
EvidenceStore
JudgeGateway
AuditLogger
RollbackManager
ApprovalGateway
PackagingLayer
```

## Execution Order

1. Load `aeos/config/aeos.config.yaml`.
2. Validate config schemas.
3. Load capabilities, permissions, and policies.
4. Load registries.
5. Resolve playbook.
6. Resolve required agents.
7. Resolve required skills.
8. Resolve required LCPs.
9. Resolve allowed MCPs.
10. Create `execution_id`.
11. Create evidence directory.
12. Run dry-run.
13. Validate permission and policy decisions.
14. Execute approved steps.
15. Collect evidence.
16. Validate evidence integrity.
17. Run deterministic Judge.
18. Generate final report.
19. Block or pass.

## Kernel Rule

Agents never access tools directly. Agents request capabilities. The Kernel decides whether a capability can become an action.
