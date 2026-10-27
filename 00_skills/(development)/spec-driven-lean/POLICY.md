# Spec-Driven Lean Policy

## Risk classes

- read_only: inspect existing `.specs/` artifacts.
- low: write `plan.md` / `checks.md` without repository mutation.
- medium: local build against approved checks.
- high: commits, test mutation, one-way doors.
- destructive: push, deploy, production data change — explicit per-action approval.

## Mutation policy

Default mutation count is 3, declared in checks.md; coverage remains owed at every count. `check_proofs.py` and `validate_verification.py` settle the executable evidence.

## Workflow policy

Plan is reviewed before checks. Frozen checks govern build. VerifierLens and screen review are sequential internal lenses; follow the fresh-session fallback and disclose `self-verified`. Never claim independent author/verifier identities.

## Commit policy

Local commits apply only after explicit user authorization. Never weaken a check or test to pass a gate.

## Security policy

Do not persist secrets in `.specs/`, evidence, notebook or chat.
