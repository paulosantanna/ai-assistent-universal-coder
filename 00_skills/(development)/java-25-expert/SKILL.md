---
name: java-25-expert
description: Build or migrate production Java 25 projects using only features/APIs verified for the repository toolchain and deployment runtime. Use when the user requests java 25 expert or invokes java-25-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 25 Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [migration.md](references/migration.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
