---
name: tests-expert
description: "Run real functional and e2e checks after a fix or new behavior. Use for fixes, new features or e2e tests. Do NOT use for unit tests or coverage."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Tests Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

The user request is the only oracle. The running application is what you observe. Module map: `references/INDEX.md`.

## Automatic use

Run this skill after application code is written or changed to fix a bug, before declaring that work done, even if the user never said "test". A new context window reads `.aeos/tests-expert/RESUME.md` first when it exists. Failure handling and exit codes: `references/failure-memory.md`.

## Rules

1. Write each check from the user request before using the implementation as an expected value. Procedure: `references/oracle.md`.
2. Exercise a real browser, HTTP, CLI, or job surface. A unit or class test is not proof. Runner and evidence shape: `references/execution.md`.
3. Freeze the charter before the run. `ORACLE_TAMPERED` or `OPEN_FAILURE_BLOCKING` means restore the frozen checks and change the application.
4. A failed check stays frozen. Do not invent a passing check, copy the broken behavior into the expectation, or stop while status is `open`.
5. Evidence is raw tool output. Redact secrets before they reach the charter, the evidence, or `.notebook/`.

## Workflow

1. Run `node "00_skills/(quality)/tests-expert/scripts/charter.mjs" resume --state .aeos/tests-expert/state.json`. Exit 0 prints the open failure: keep that oracle and go to step 4. Exit 1 means there is nothing to resume.
2. Copy the user request into the charter and add one functional or end-to-end check per observable outcome they asked for. Shape and counterexamples: `references/examples.md`.
3. Freeze with `node "00_skills/(quality)/tests-expert/scripts/charter.mjs" freeze --charter .aeos/tests-expert/charter.json --state .aeos/tests-expert/state.json`. Exit 0 freezes. Exit 2 blocks a changed oracle. Pass `--allow-new-request` only when the user stated a different request.
4. Run the application the way a user would. Save the raw output under `.aeos/tests-expert/evidence/` and include every check id in that output.
5. Record with `node "00_skills/(quality)/tests-expert/scripts/charter.mjs" record --charter .aeos/tests-expert/charter.json --state .aeos/tests-expert/state.json --outcome .aeos/tests-expert/outcome.json`. Exit 0 is PASS. Exit 3 means the application failed and the next-window memory was written.
6. On exit 3, follow `references/failure-memory.md` and point `.notebook/HANDOFF.md` at `RESUME.md` before any further edit. Fix the application and repeat from step 4 until record exits 0. A later window that does not have the failure starts at step 1.

## Stop

Stop, without a passing claim, when the request names no observable behavior, the only possible check is a unit or class test, or the run would touch production data. Say what is missing.

## Output

Report the charter hash, the surface, the evidence path, and PASS or the open resume path. Do not report PASS from a unit test or from an edited expectation.

## Example

User says: "o login aceita senha vazia; corrija."
Result: one `browser` or `http` check that an empty password is rejected. A session after submit is FAIL. The expectation stays frozen until rejection is observed.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
