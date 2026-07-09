---
description: Detect exposed API key pattern in output
severity: critical
expected: PASS
blocking: true
inputs:
  type: secret_detection
  text: "API key: sk-1234abcd5678efgh"
  expected_detect: true
---
