---
name: java-17-expert
description: Implement and migrate LTS Java 17 applications safely. Use when the user requests java 17 expert or invokes java-17-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 17 Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Implement and migrate LTS Java 17 applications safely.

## Expertise
Records, sealed classes, pattern matching available in 17, strong encapsulation, JVM/GC, Spring Boot compatibility, Jakarta boundaries, Maven/Gradle, containers and observability.

## Migration gate
Inventory reflection/internal JDK use, dependencies/plugins, tests, JVM flags and serialization contracts before changing toolchain. Establish baseline, migrate incrementally, verify runtime behavior and performance.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [INDEX.md](references/INDEX.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
