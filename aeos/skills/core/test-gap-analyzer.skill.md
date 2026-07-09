# Test Gap Analyzer Skill

**ID:** test-gap-analyzer
**Version:** 1.0.0
**Owner Agent:** tester
**Risk Level:** low

## Mission
Analyze the gap between source code and test coverage — identifying untested modules, functions, and edge cases.

## Scope
- Read source files and existing test files
- Map code paths to test coverage
- Identify untested functions, branches, error paths

## Allowed Actions
- `filesystem.read` — read source and test files
- `generate_evidence` — register gap findings

## Forbidden Actions
- Modify test files or source files
- Run test commands
- Write test files directly (use test-writer skill)

## Required Capabilities
- READ_REPOSITORY
- ANALYZE_TEST_COVERAGE
- GENERATE_REPORT

## Required Evidence
- Source files analyzed (paths with SHA-256)
- Test files analyzed (paths with SHA-256)
- Gap analysis report

## Quality Gates
- Each gap must cite specific source line numbers
- Untested claims must be verifiable by file inspection

## Output Schema
```json
{
  "total_functions": 100,
  "tested_functions": 65,
  "untested_functions": [{"file": "src/service.py", "function": "calculate", "line": 42}],
  "coverage_pct": 65.0,
  "high_risk_gaps": [{"file": "src/auth.py", "function": "validate_token", "reason": "Security critical"}]
}
```

## Blocking Conditions
- Gap claims without source citations
- Attempts to modify test files