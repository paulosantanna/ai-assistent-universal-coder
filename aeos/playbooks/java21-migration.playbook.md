# Playbook: Java 21 Migration

## Objective

Migrate a Java codebase from an older Java version to Java 21, ensuring compatibility, test coverage, and security validation.

## Preconditions

- Workspace path exists.
- Java source files detected.
- Build tool detected (Maven/Gradle).
- MCPs for filesystem read/write, git, shell, and test runner available.
- LCPs for global rules, java-backend, and security-governance loaded.

## Agents

- Root Agent
- Architect Agent
- Coder Agent
- Tester Agent
- Security Agent
- Judge Agent

## Skills

- java-migration
- test-generation
- security-audit

## MCPs

- filesystem-readonly
- filesystem-write-sandbox
- git-readonly
- git-write-branch
- shell-controlled
- test-runner

## Steps

1. Load project context and Java-specific LCPs.
2. Detect current Java version and build configuration.
3. Analyze dependencies for Java 21 compatibility.
4. Identify deprecated APIs and migration candidates.
5. Create feature branch for migration.
6. Update build configuration (pom.xml / build.gradle).
7. Apply Java 21 syntax and API migrations.
8. Record module and test results as evidence.
9. Run full test suite.
10. Generate migration report.
11. Send outputs to Judge Agent.
12. Generate judge-report.md.

## Blocking Conditions

- Build fails after migration.
- Tests fail or are missing.
- Public API changed without contract test.
- Security scan detects new vulnerabilities.
- Rollback plan not defined.

## Outputs

- .aeos/migration-report.md
- .aeos/compatibility-report.md
- .aeos/test-results.md
- .aeos/security-scan.md
- .aeos/judge-report.md
