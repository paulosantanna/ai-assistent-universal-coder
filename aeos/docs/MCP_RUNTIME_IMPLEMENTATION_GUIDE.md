# MCP Runtime Implementation Guide

## Minimum Vertical Slice

Implement these first:

```text
aeos run mcp-health-check --target <path>
aeos run mcp-discovery --target <path>
aeos run tool-router-audit --target <path>
```

## Implementation Order

1. Load `aeos/config/mcp.runtime.yaml`.
2. Load `aeos/config/tool-router.config.yaml`.
3. Load `aeos/config/mcp-tools.allowlist.yaml`.
4. Load `aeos/registries/mcps.registry.yaml`.
5. Validate MCP configs.
6. Implement MCPRegistry.
7. Implement MCPRuntime health check.
8. Implement ToolRouter call skeleton.
9. Wire PermissionEngine.
10. Wire PolicyEngine.
11. Wire EvidenceStore.
12. Add Judge v6 checks.

## Do Not Implement Yet

- secrets runtime real;
- browser login;
- database write;
- deploy;
- push/merge;
- shell unrestricted.
