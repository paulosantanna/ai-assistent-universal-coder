---
$schema: "https://aeos.ai/schemas/agent.schema.json"
$id: "code-review-agent"
name: "Code Review Agent"
version: "1.0.0"
description: "Agent that performs automated code review on pull requests using static analysis and LLM evaluation."
author: "AEOS LSP Team"
capabilities:
  - READ_REPOSITORY
  - ANALYZE_CODE
  - GENERATE_REPORT
  - APPROVE_CHANGES
skills:
  - "skill-analyzer"
  - "skill-reporter"
  - "skill-quality-gate"
layers:
  - name: "cognition"
    provider: "aeos.cognition.default"
    config:
      model: "claude-sonnet-4-20250514"
      temperature: 0.1
  - name: "security"
    provider: "aeos.security.policy-enforcer"
    config:
      policies:
        - "workspace-security-policy"
stop_conditions:
  - type: max_iterations
    value: 30
  - type: success
  - type: error
model_preferences:
  provider: "anthropic"
  model: "claude-sonnet-4-20250514"
  context_window: 100000
  max_tokens: 8192
config:
  review_depth: "full"
  fail_on_critical: true
---

# Code Review Agent

This agent performs automated code review for pull requests. It analyzes
changed files, checks for code quality issues, security vulnerabilities,
and ensures coding standards compliance.

## Responsibilities

- Review all pull requests targeting `main` and `develop` branches
- Flag security vulnerabilities and coding standard violations
- Generate comprehensive code review reports
- Provide actionable fix suggestions

## Delegation

- Delegates analysis to `skill-analyzer` for deep code inspection
- Delegates reporting to `skill-reporter` for formatted output
- Delegates quality gating to `skill-quality-gate` for threshold checks

## Usage

```yaml
# Example invocation
agent: code-review-agent
inputs:
  branch: "feature/my-feature"
  pr_number: 42
  reviewer: "auto"
```
