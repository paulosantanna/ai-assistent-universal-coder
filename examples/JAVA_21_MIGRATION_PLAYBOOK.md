# Example — Java 21 Migration Playbook

## Objective

Upgrade a Java project to Java 21 safely.

## Steps

1. Detect build tool.
2. Detect current Java version.
3. Detect framework compatibility.
4. Read migration guides.
5. Update toolchain.
6. Update Docker/CI.
7. Fix deprecated APIs.
8. Run tests.
9. Run security/dependency checks.
10. Write ADR.
11. Judge.

## Required evidence

- `pom.xml` or `build.gradle`
- CI workflow
- Dockerfile
- test output
- dependency compatibility output
- migration ADR
