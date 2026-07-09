---
description: Prevent cache poisoning attack
severity: high
expected: PASS
blocking: false
inputs:
  type: permission
  action: cache-write
  capability: evidence-cache
  expected_allowed: false
---
