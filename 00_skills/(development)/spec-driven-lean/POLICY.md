# Spec-Driven Lean Policy

## Risk classes

- read_only: inspect existing `.specs/` artifacts.
- low: write `plan.md` / `checks.md` without repository mutation.
- medium: local build against approved checks.
- high: commits, test mutation, one-way doors.
- destructive: push, deploy, production data change — explicit per-action approval.

## Profile policy

Default profile is `light` unless the user raises it. `validate_verification.py` must match the approved checks profile.

## Workflow policy

Plan is reviewed before checks. Checks are reviewed before build. The builder does not write `verification.md`. `VerifierLens` is never optional after the last commit of the feature.

## Commit policy

Local commits apply only after explicit user authorization. Never weaken a check or test to pass a gate.

## Security policy

Do not persist secrets in `.specs/`, evidence, notebook or chat.
