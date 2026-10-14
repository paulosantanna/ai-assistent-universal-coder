---
name: tlc-discover
description: Interviews an unshaped idea into a verdict and a design document - decisions, flows, schema, contracts - that anyone can plan from without having been in the room. Use when the user says "research this", "help me understand this problem", "should we build this", "discovery", "explore this problem", or "tlc-discover". Do NOT use to cut a finished design into tasks, or to implement.
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 0.9.0
  owner_agent: codenavi-agent
---

# TLC Discover

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Interviews an unshaped idea into a verdict and a design document - decisions, flows, schema, contracts - that anyone can plan from without having been in the room.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Critical rules](references/instructions/02-critical-rules.md) — before acting on this contract.
- 3. [The interview](references/instructions/03-the-interview.md) — when this domain or mode is in scope.
- 4. [Situation](references/instructions/04-situation.md) — when this domain or mode is in scope.
- 5. [Problem](references/instructions/05-problem.md) — when this domain or mode is in scope.
- 6. [Verdict](references/instructions/06-verdict.md) — when this domain or mode is in scope.
- 7. [Decide](references/instructions/07-decide.md) — when this domain or mode is in scope.
- 8. [Format](references/instructions/08-format.md) — when this domain or mode is in scope.
- 9. [Knowledge chain](references/instructions/09-knowledge-chain.md) — when this domain or mode is in scope.
- 10. [Output](references/instructions/10-output.md) — before acting on this contract.
- 11. [Examples](references/instructions/11-examples.md) — when choosing an output or matching a use case.
- 12. [Common failures](references/instructions/12-common-failures.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
