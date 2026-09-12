# Playbook: spec-driven-feature-lifecycle

## Required agent

- `codenavi-agent` only.

## Required skills

- `spec-driven`
- `specs` as AEOS mutating preflight when artifacts will be created or altered

## Required LCPs

- `global-rules`
- `spec-driven-development`
- `security-governance`

## Flow

1. Read continuity quartet and `.specs/STATE.md` if present.
2. Size the feature (small/medium/large/complex) and activate only the needed phases.
3. Specify with EARS acceptance criteria; run `skills/spec-driven/scripts/validate_spec.py`.
4. Design and tasks only when sizing requires them; validate tasks before approval.
5. Implement locally against the approved spec. Commits only with explicit user authorization.
6. Run `VerifierLens` after the last task; the implementer does not write `validation.md`.
7. Run `validate_state.py` before declaring done.
8. Promote only verified durable facts into `.notebook/MEMORY.md`.

## Failure policy

A failed structural gate, failed test gate or evidence-free validation report blocks completion. Do not weaken tests to proceed.
