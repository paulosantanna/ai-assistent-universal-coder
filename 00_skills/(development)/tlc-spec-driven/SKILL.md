---
name: tlc-spec-driven
description: Feature planning and implementation with 4 adaptive phases (Specify, Design, Tasks, Execute). Auto-sizes depth by complexity. Writes testable requirements in EARS notation, atomic tasks, atomic Conventional Commits, and requirement traceability. Ships deterministic Python validation scripts so structural gates are enforced by code, not memory. Features an independent Verifier (author != verifier, evidence-or-zero), a discrimination sensor, a decision log (STATE.md), a test-coverage matrix, and a self-improving lessons layer. Stack-agnostic and tool-agnostic. Use when (1) planning features, (2) implementing with verification and atomic commits, (3) validating an implementation against a spec. Triggers on "specify feature", "discuss feature", "design", "tasks", "implement", "validate", "verify work", "UAT", "record decision", "pause work", "resume work". Do NOT use for pure architecture decomposition analysis or standalone technical design documents.
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 3.3.0
  owner_agent: codenavi-agent
---

# Tech Lead's Club - Spec-Driven Development

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Feature planning and implementation with 4 adaptive phases (Specify, Design, Tasks, Execute). Auto-sizes depth by complexity. Writes testable requirements in EARS notation, atomic tasks, atomic Conventional Commits, and requirement traceability. Ships deterministic Python validation scripts so structural gates are enforced by code, not memory. Features an independent Verifier (author != verifier, evidence-or-zero), a discrimination sensor, a decision log (STATE.md), a test-coverage matrix, and a self-improving lessons layer. Stack-agnostic and tool-agnostic.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Critical Rules (read before acting)](references/instructions/02-critical-rules-read-before-acting.md) — before acting on this contract.
- 3. [Auto-Sizing: The Core Principle](references/instructions/03-auto-sizing-the-core-principle.md) — when this domain or mode is in scope.
- 4. [.specs Structure](references/instructions/04-specs-structure.md) — when this domain or mode is in scope.
- 5. [Workflow](references/instructions/05-workflow.md) — at this step of execution.
- 6. [Context Loading Strategy](references/instructions/06-context-loading-strategy.md) — when this domain or mode is in scope.
- 7. [Sub-Agent Delegation](references/instructions/07-sub-agent-delegation.md) — when this domain or mode is in scope.
- 8. [Commands](references/instructions/08-commands.md) — when this domain or mode is in scope.
- 9. [Knowledge Verification Chain](references/instructions/09-knowledge-verification-chain.md) — before claiming completion.
- 10. [Output Behavior](references/instructions/10-output-behavior.md) — before acting on this contract.
- 11. [Code Analysis](references/instructions/11-code-analysis.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
