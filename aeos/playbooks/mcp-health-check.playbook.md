# Playbook: mcp-health-check

## Objective

Validate registered MCPs without executing risky operations.

## Required Skills

- mcp-health-check
- security-audit

## Required MCPs

- filesystem-readonly
- git-readonly
- test-runner-controlled
- package-local

## Steps

1. Load MCP registry.
2. Validate MCP config files.
3. Validate enabled status.
4. Validate allowed tools.
5. Run health check for each enabled MCP.
6. Generate MCP health report.
7. Generate evidence manifest.
8. Run Judge.

## Blocking Conditions

- MCP config missing.
- MCP exposes tool not in allowlist.
- Critical MCP enabled without explicit policy.
- Tool Router bypass detected.
