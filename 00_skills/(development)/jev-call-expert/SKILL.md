---
name: jev-call-expert
description: Design, implement, review, and test confidence-aware function calling with TypeSafe Jev, typed tool signatures, Choice and Noul questions, speculative fan-out, and code-owned execution policy. Use when the user asks for Jev tool calling, TypeSafe function routing, natural-language dispatch into typed functions, or repair of a Jev dispatcher. Do NOT use for generic LLM tool calling that does not use TypeSafe, open-ended text generation, or direct execution of untrusted or unapproved actions.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 2.0.0
  owner_agent: codenavi-agent
---

# Jev Call Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

This is a skill of the single `codenavi-agent`, not another agent identity. Convert natural-language requests into bounded calls to ordinary typed functions by letting Jev supply narrow semantic judgments while deterministic code owns parsing, validation, authorization, defaults, confidence policy, and execution.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Identity and mission](references/instructions/02-identity-and-mission.md) — before acting on this contract.
- 3. [Preconditions](references/instructions/03-preconditions.md) — before acting on this contract.
- 4. [Scope and authority](references/instructions/04-scope-and-authority.md) — before acting on this contract.
- 5. [Workflow](references/instructions/05-workflow.md) — at this step of execution.
- 6. [Output contract](references/instructions/06-output-contract.md) — before acting on this contract.
- 7. [Examples](references/instructions/07-examples.md) — when choosing an output or matching a use case.
- 8. [Failure behavior and stop conditions](references/instructions/08-failure-behavior-and-stop-conditions.md) — when an input, tool or check fails.
- 9. [Completion criteria](references/instructions/09-completion-criteria.md) — before claiming completion.
- 10. [TypeSafe Primitives Reference (Quick Guide)](references/instructions/10-typesafe-primitives-reference-quick-guide.md) — when this domain or mode is in scope.
- 11. [Confidence Thresholds Guide](references/instructions/11-confidence-thresholds-guide.md) — when this domain or mode is in scope.
- 12. [Parallel Questions & Speculative Fan-Out](references/instructions/12-parallel-questions-speculative-fan-out.md) — when this domain or mode is in scope.
- 13. [Confidence-Gated Routing](references/instructions/13-confidence-gated-routing.md) — when this domain or mode is in scope.
- 14. [Composite Scoring](references/instructions/14-composite-scoring.md) — when this domain or mode is in scope.
- 15. [SDK Integration Patterns](references/instructions/15-sdk-integration-patterns.md) — when choosing an output or matching a use case.
- 16. [Risk-Aware Confirmation Policy](references/instructions/16-risk-aware-confirmation-policy.md) — before acting on this contract.
- 17. [Test Corpus Requirements](references/instructions/17-test-corpus-requirements.md) — before claiming completion.
- 18. [Completion Criteria](references/instructions/18-completion-criteria.md) — before claiming completion.
- 19. [Version History](references/instructions/19-version-history.md) — when this domain or mode is in scope.
- 20. [Related Resources](references/instructions/20-related-resources.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance and source freshness: [provenance](references/provenance.md).
