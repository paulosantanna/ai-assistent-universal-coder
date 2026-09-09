# Java verification

Baseline before migration: compile/package, unit/integration/contract tests, startup, critical endpoint/message flows, JVM flags, serialization, reflection, native/JNI, performance baseline.

After change: repeat comparable checks; inspect illegal reflective access/removal, dependency/plugin support, container JRE, CI toolchain and observability. Roll back if contract behavior or required SLO regresses without accepted trade-off.
