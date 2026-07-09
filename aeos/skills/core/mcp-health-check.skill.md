# Skill: mcp-health-check

## Mission

Validate MCP runtime health, state, tools, capabilities and security posture.

## Allowed Actions

- Read MCP registries.
- Read MCP config files.
- Request health check through Tool Router.
- Generate reports.

## Forbidden Actions

- Invoke risky tools.
- Start critical MCPs.
- Read secrets.
- Execute shell.
- Bypass Tool Router.

## Required Evidence

- MCP registry snapshot.
- MCP config snapshot.
- Health result.
- Tool allowlist validation.
- Judge report.

## Quality Gates

- Every enabled MCP has a health result.
- Every exposed tool is allowlisted.
- Critical MCPs are disabled by default.
