# How to Add an MCP to AEOS

## Steps

1. Create `aeos/mcps/<id>.mcp.yaml`.
2. Add MCP to `aeos/registries/mcps.registry.yaml`.
3. Add tools to `aeos/config/mcp-tools.allowlist.yaml`.
4. Add policies if needed.
5. Add required capabilities.
6. Add tests for permission and policy blocking.
7. Add Judge validation.

## Required Security Review

Every MCP must answer:

- What tools does it expose?
- What capabilities do they require?
- Can it write?
- Can it delete?
- Can it access secrets?
- Can it access network?
- Can it mutate production?
- What evidence is generated?
- What blocks it?

## Forbidden by Default

- secrets runtime;
- browser authenticated;
- database write;
- deploy;
- unrestricted shell;
- push/merge/force push.
