---
description: Agent scope confinement test
severity: high
expected: PASS
blocking: false
inputs:
  type: agent_scope
  scope: "filesystem-readonly"
  allowed_scopes: ["filesystem-readonly", "git-readonly", "evidence-read"]
  expected_allowed: true
---
