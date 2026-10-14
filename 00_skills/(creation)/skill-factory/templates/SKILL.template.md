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
- Structured facts, assumptions, risks, recommendations and blocking conditions when applicable.

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

## 10. Prompt contract

Follow the AEOS prompt contract:

- state the objective, scope, assumptions and constraints before execution;
- use evidence-backed facts only;
- route tool access through approved command, MCP or Tool Router paths;
- redact secrets, credentials, tokens and sensitive values;
- return facts, assumptions, risks, recommendations, evidence refs and blocking conditions;
- keep execution bounded by permissions, policy, risk profile and requested target.

## 11. Agent knowledge layers

Use the generated Agent and knowledge files as layered context:

- `AGENT.md` defines the operating role, loading order and execution rules.
- `knowledge/NEGATIVE_KNOWLEDGE.md` blocks repeated failures and unsafe shortcuts.
- `knowledge/POSITIVE_KNOWLEDGE.md` captures validated successful patterns.
- `knowledge/KNOWLEDGE.md` stores promoted domain knowledge only after evidence.
- `memory/OPEN_RISKS.md`, `memory/DECISIONS.md` and `memory/FAILURES.md` preserve operational memory.
- `knowledge/KNOWLEDGE_PROMOTION.md` governs when observations become reusable knowledge.

## 12. Honest evaluator

Before completion, apply `evaluation/HONEST_EVALUATOR.md`.

The evaluator must be extremely honest:

- reject unsupported confidence;
- mark missing evidence as a blocker;
- separate useful partial results from completed work;
- return `PASS`, `REVIEW` or `BLOCKED`;
- prefer an uncomfortable true limitation over a pleasing but false completion claim.

## 13. Stop conditions

Stop when:

- scope must expand;
- approval is required;
- evidence cannot be produced;
- a critical blocker remains.
- the honest evaluator returns `BLOCKED`.

## 14. Completion

Complete only when:

- requested output exists;
- validation passes;
- limitations are disclosed;
- no blocking finding remains;
- the honest evaluator verdict is `PASS` or explicitly disclosed as `REVIEW`.
