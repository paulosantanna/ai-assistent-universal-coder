---
name: revisar-seguranca-pr
description: Review a concrete pull-request diff for authorization, sensitive-data handling and security failures that scans need contextual evidence to assess. Use when the user says revisar segurança deste PR or avaliar este achado CodeQL/Fortify/Trivy. Do NOT use for general PR review (revisar-pr), fleet vulnerability inventory, or known dependency remediation (cve-remediation).
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Revisar Seguranca Pr

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Review a concrete pull-request diff for authorization, sensitive-data handling and security failures that scans need contextual evidence to assess.

## Workflow

1. Read the PR requirement, exact head SHA, diff, touched trust boundaries and scanner results; omit author identity from the review input.
2. Trace authentication/authorization, input validation, secrets/logging, sensitive responses, data isolation and risky external calls through actual code.
3. Check each relevant scanner finding against the code path and realistic failure conditions; preserve true findings and explain evidenced false positives.
4. Rank findings with file/line, failure scenario, severity, confidence and smallest correction; separate pre-existing issues from new blockers.
5. Produce a local verdict and verification gaps. Publish a review/comment only when the user explicitly requests that remote action.

## Rules

- Never approve from benefit of doubt or claim independent review when the same agent wrote the change.
- Do not duplicate satisfied CI checks; concentrate on context they cannot prove.
- Use a read-only lens; Judge is a deterministic service, never an agent persona.

## Inputs and outputs

Inputs: the user-requested target, authorized source paths/access, scope and expected result.

APROVAR, APROVAR COM RESSALVAS or PEDIR MUDANÇAS, supported by findings and explicit unverified conditions.

## Verification and stop

Verify the actual outputs and relevant contract checks. Missing evidence, dependency, source asset, input or permission blocks its dependent stage; report the precise gap.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
