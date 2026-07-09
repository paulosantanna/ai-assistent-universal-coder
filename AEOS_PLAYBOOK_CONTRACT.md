# AEOS Playbook Contract

## Definition

A playbook is a governed operational procedure that orchestrates skills, agents, MCPs, LCPs, policies, approvals, evidence, and Judge validation.

## Required Fields

```yaml
playbook:
  id:
  name:
  version:
  objective:
  preconditions:
  required_agents:
  required_skills:
  required_lcps:
  allowed_mcps:
  steps:
  blocking_conditions:
  required_evidence:
  rollback_strategy:
  judge_requirements:
```

## Playbook State Machine

```text
PENDING
VALIDATING_CONFIG
RESOLVING_PLAYBOOK
RESOLVING_CONTEXT
CHECKING_PERMISSIONS
DRY_RUN
WAITING_APPROVAL
EXECUTING
COLLECTING_EVIDENCE
JUDGING
PASSED
BLOCKED
FAILED
ROLLED_BACK
```
