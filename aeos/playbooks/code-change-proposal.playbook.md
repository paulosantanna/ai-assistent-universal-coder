# Playbook: code-change-proposal

## Objective

Execute the `code-change-proposal` operation under AEOS governance.

## Required Skills

- code-analyzer
- patch-planner
- test-generation
- security-audit

## Required MCPs

- filesystem-readonly
- git-readonly, when applicable
- filesystem-write-sandbox, when generating artifacts

## Required LCPs

- global-rules
- security-governance

## Steps

1. Load AEOS config.
2. Validate registries.
3. Resolve required LCPs.
4. Resolve required skills.
5. Resolve allowed MCPs.
6. Validate permissions.
1. Execute `code-analyzer` skill.
2. Execute `patch-planner` skill.
3. Execute `test-generation` skill.
4. Execute `security-audit` skill.
7. Collect evidence.
8. Generate reports.
9. Generate evidence manifest and hash-chain.
10. Run Judge.

## Blocking Conditions

- Missing evidence.
- Missing permission decision.
- Secret value exposure.
- Direct tool bypass.
- Hash mismatch.
- Output outside allowed scope.
- Unsupported claim.

## Outputs

- `.aeos/evidence/{execution_id}/`
- `.aeos/reports/{execution_id}/`
- `.aeos/sandbox/{execution_id}/`, when applicable
