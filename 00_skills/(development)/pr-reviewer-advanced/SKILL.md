---
name: pr-reviewer-advanced
description: Perform severity-ranked, evidence-backed PR review. Use when the user requests pr reviewer advanced or invokes pr-reviewer-advanced. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Advanced PR Reviewer

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Perform severity-ranked, evidence-backed PR review.

## Review dimensions
Correctness, contracts, concurrency, data integrity, security, performance, backward compatibility, tests, observability, documentation and architectural boundaries.

Findings include file/location, failure scenario, impact, evidence and minimal remediation. Avoid speculative nitpicks; prioritize defects that can actually occur. Missing Why/Porquê on the PR body is a review defect because later worktrees lose the motivation for the change.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
