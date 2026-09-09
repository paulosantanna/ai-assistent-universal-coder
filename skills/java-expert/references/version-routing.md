# Version routing

Entry: `pom.xml`, `build.gradle*`, toolchain files, container image, CI runtime.

- Java 17 → `skills/java-17-expert/` + `docs-java-17`.
- Java 21 → `skills/java-21-expert/` + `docs-java-21`.
- Java 25 → `skills/java-25-expert/` + `docs-java-25`.
- Java 26 → `skills/java-26-expert/` + `docs-java-26`.
- Mixed source/runtime → stop and map compatibility before code changes.
- Framework compatibility is independent of language syntax compatibility; verify both.
