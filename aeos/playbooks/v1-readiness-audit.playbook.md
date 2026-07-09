# Playbook: v1-readiness-audit

## Objective

Validate whether AEOS is ready for v1.0.

## Steps

1. Load v1 release gates.
2. Validate foundational documents.
3. Validate configs and registries.
4. Validate CLI command surface.
5. Validate security hardening.
6. Validate evidence and package verification.
7. Validate rollback and approval.
8. Validate Tool Router and MCP controls.
9. Validate Agent Runtime controls.
10. Generate v1 readiness report.
11. Run Judge.

## PASS Criteria

All v1 release gates must pass.

## Blocking Conditions

- any critical gate missing;
- no tests for policy blocking;
- evidence verify absent;
- package verify absent;
- secrets can be persisted;
- auto-merge enabled;
- auto-deploy enabled.
