---
name: java-11-expert
description: Build and modernize production Java 11 systems with explicit Java 8→11 compatibility analysis. Use when the user requests java 11 expert or invokes java-11-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 11 Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Build and modernize production Java 11 systems with explicit Java 8→11 compatibility analysis.

## Expertise
Java 11 APIs/runtime, HTTP Client, var in lambda parameters, modules/runtime removals, TLS/JVM changes, Maven/Gradle, Spring/Jakarta transition risks, containers and GC.

## Procedure
Detect actual toolchain → map dependencies and removed JDK modules → baseline tests → plan bounded migration/change → implement → verify compile/test/runtime/container behavior → document.

Never claim a library is Java 11 compatible without manifest/build or authoritative evidence.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [INDEX.md](references/INDEX.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
