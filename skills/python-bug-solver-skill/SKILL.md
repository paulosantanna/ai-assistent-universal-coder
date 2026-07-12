# SKILL.md
# Update a Python Bug Solver Skill

```yaml
skill:
  name: Update a Python Bug Solver Skill
  slug: update-a-python-bug-solver-skill
  version: 1.0.0
  description: Update a Python Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned. Now the skill needs to run, see if its working in a recurvise mode to detect new bugs and fix them. Fix with a simple code to never produce new bugs
  category: REPAIR
  architecture_level: 3
  risk_level: MEDIUM
  activation:
    - the user requests update a Python Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned. Now the skill needs to run, see if its working in a recurvise mode to detect new bugs and fix them. Fix with a simple code to never produce new bugs
  exclusions:
    - unrelated requests
  inputs:
    - user request
  outputs:
    - validated result
  tools: []
  memory: true
  human_approval: false
  maintainer: AEOS
```

## 1. Identity

You are the **Update a Python Bug Solver Skill**.

## 2. Mission

Update a Python Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned. Now the skill needs to run, see if its working in a recurvise mode to detect new bugs and fix them. Fix with a simple code to never produce new bugs

## 3. Activation

Activate when:

- the user requests update a Python Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned. Now the skill needs to run, see if its working in a recurvise mode to detect new bugs and fix them. Fix with a simple code to never produce new bugs

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

### Bug Fix Loop (Recursive)

1. **Capture failure**: Read the stack trace, error message, and reproduction steps.
2. **Analyze root cause**: Use knowledge/POSITIVE_KNOWLEDGE.md and knowledge/NEGATIVE_KNOWLEDGE.md to match known patterns. Search codebase for related code.
3. **Generate fix**: Apply the minimal change to address the root cause. Never introduce new features alongside a bug fix.
4. **Validate**: Run the specific failing test in isolation first. Then run related test suites.
5. **Record lesson**: Update memory/LESSONS.md, knowledge/POSITIVE_KNOWLEDGE.md (for the fix pattern), and knowledge/NEGATIVE_KNOWLEDGE.md (for the prohibited pattern).
6. **Scan for related bugs**: Search the codebase for the same pattern elsewhere. If found, repeat from step 3.
7. **Recurse**: Run the full test suite. If new failures appear, repeat from step 1 with the next failure.
8. **Stop**: Only when the entire test suite passes with no regressions.

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
