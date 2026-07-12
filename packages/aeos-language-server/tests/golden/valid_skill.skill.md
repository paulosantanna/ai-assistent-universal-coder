---
$schema: "https://aeos.ai/schemas/skill.schema.json"
$id: "skill-quality-gate"
name: "Quality Gate Skill"
version: "1.0.0"
description: "Evaluates code quality metrics against configurable thresholds and determines whether code meets quality standards for merge."
author: "AEOS LSP Team"
tools:
  - name: "evaluate-metrics"
    tool_type: "custom"
    description: "Evaluate code metrics against quality thresholds"
    config:
      thresholds:
        maintainability: 70
        test_coverage: 80
        duplication: 5
        complexity: 20
  - name: "check-coverage"
    tool_type: "bash"
    description: "Check test coverage percentage from coverage reports"
    config:
      command_template: "node scripts/check-coverage.js --input {{input.coverage_path}} --threshold {{input.min_coverage}}"
dependencies:
  packages:
    - name: "typescript"
      version: ">=5.3.0"
      manager: "npm"
timeout: 30000
retry:
  max_attempts: 2
  delay_ms: 1000
inputs:
  type: object
  required:
    - coverage_path
    - min_coverage
  properties:
    coverage_path:
      type: string
      description: "Path to the coverage report file"
    min_coverage:
      type: number
      description: "Minimum acceptable coverage percentage"
      minimum: 0
      maximum: 100
    allow_low_complexity:
      type: boolean
      description: "Skip complexity check"
      default: false
outputs:
  type: object
  description: "Quality gate evaluation result"
  properties:
    passed:
      type: boolean
    score:
      type: number
    details:
      type: object
---

# Quality Gate Skill

Evaluates code quality metrics against thresholds and determines
whether the code meets the quality bar for merging.

## Metrics Evaluated

- **Maintainability Index**: Target >= 70
- **Test Coverage**: Target >= 80%
- **Code Duplication**: Target < 5%
- **Cyclomatic Complexity**: Target <= 20

## Usage

Referenced by playbooks and agents that need to enforce quality gates
before merging code changes.
