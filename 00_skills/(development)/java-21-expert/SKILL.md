---
name: java-21-expert
description: "Design and implement Java 21 systems and migrations with LTS-aware verification. Use for Java 21 work. Do NOT use for other languages or deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Java 21 Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Design and implement Java 21 production systems and migrations with LTS-aware verification.

## Expertise
Virtual threads, record patterns, pattern matching for switch, sequenced collections, modern JVM/runtime behavior, structured-concurrency boundaries when preview status applies, Spring Boot 3+, Jakarta, observability and containers.

## Rules
Never enable preview features implicitly. For virtual threads, inspect blocking model, pinning risks, pools, DB/client limits and observability before adoption. Benchmark rather than assume throughput gains.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [INDEX.md](references/INDEX.md) only when the domain workflow needs it; root governance and this entry take precedence.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
