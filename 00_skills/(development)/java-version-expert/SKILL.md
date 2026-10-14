---
name: java-version-expert
description: Route Java work to the exact verified JDK profile without loading unrelated version knowledge. Use when the user requests java version expert or invokes java-version-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: java-version-expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Route Java work to the exact verified JDK profile without loading unrelated version knowledge.

## Invoke when
- a Java repository must be created, diagnosed, modernized or migrated;
- the target JDK is unknown or multiple JDKs coexist;
- framework/build compatibility must be resolved before implementation.

## Lifecycle
**BRIEFING** — objective, target repository, runtime constraints, acceptance criteria.

**RECON** — inspect `pom.xml`/Gradle, toolchains, CI, container/runtime, framework versions and production JDK. Never infer the target from syntax alone.

**PLAN** — select exactly one primary version expert (`java-expert-17`, `java-expert-21`, `java-expert-25`, `java-expert-26`) plus migration references only when required.

**EXECUTE** — preserve project conventions; use only APIs/features supported by the verified target; keep changes surgical.

**VERIFY** — compile/test with the declared toolchain and verify framework/plugin/runtime compatibility from current official documentation.

**DEBRIEF** — evidence, changed files, test/build result, residual compatibility risks and notebook updates.

## Token contract
Read this file first. Then read `references/INDEX.md`. Load only the references selected by mission/version. Do not load all JDK profiles into one context.

## Stop conditions
- JDK source/target/runtime cannot be established;
- framework/plugin compatibility is unresolved for a material change;
- requested API behavior cannot be verified from project evidence or current authoritative documentation.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
