---
name: java-25-expert
description: "Build or migrate Java 25 projects using only APIs verified for toolchain and runtime. Use for Java 25 work. Do NOT use for other languages."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 25 Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [migration.md](references/migration.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
