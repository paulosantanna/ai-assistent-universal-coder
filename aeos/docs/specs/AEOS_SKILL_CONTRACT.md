# AEOS Skill Contract

## Definition

A skill is a reusable, versioned technical capability with explicit scope, actions, evidence requirements, forbidden actions, and quality gates.

## Required Fields

```yaml
skill:
  id:
  name:
  version:
  owner_agent:
  mission:
  scope:
  allowed_actions:
  forbidden_actions:
  required_capabilities:
  required_evidence:
  quality_gates:
  output_schema:
  blocking_conditions:
```

## Skill Rules

- Skills are not loose prompts.
- Skills must be registered before use.
- Skills must declare side effects.
- Skills must distinguish facts, assumptions, risks, and recommendations.
- Skills must not execute tools directly.
