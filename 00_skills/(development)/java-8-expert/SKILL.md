---
name: java-8-expert
description: "Implement, diagnose and modernize Java 8 systems without later-version APIs. Use for Java 8 work. Do NOT use for other languages or deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 8 Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [INDEX.md](references/INDEX.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
