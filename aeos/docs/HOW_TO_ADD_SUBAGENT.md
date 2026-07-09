# How to Add an AEOS Subagent

## Steps

1. Create `aeos/agents/subagents/<id>.subagent.md`.
2. Register it under `subagents` in agent registry.
3. Assign allowed parent roles.
4. Define output schema.
5. Define forbidden actions.
6. Add delegation policy rule.

## Subagent Constraints

Subagents:
- cannot use tools directly;
- cannot approve;
- cannot mutate files;
- cannot read secrets;
- cannot delegate further unless explicitly allowed;
- must return evidence_refs.
