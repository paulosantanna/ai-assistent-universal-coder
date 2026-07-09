# Playbook: subagent-risk-review

## Objective

Audit subagent outputs for scope violations, unsupported claims, missing evidence, and unsafe recommendations.

## Steps

1. Load subagent outputs.
2. Validate output schema.
3. Validate evidence refs.
4. Validate no raw secrets.
5. Validate no scope expansion.
6. Validate no forbidden recommendations.
7. Generate risk review.
8. Run Judge.

## Blocking Conditions

- unsupported facts;
- missing evidence;
- scope violation;
- raw secret;
- recommendation for forbidden action;
- self-approval.
