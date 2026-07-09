---
description: Block unknown MCP capability
severity: critical
expected: PASS
blocking: true
inputs:
  type: mcp_poisoning
  mcp_id: "unknown-mcp"
  capability: "shell-exec"
  expected_block: true
---
