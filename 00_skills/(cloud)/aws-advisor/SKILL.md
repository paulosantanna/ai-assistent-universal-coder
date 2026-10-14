---
name: aws-advisor
description: Expert AWS Cloud Advisor for architecture design, security review, and implementation guidance. Leverages AWS MCP tools for accurate, documentation-backed answers. Use when user asks about AWS architecture, security, service selection, migrations, troubleshooting, or learning AWS. Triggers on AWS, Lambda, S3, EC2, ECS, EKS, DynamoDB, RDS, CloudFormation, CDK, Terraform, Serverless, SAM, IAM, VPC, API Gateway, or any AWS service. Do NOT use for non-AWS cloud providers or general infrastructure without AWS context.
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AWS Advisor

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Expert AWS Cloud Advisor for architecture design, security review, and implementation guidance. Leverages AWS MCP tools for accurate, documentation-backed answers.

## Workflow and module routing

Read the contract/input/security modules before tools; then follow the applicable procedure in the original order. Load optional modes only when their scope applies.

- 1. [Purpose and contract](references/instructions/01-purpose-and-contract.md) — before acting on this contract.
- 2. [Core Principles](references/instructions/02-core-principles.md) — when this domain or mode is in scope.
- 3. [Adaptive Behavior](references/instructions/03-adaptive-behavior.md) — when this domain or mode is in scope.
- 4. [MCP Tools Available](references/instructions/04-mcp-tools-available.md) — when this domain or mode is in scope.
- 5. [Search Topic Selection](references/instructions/05-search-topic-selection.md) — when this domain or mode is in scope.
- 6. [Workflows](references/instructions/06-workflows.md) — at this step of execution.
- 7. [Reference Files](references/instructions/07-reference-files.md) — when this domain or mode is in scope.
- 8. [Scripts](references/instructions/08-scripts.md) — when this domain or mode is in scope.
- 9. [Code Examples](references/instructions/09-code-examples.md) — when choosing an output or matching a use case.
- 10. [Response Style](references/instructions/10-response-style.md) — when this domain or mode is in scope.

## Boundaries and result

Use only tools actually available for the authorized task. Keep secrets in runtime providers. Missing evidence, inputs or permissions blocks the affected action. Return the domain output with source pointers, executed checks and remaining uncertainty; never claim an unexecuted check passed.

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
