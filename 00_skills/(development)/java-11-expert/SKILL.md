---
name: java-11-expert
description: "Build and modernize Java 11 systems with Java 8-to-11 compatibility analysis. Use for Java 11 work. Do NOT use for other languages or deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 11 Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Build and modernize production Java 11 systems with explicit Java 8→11 compatibility analysis.

## Expertise
Java 11 APIs/runtime, HTTP Client, var in lambda parameters, modules/runtime removals, TLS/JVM changes, Maven/Gradle, Spring/Jakarta transition risks, containers and GC.

## Procedure
Detect actual toolchain → map dependencies and removed JDK modules → baseline tests → plan bounded migration/change → implement → verify compile/test/runtime/container behavior → document.

Never claim a library is Java 11 compatible without manifest/build or authoritative evidence.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [INDEX.md](references/INDEX.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
