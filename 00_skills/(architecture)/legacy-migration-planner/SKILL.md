---
name: legacy-migration-planner
description: "Plan legacy migrations, strangler-fig rewrites and framework upgrades. Use for migration strategy. Do NOT use for domain analysis (domain-analysis)."
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Legacy Migration Planner

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Plan legacy migrations, strangler-fig rewrites and framework upgrades. Use for migration strategy. Do NOT use for domain analysis (domain-analysis).

  

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Core Principles](references/instructions/02-core-principles.md) — when in scope.
- 3. [Workflow](references/instructions/03-workflow.md) — at this step.
- 4. [Output Structure](references/instructions/04-output-structure.md) — before acting.
- 5. [Reference Guide](references/instructions/05-reference-guide.md) — when in scope.
- 6. [Constraints](references/instructions/06-constraints.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [parity lens](lenses/parity-auditor.md) when validating migration outputs; missing applicable evidence yields INCONCLUSIVO. It is a sequential lens of codenavi-agent, never an independent profile.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
