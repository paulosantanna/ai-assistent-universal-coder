# Skill: java-version-expert
Governance: CodENavi v1

## Mission
Analyze and modify Java code with version-aware semantics for Java 8, 11, 17 and 21 without silently introducing APIs or language features unavailable to the declared target.

## Profiles
- Java 8: no modules, records, text blocks, var, sealed classes or virtual threads; prefer APIs available in Java 8.
- Java 11: allow Java 9–11 APIs/features only when project source/target permits them.
- Java 17: treat Java 17 LTS behavior as baseline when project explicitly targets 17; verify framework compatibility.
- Java 21: use Java 21 language/runtime features only when source/target/toolchain and production runtime are verified.

## Workflow
Recon `pom.xml`/Gradle/toolchains/runtime/container, framework versions and CI matrix before suggesting code.
Verify current JDK/framework APIs from authoritative docs when signatures or behavior matter.
Preserve repository conventions; do not modernize syntax merely because a newer JDK exists.
For migrations, provide compatibility findings, staged plan, tests and rollback.
