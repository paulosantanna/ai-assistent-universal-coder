# Playbook: documentation-generation

## Objective

Execute the `documentation-generation` operation under AEOS governance.

## Required Skills

- repo-scanner
- architecture-mapper
- documentation

## Required MCPs

- filesystem-readonly
- git-readonly, when applicable
- filesystem-write-sandbox, when generating artifacts
- complete-docs, when generating complete architecture, Mermaid diagrams, ADRs or cloud readiness packages

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
7. Execute `repo-scanner` skill.
8. Execute `architecture-mapper` skill.
9. Execute `documentation` skill.
10. Request `docs.architecture_package` when complete architecture or cloud maturity documentation is required.
11. Validate all Mermaid blocks before publishing generated artifacts.
12. Collect evidence.
13. Generate reports.
14. Generate evidence manifest and hash-chain.
15. Run Judge.

## Blocking Conditions

- Missing evidence.
- Missing permission decision.
- Secret value exposure.
- Direct tool bypass.
- Hash mismatch.
- Output outside allowed scope.
- Unsupported claim.
- Missing Mermaid validation for complete architecture documentation.
- Missing cloud readiness evidence when deployment maturity is requested.

## Outputs

- `.aeos/evidence/{execution_id}/`
- `.aeos/reports/{execution_id}/`
- `.aeos/sandbox/{execution_id}/`, when applicable
- `README.md`, `docs/ARCHITECTURE.md`, `docs/RUNTIME_FLOW.md`, `docs/SKILLS_MCPS_LSPS.md`, `docs/CLOUD_READINESS.md` and ADR candidates inside the approved sandbox/report output when complete architecture packaging is requested
