---
name: legacy-migration-planner
description: Use when planning legacy system migrations, codebase modernization, monolith decomposition, microservices consolidation, cross-language rewrites, or framework upgrades. Invoke for strangler fig pattern, incremental migration strategy, or refactoring roadmaps. Do NOT use for domain analysis (use domain-analysis), component sizing (use component-identification-sizing), or step-by-step decomposition plans (use decomposition-planning-roadmap).
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Legacy Migration Planner

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Use when planning legacy system migrations, codebase modernization, monolith decomposition, microservices consolidation, cross-language rewrites, or framework upgrades. Invoke for strangler fig pattern, incremental migration strategy, or refactoring roadmaps. Do NOT use for domain analysis (use domain-analysis), component sizing (use component-identification-sizing), or step-by-step decomposition plans (use decomposition-planning-roadmap).

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Core Principles](references/instructions/02-core-principles.md) — when this domain or mode is in scope.
- 3. [Workflow](references/instructions/03-workflow.md) — at this step of execution.
- 4. [Output Structure](references/instructions/04-output-structure.md) — before acting on this contract.
- 5. [Reference Guide](references/instructions/05-reference-guide.md) — when this domain or mode is in scope.
- 6. [Constraints](references/instructions/06-constraints.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.

Read [parity lens](lenses/parity-auditor.md) when validating migration outputs; missing applicable evidence yields INCONCLUSIVO. It is a sequential lens of codenavi-agent, never an independent profile.
