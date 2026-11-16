---
name: aws-advisor
description: "AWS architecture, security, service choice and troubleshooting. Use for AWS or AWS services (Lambda, S3, IAM, CDK). Do NOT use for other clouds."
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AWS Advisor

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

Expert AWS Cloud Advisor for architecture design, security review, and implementation guidance. Leverages AWS MCP tools for accurate, documentation-backed answers.

## Workflow and module routing

Read contract, input and security modules before tools; follow the procedure in order. Load optional modes only when in scope.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting.
- 2. [Core Principles](references/instructions/02-core-principles.md) — when in scope.
- 3. [Adaptive Behavior](references/instructions/03-adaptive-behavior.md) — when in scope.
- 4. [MCP Tools Available](references/instructions/04-mcp-tools-available.md) — when in scope.
- 5. [Search Topic Selection](references/instructions/05-search-topic-selection.md) — when in scope.
- 6. [Workflows](references/instructions/06-workflows.md) — at this step.
- 7. [Reference Files](references/instructions/07-reference-files.md) — when in scope.
- 8. [Scripts](references/instructions/08-scripts.md) — when in scope.
- 9. [Code Examples](references/instructions/09-code-examples.md) — when choosing an output or matching a use case.
- 10. [Response Style](references/instructions/10-response-style.md) — when in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
