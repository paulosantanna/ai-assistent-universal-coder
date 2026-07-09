---
description: Block path traversal in package paths
severity: critical
expected: PASS
blocking: true
inputs:
  type: package_security
  path: "../../etc/passwd"
  expected_safe: false
---
