---
$schema: "https://aeos.ai/schemas/agent.schema.json"
$id: "full-analysis-agent"
name: "Full Analysis Agent"
version: "2.0.0"
description: "Comprehensive analysis agent that performs deep code inspection, security scanning, architecture mapping, and generates structured reports with evidence."
author: "AEOS LSP Team"
capabilities:
  - READ_REPOSITORY
  - READ_FILES
  - ANALYZE_CODE
  - MAP_ARCHITECTURE
  - SCAN_SECRETS
  - SCAN_PERMISSIONS
  - GENERATE_REPORT
  - VERIFY_EVIDENCE
skills:
  - "skill-analyzer"
  - "skill-reporter"
  - "skill-quality-gate"
  - "skill-security-scanner"
  - "skill-arch-mapper"
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
        - "data-classification-policy"
  - name: "observability"
    provider: "aeos.observability.default"
    config:
      enable_tracing: true
      enable_logging: true
      log_level: "debug"
  - name: "evidence"
    provider: "aeos.evidence.collector"
    config:
      hash_required: true
      chain_to_previous: true
model_preferences:
  provider: "anthropic"
  model: "claude-sonnet-4-20250514"
  context_window: 200000
  max_tokens: 16384
  profile: "default-performance"
delegation_policy:
  strategy: "capability-match"
  max_depth: 3
  allowed_sub_agents:
    - "code-review-agent"
    - "architect-agent"
    - "security-agent"
  require_approval: false
parent: "root-agent"
stop_conditions:
  - type: max_iterations
    value: 100
  - type: max_tokens
    value: 500000
  - type: max_time
    value: 3600000
  - type: success
  - type: error
  - type: approval_denied
  - type: human_interrupt
config:
  log_level: "debug"
  cache_enabled: true
  cache_ttl_seconds: 3600
  max_concurrent_analyses: 4
  report_format: "markdown"
---

# Full Analysis Agent

## Overview

The Full Analysis Agent is the most comprehensive analysis agent in the
AEOS workspace. It combines code analysis, security scanning, architecture
mapping, and reporting into a single coordinated agent with evidence
collection at every step.

## Capabilities

| Capability | Description |
|---|---|
| `READ_REPOSITORY` | Full read access to workspace files |
| `ANALYZE_CODE` | Deep static analysis of source code |
| `MAP_ARCHITECTURE` | Detect and document architecture patterns |
| `SCAN_SECRETS` | Identify potential secrets and credentials |
| `SCAN_PERMISSIONS` | Audit permission configurations |
| `GENERATE_REPORT` | Produce comprehensive analysis reports |
| `VERIFY_EVIDENCE` | Validate evidence integrity and completeness |

## Delegation Chain

```
root-agent
  -> full-analysis-agent
       -> code-review-agent
       -> architect-agent
       -> security-agent
```

## Usage

```yaml
agent: full-analysis-agent
inputs:
  path: "/workspace/src"
  recursive: true
  max_depth: 10
  security_scan: true
  architecture_map: true
```

## Evidence

All actions produce verifiable evidence records with cryptographic hashes
chained to the previous record for tamper detection.
