---
name: kotlin-expert
description: Design and implement Kotlin production systems and migrations against the current stable Kotlin release, with version-aware verification. Use when the user requests kotlin expert or invokes kotlin-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Kotlin Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Design and implement Kotlin production systems and migrations against the current stable Kotlin release, with version-aware verification.

## Expertise
K2 compiler, current stable Kotlin 2.4.20, language/API 2.4, coroutines, Kotlin Multiplatform, Gradle Kotlin DSL, JVM/JS/Native/Wasm targets, Java interop, null-safety, Compose when present, kotlinx libraries, observability and containers.

## Rules
Never enable Experimental/Alpha/Beta or opt-in APIs implicitly. Detect the Kotlin Gradle plugin, `languageVersion` and `apiVersion` before using newer APIs. Query `docs-kotlin-current` for signatures, release status and migration deltas. Do not upgrade the toolchain merely because a newer compiler exists.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [current-release.md](references/current-release.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
Read [INDEX.md](references/INDEX.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
