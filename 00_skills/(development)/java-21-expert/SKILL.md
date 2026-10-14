---
name: java-21-expert
description: Design and implement Java 21 production systems and migrations with LTS-aware verification. Use when the user requests java 21 expert or invokes java-21-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 21 Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Design and implement Java 21 production systems and migrations with LTS-aware verification.

## Expertise
Virtual threads, record patterns, pattern matching for switch, sequenced collections, modern JVM/runtime behavior, structured-concurrency boundaries when preview status applies, Spring Boot 3+, Jakarta, observability and containers.

## Rules
Never enable preview features implicitly. For virtual threads, inspect blocking model, pinning risks, pools, DB/client limits and observability before adoption. Benchmark rather than assume throughput gains.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [INDEX.md](references/INDEX.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
