---
name: tlc-spec-lean
description: "Tech Lead Club spec-lean 2.0.0: freeze observable obligations in plan and proof-backed checks, then build and verify mutations and screens. Use for \"tlc-spec-lean\", \"plan feature\", \"write the checks\", \"build this plan\", \"verify work\". Do NOT use for standalone design documents, architecture decomposition or work with an existing task list."
license: CC-BY-4.0
metadata:
  author: "Tech Leads Club - github.com/tech-leads-club"
  version: 2.0.0
  owner_agent: codenavi-agent
---

# tlc-spec-lean

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Mission

Plan → Checks → Build → Verify. Freeze obligations and coverage rather than a task catalogue; run proofs at HEAD and verify mutations and screens before completion.

## Workflow

1. Inspect the user request, target code and continuity quartet; define observable success and size the feature.
2. Read the [official 2.0.0 contract](references/tlc/UPSTREAM.md) before acting. Read each phase reference completely when that phase applies.
3. Use local `scripts/` for executable gates (including the Windows mutation fix); `references/tlc/` is the immutable source snapshot. Resolve references using the paths below; `.specs/` belongs to the target project. Pass `--root` when cwd differs. Do not use workspace-root `scripts/` by accident.
4. Preserve product decisions and binding captures. Record real approvals and answers in feature artifacts; never fabricate approval or ask again for authorization already given in the session.
5. Derive tests from requirements/checks. Run gates and fix failures; never weaken checks to obtain a pass. validate_plan.py → validate_checks.py → check_commit.py → check_proofs.py → validate_verification.py. Run selftest.py after validator/template changes.
6. Keep author, verifier and screen review as sequential internal lenses of codenavi-agent. No additional agent identities or delegation are permitted. This is self-verification: use the source fallback in a fresh session and label it `self-verified`; never claim independent review.
7. Commit only within existing session authorization and local policy. Remote publication, deploy and production data changes require explicit authorization for that action.
8. Report artifacts, executed gates, proof HEAD and unresolved findings; update continuity with durable evidence. A failing gate blocks completion.

## Phase resources

- Read [plan.md](references/tlc/references/plan.md) before presenting a plan.
- Read [checks.md](references/tlc/references/checks.md) before freezing checks.
- Read [build.md](references/tlc/references/build.md) before implementation.
- Read [verify.md](references/tlc/references/verify.md) when verifying completion.
- Read [verify-screens.md](references/tlc/references/verify-screens.md) when a capture has a running picture.
- Read [memory.md](references/tlc/references/memory.md) when recording decisions or lessons.

Run `python 00_skills/(development)/tlc-spec-lean/scripts/<name>.py` with the feature arguments required by the phase. Python 3.8+ and Git are required for proofs/mutations; browser and image-reading support are required for capture checks.

## Examples and failure handling

Example: "plan feature: add a billing guard" → inspect the target, write criteria and proofs, build within approved scope and report the gate result. A standalone architecture document routes elsewhere.

Missing Python/Git, browser, image support, evidence or authorization blocks the affected proof/action; report it. Credentials stay in approved runtime providers; never persist secrets or raw cookies.

Source/license/version: [provenance](references/provenance.md).

## Supporting resources

- Read [retained instructions](references/instructions) only for its matching supporting context; the current entry and pinned phase procedures take precedence.
