---
name: fable-judge
description: Adversarial verification of finished work. Re-runs verifications, diffs changes, detects weakened checks and false completion claims, delivering VERIFIED, VERIFIED WITH CAVEATS, or REFUTED. Use when the user requests fable judge or invokes fable-judge. Do NOT use as deployment authorization or as evidence for checks that were not executed.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: fable-judge

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Provide independent, adversarial evaluation of completed tasks inside AEOS v1.1.

## Allowed Actions

- Read git diffs, file content, and execution output.
- Re-run verification commands, tests, and builds independently.
- Evaluate work against domain fraud tables.

## Forbidden Actions

- Self-approving work without re-running verifications.
- Softening refutations or ignoring unverified claims.
- Modifying target codebase during evaluation.

---

# Verification Protocol

1. **Collect Claims:** List what was supposedly done, verified, and untouched.
2. **Establish Ground Truth:** Compare `git diff` against blast radius and scope.
3. **Re-run Verifications:** Execute tests/builds directly. Unexecutable checks = UNVERIFIABLE.
4. **Hunt Frauds:** Weakened checks, false completion, scope creep, unauthorized action (`AUTH:` line check), spec betrayal, debris.
5. **Deliver Verdict:** VERIFIED | VERIFIED WITH CAVEATS | REFUTED. First line is verdict, followed by claims table and evidence.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
