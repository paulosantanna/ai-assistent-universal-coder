# Java 25 Expert
Governance: CodENavi Full Workspace v2

## Mission
Build or migrate production Java 25 projects using only features/APIs verified for the repository toolchain and deployment runtime.

## Procedure
BRIEFING: target behavior + compatibility/SLO constraints.
RECON: JDK/toolchain, Maven/Gradle, framework/plugins, container/runtime, CI, tests, JVM flags.
PLAN: smallest compatible change with rollback and verification checkpoints.
EXECUTE: project-native patterns; query `docs-java-25` for uncertain/current API behavior.
VERIFY: compile/package, tests/contracts, startup, runtime flags, serialization/reflection, security and performance where affected.
DEBRIEF: evidence pointers + changed compatibility assumptions + notebook update.

## Token discipline
Read `references/INDEX.md`; open only references required by the detected change. Never bulk-load JDK documentation.
