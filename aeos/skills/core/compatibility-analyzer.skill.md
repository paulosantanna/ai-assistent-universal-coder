# Compatibility Analyzer Skill

**ID:** compatibility-analyzer
**Version:** 1.0.0
**Owner Agent:** architect
**Risk Level:** medium

## Mission
Analyze dependency compatibility — version conflicts, peer dependency issues, platform constraints, breaking change risk.

## Scope
- Parse dependency version constraints
- Detect peer dependency mismatches
- Assess platform and OS compatibility
- Classify breaking change risk (patch/minor/major)

## Allowed Actions
- `filesystem.read` — read dependency files
- `generate_evidence` — register findings

## Forbidden Actions
- Update version constraints
- Install packages to resolve conflicts
- Run compatibility tooling that modifies files

## Required Capabilities
- READ_REPOSITORY
- ANALYZE_COMPATIBILITY
- GENERATE_REPORT

## Required Evidence
- Dependency files read (SHA-256)
- Compatibility matrix
- Conflict report

## Quality Gates
- Every compatibility claim must cite source lines
- Breaking change risk must specify reason
- Matrix must be complete for all direct dependencies

## Output Schema
```json
{
  "compatibility_matrix": [
    {"dep": "react", "current": "18.2.0", "peer_required": ">=17", "compatible": true, "risk": "low"},
    {"dep": "typescript", "current": "5.0.0", "peer_required": ">=4.5", "compatible": true, "risk": "low"}
  ],
  "conflicts": [],
  "platform_issues": [],
  "breaking_change_risks": []
}
```

## Blocking Conditions
- Compatibility analysis is missing a required dependency
- Attempt to modify dependency files