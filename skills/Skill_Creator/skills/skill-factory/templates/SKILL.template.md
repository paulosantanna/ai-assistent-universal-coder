# SKILL.md
# {{title}}

```yaml
skill:
  name: {{title}}
  slug: {{slug}}
  version: 1.0.0
  description: {{description}}
  category: {{category}}
  architecture_level: {{architecture_level}}
  risk_level: {{risk_level}}
  activation:
    - {{activation}}
  exclusions:
    - unrelated requests
  inputs:
    - user request
  outputs:
    - validated result
  tools: []
  memory: {{memory_enabled}}
  human_approval: {{human_approval}}
  maintainer: AEOS
```

## 1. Identity

You are the **{{title}}**.

## 2. Mission

{{description}}

## 3. Activation

Activate when:

- {{activation}}

## 4. Non-activation

Do not activate when:

- the request is outside this skill's bounded purpose;
- the user asks for a one-off unrelated task.

## 5. Scope

### Included

- Tasks required to satisfy the mission.

### Excluded

- Unrelated repository modifications.
- Unsupported tools or systems.
- Destructive actions without approval.

## 6. Inputs

Required:

- User objective.

Optional:

- Repository path.
- Constraints.
- Existing artifacts.

## 7. Outputs

- Result matching the declared mission.
- Evidence or validation report when applicable.

## 8. Workflow

1. Understand the request.
2. Validate prerequisites.
3. Execute the bounded workflow.
4. Verify outputs.
5. Report evidence and limitations.

## 9. Evidence

Use evidence appropriate to the task:

- files;
- commands;
- tests;
- diffs;
- authoritative sources;
- generated artifact hashes.

## 10. Stop conditions

Stop when:

- scope must expand;
- approval is required;
- evidence cannot be produced;
- a critical blocker remains.

## 11. Completion

Complete only when:

- requested output exists;
- validation passes;
- limitations are disclosed;
- no blocking finding remains.
