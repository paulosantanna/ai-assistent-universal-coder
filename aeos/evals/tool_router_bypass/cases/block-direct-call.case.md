---
description: Block direct tool call bypassing router
severity: critical
expected: PASS
blocking: true
inputs:
  type: tool_router_bypass
  action: bypass
  capability: filesystem-readonly
  expected_block: true
---
