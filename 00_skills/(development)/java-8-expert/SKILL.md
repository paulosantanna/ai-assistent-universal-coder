---
name: java-8-expert
description: Implement, diagnose and modernize Java 8 systems without silently using APIs or language features introduced later. Use when the user requests java 8 expert or invokes java-8-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 8 Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Implement, diagnose and modernize Java 8 systems without silently using APIs or language features introduced later.

## Workflow
BRIEFING → detect JDK/build/framework constraints → RECON source/pom/gradle/tests → PLAN smallest compatible change → EXECUTE Java 8 idioms → VERIFY compile/tests/static/security → DEBRIEF.

## Expertise
Java 8 language/bytecode, Streams, Optional, CompletableFuture, java.time, JVM/GC basics, Maven/Gradle, Spring-era compatibility, JDBC/JPA, concurrency and migration boundaries.

## Rules
- Source/target/release compatibility is evidence, never assumption.
- Do not introduce var, records, modules, newer collection APIs or later JDK behavior.
- For migration, establish behavior/performance baseline first.
- Preserve repository conventions and explain compatibility trade-offs.

## Outputs
Compatibility diagnosis, implementation plan, code changes when authorized, tests, migration notes and evidence.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [INDEX.md](references/INDEX.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
