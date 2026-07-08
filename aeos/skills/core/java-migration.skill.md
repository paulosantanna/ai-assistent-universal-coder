# Skill: Java Migration

## Mission

Analyze Java projects and perform version migrations, API replacements, and build configuration updates.

## Allowed Actions

- Read Java source files.
- Read build configuration (pom.xml, build.gradle).
- Read module descriptors.
- Detect deprecated APIs and suggest replacements.
- Apply code transformations within sandbox.
- Run build commands.
- Run test suites.
- Generate migration reports.

## Forbidden Actions

- Delete modules without evidence.
- Change public API without contract test.
- Upgrade major dependencies without compatibility check.
- Commit directly to main branch.
- Merge pull requests without approval.
- Deploy without approval.

## Inputs

- workspace path
- source Java version
- target Java version
- migration scope

## Outputs

- migration-report.md
- compatibility-report.md
- changed-files.md
- test-results.md

## Evidence Required

- dependency tree before/after
- build results
- test results
- changed files diff
- rollback plan

## Quality Gates

- Must pass full test suite.
- Must not break public API without contract tests.
- Must document every change.
- Must verify build after migration.
- Must produce rollback plan.
