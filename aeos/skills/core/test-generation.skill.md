# Skill: Test Generation

## Mission

Analyze production code and generate test cases, test suites, and test infrastructure to improve coverage and reliability.

## Allowed Actions

- Read source files.
- Read existing test files.
- Detect testing frameworks in use.
- Generate test files in sandbox.
- Run test commands.
- Collect test results.
- Generate test coverage reports.

## Forbidden Actions

- Delete existing tests without evidence.
- Generate tests that always pass.
- Modify production code without associated test.
- Disable or skip failing tests.
- Commit incomplete test suites.

## Inputs

- workspace path
- target modules
- testing framework
- coverage threshold

## Outputs

- generated-tests/*.test.*
- test-coverage-report.md
- test-results.md
- test-gap-analysis.md

## Evidence Required

- source files analyzed
- existing tests analyzed
- test results before/after
- coverage metrics

## Quality Gates

- Generated tests must pass.
- Each test must assert a specific behavior.
- Must not reduce existing test coverage.
- Must follow existing test conventions.
- Must produce coverage report.
