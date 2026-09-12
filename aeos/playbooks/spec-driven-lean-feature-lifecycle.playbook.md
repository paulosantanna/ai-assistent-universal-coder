# Playbook: spec-driven-lean-feature-lifecycle

## Required agent

- `codenavi-agent` only.

## Required skills

- `spec-driven-lean`
- `specs` as AEOS mutating preflight when artifacts will be created or altered

## Required LCPs

- `global-rules`
- `spec-driven-development`
- `security-governance`

## Flow

1. Read continuity quartet and `.specs/STATE.md` if present.
2. Confirm verification profile (`light` default, or user-raised `standard`/`ui`).
3. Write `plan.md` and run `skills/spec-driven-lean/scripts/validate_plan.py`. Stop for human review.
4. Derive `checks.md` and run `validate_checks.py`. Stop for human review.
5. Build from checks, not from the implementation. Commits only with explicit user authorization.
6. Dispatch `VerifierLens` over `<feature base>..HEAD`; the builder does not write `verification.md`.
7. Run `validate_verification.py` before declaring done.

## Failure policy

A check without proof, a profile mismatch, an author-written verification report or a surviving mutant blocks completion.
