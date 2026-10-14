---
name: tlc-spec-lean
description: 'Spec-driven feature work that freezes obligations instead of the plan: one human-reviewed plan with EARS criteria, path, entities, interface and one-way doors, then proof-backed checks, then build, then an independent Verifier. Use when the user says "tlc-spec-lean", "plan feature", "specify feature", "write the checks", "build this plan", or "verify work". Do NOT use for standalone design documents unattached to a feature, architecture decomposition analysis, or work that already has a task list or checklist to execute.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 1.1.0
  owner_agent: codenavi-agent
---

# Tech Lead's Club - Spec, Lean

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Spec-driven feature work that freezes obligations instead of the plan: one human-reviewed plan with EARS criteria, path, entities, interface and one-way doors, then proof-backed checks, then build, then an independent Verifier.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Why this shape](references/instructions/02-why-this-shape.md) — when this domain or mode is in scope.
- 3. [Critical rules](references/instructions/03-critical-rules.md) — before acting on this contract.
- 4. [Profile](references/instructions/04-profile.md) — when this domain or mode is in scope.
- 5. [Artifacts](references/instructions/05-artifacts.md) — when this domain or mode is in scope.
- 6. [Understanding and obligations are separate artifacts](references/instructions/06-understanding-and-obligations-are-separate-artifacts.md) — when this domain or mode is in scope.
- 7. [Flow](references/instructions/07-flow.md) — when this domain or mode is in scope.
- 8. [Scripts](references/instructions/08-scripts.md) — when this domain or mode is in scope.
- 9. [Sub-agents and handoff](references/instructions/09-sub-agents-and-handoff.md) — when this domain or mode is in scope.
- 10. [Knowledge chain](references/instructions/10-knowledge-chain.md) — when this domain or mode is in scope.
- 11. [Output behaviour](references/instructions/11-output-behaviour.md) — before acting on this contract.
- 12. [Examples](references/instructions/12-examples.md) — when choosing an output or matching a use case.
- 13. [Troubleshooting](references/instructions/13-troubleshooting.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
