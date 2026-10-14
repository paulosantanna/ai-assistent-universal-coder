---
name: tlc-implement
description: 'Implement a work already planned: extracts a checklist, builds it, and proves every check with an independent verifier. Use when the user says "extract a checklist", "build this ticket", "implement this spec", or "tlc-implement". Do NOT use when nobody has decided what to build, or to design the work.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: 0.1.0
  owner_agent: codenavi-agent
---

# TLC Implement

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Implement a work already planned: extracts a checklist, builds it, and proves every check with an independent verifier.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Profile](references/instructions/02-profile.md) — when this domain or mode is in scope.
- 3. [Critical rules](references/instructions/03-critical-rules.md) — before acting on this contract.
- 4. [Extract](references/instructions/04-extract.md) — when this domain or mode is in scope.
- 5. [Build](references/instructions/05-build.md) — when this domain or mode is in scope.
- 6. [Verify](references/instructions/06-verify.md) — before claiming completion.
- 7. [Knowledge chain](references/instructions/07-knowledge-chain.md) — when this domain or mode is in scope.
- 8. [Output](references/instructions/08-output.md) — before acting on this contract.
- 9. [Examples](references/instructions/09-examples.md) — when choosing an output or matching a use case.
- 10. [Common failures](references/instructions/10-common-failures.md) — when an input, tool or check fails.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).
