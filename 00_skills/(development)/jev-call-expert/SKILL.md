---
name: jev-call-expert
description: "Design and review TypeSafe Jev function calling with typed signatures. Use for Jev calls. Do NOT use for generic tool calling or unapproved actions."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 2.0.0
  owner_agent: codenavi-agent
---

# Jev Call Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

This is a skill of the single `codenavi-agent`, not another agent identity. Convert natural-language requests into bounded calls to ordinary typed functions by letting Jev supply narrow semantic judgments while deterministic code owns parsing, validation, authorization, defaults, confidence policy, and execution.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Identity and mission](references/instructions/02-identity-and-mission.md) — before acting.
- 3. [Preconditions](references/instructions/03-preconditions.md) — before acting.
- 4. [Scope and authority](references/instructions/04-scope-and-authority.md) — before acting.
- 5. [Workflow](references/instructions/05-workflow.md) — at this step.
- 6. [Output contract](references/instructions/06-output-contract.md) — before acting.
- 7. [Examples](references/instructions/07-examples.md) — when choosing an output or matching a use case.
- 8. [Failure behavior and stop conditions](references/instructions/08-failure-behavior-and-stop-conditions.md) — when an input, tool or check fails.
- 9. [Completion criteria](references/instructions/09-completion-criteria.md) — before claiming completion.
- 10. [TypeSafe Primitives Reference (Quick Guide)](references/instructions/10-typesafe-primitives-reference-quick-guide.md) — when in scope.
- 11. [Confidence Thresholds Guide](references/instructions/11-confidence-thresholds-guide.md) — when in scope.
- 12. [Parallel Questions & Speculative Fan-Out](references/instructions/12-parallel-questions-speculative-fan-out.md) — when in scope.
- 13. [Confidence-Gated Routing](references/instructions/13-confidence-gated-routing.md) — when in scope.
- 14. [Composite Scoring](references/instructions/14-composite-scoring.md) — when in scope.
- 15. [SDK Integration Patterns](references/instructions/15-sdk-integration-patterns.md) — when choosing an output or matching a use case.
- 16. [Risk-Aware Confirmation Policy](references/instructions/16-risk-aware-confirmation-policy.md) — before acting.
- 17. [Test Corpus Requirements](references/instructions/17-test-corpus-requirements.md) — before claiming completion.
- 18. [Completion Criteria](references/instructions/18-completion-criteria.md) — before claiming completion.
- 19. [Version History](references/instructions/19-version-history.md) — when in scope.
- 20. [Related Resources](references/instructions/20-related-resources.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
