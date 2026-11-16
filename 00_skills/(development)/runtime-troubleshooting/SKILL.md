---
name: runtime-troubleshooting
description: "Diagnose apps from read-only logs. Use for runtime failures. Do NOT use to restart, scale, deploy, redesign or invent inaccessible broker state."
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Runtime Troubleshooting

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Diagnose a running application from read-only logs, metrics, traces, events and repository code without changing the live system.

## Workflow

1. Freeze the symptom, time window, affected environment/component, expected behavior and available read-only access.
2. Collect bounded logs/metrics/traces/events/configuration references with timestamps, correlation IDs and secret redaction.
3. Map the runtime component to the exact repository/deployed version; compare the failing path to source and current API behavior.
4. Rank hypotheses by falsifiable evidence and perform only safe read-only diagnostics; distinguish root cause, contributor and unanswered question.
5. Present the smallest remediation option, verification and rollback requirements; hand live mutations to the authorized operations workflow and preserve incident continuity.

## Rules

- No restart, scale, patch, write, destructive query or configuration change on the running system.
- Do not treat symptoms or correlated events as a proven root cause.
- If access or deployment identity is missing, state the gap and stop the dependent claim.

## Inputs and outputs

Inputs: the user-requested target, authorized source paths/access, scope and expected result.

An evidenced diagnostic timeline, code/runtime pointers, ranked hypotheses, confirmed cause where supported and actionable remediation/verification handoff.

## Verification and stop

Verify the actual outputs and relevant contract checks. Missing evidence, dependency, source asset, input or permission blocks its dependent stage; report the precise gap.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
