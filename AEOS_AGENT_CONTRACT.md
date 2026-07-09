# AEOS Agent Contract

## Agent Definition

An AEOS agent is a specialized executor with a mission, scope, capabilities, limits, context requirements, tool permissions, and quality gates.

## Required Fields

```yaml
agent:
  id:
  name:
  version:
  type:
  mission:
  allowed_capabilities:
  forbidden_actions:
  required_lcps:
  allowed_skills:
  allowed_mcps:
  approval_required_for:
  evidence_required:
  quality_gates:
  escalation_rules:
```

## Rules

- An agent must not approve its own work.
- The Judge Agent must be independent from the implementing agent.
- Agents cannot bypass Policy Engine or Permission Engine.
- Agents cannot persist secrets.
- Agents cannot change architecture without ADR or approval.
