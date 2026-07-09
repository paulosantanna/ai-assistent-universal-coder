# AEOS Ecosystem Schema

The `aeos.ecosystem.yaml` represents the target project ecosystem.

## Core Fields

```yaml
id:
name:
type:

workspace:
  mode:
  portability:

repos:
  - name:
    path:
    role:

environment:
  strategy:
  generate:

agents:
  root_agent:
  judge_agent:

skills:
  auto_generate:
  evolve_from_repo_analysis:

playbooks:
  auto_recommend:
  require_evidence:

guardrails:
  require_tests:
  require_rollback_plan:
  block_secret_leaks:

judge:
  enabled:
  min_score:
```
