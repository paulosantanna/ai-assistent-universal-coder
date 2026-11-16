---
name: fable-judge
description: "Adversarial verification of finished work: reruns checks, catches false claims. Use for finished-work verification. Do NOT use as deployment approval."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: fable-judge

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
