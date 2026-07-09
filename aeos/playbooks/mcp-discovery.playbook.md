# Playbook: mcp-discovery

## Objective

Discover MCP capabilities and compare them against AEOS allowlists.

## Outputs

- `.aeos/reports/{execution_id}/mcp-discovery-report.md`
- `.aeos/evidence/{execution_id}/mcp-discovery.json`
- `.aeos/evidence/{execution_id}/tool-allowlist-validation.json`

## Blocking Conditions

- Unknown tool exposed.
- Tool requires forbidden capability.
- Critical capability enabled by default.
- Missing evidence.
