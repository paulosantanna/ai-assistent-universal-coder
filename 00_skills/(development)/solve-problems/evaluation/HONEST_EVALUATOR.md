# HONEST_EVALUATOR.md

## Proposal Verdict

Return `PASS`, `REVIEW` or `BLOCKED`.

## Required Checks

- Root cause has direct evidence.
- Affected language is identified from repository evidence.
- Proposal preserves architecture and package structure.
- Proposal does not add comments to source code.
- Proposal does not introduce unused imports, orphan variables, dead assignments or unused files.
- Proposal is smaller and simpler than rejected alternatives.
- Tests include reproduction or deterministic equivalent when possible.
- Verification commands are repository-native.
- Residual risk is explicit.

## Blockers

Return `BLOCKED` when any non-negotiable rule is violated, required evidence is missing, verification cannot run without approved risk deferral, or the proposal relies on confidence instead of evidence.
