---
name: pr-comment-resolver
description: Resolve pull-request review comments systematically without blindly obeying incorrect feedback. Use when the user requests pr comment resolver or invokes pr-comment-resolver. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# PR Comment Resolver

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Resolve pull-request review comments systematically without blindly obeying incorrect feedback.

## Workflow
Collect unresolved threads → classify correctness/security/style/question → inspect referenced code → reproduce concern when possible → accept/reject with technical rationale → implement minimal fix → run targeted/full verification → draft evidence-backed reply → resolve only when addressed.

Never modify unrelated code merely to satisfy stylistic preference.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
