# AEOS Task Delegation Contract

## Definition

A delegated task is a scoped unit of work assigned to an agent or subagent, with required context, allowed skills, allowed MCPs, expected outputs, and blocking conditions.

## Task Definition

```yaml
task:
  id:
  execution_id:
  parent_task_id:
  assigned_agent:
  objective:
  scope:
  allowed_skills:
  allowed_capabilities:
  allowed_mcps:
  required_lcps:
  required_context:
  required_evidence:
  expected_outputs:
  forbidden_actions:
  quality_gates:
  escalation_rules:
  status:
```

## Delegation Rules

- The Root Agent may delegate.
- Planner Agent may propose delegation.
- Security Agent may block delegation.
- Judge Agent validates final delegated outputs.
- No task can grant capabilities beyond the assigned agent role.
- No subagent can expand its own scope.
- No subagent can delegate further unless explicitly allowed.

## Escalation Required When

- task requires approval;
- risk is high or critical;
- evidence is insufficient;
- tool permission denied;
- agent detects architectural impact;
- security issue detected;
- conflicting agent outputs exist.
