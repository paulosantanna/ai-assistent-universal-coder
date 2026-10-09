# PROGRESS

Updated: 2026-10-08

## Active Mission
- Objective: add `tests-expert`, a skill of at most 100 lines that runs real functional and end-to-end checks from the user request after a bug fix or new behavior, and keeps a failed run for a later context window.
- [x] BRIEFING: notebook read; scope = one skill, charter gate, router boost, overlay registry, Cursor activation entry.
- [x] RECON: skill-architect contract, kotlin/ADR skill layout, overlay loader, and router boosts inspected.
- [x] PLAN: canonical skill under `skills/tests-expert/`; modules in `references/`; deterministic gate in `scripts/charter.mjs`.
- [x] EXECUTE: skill package, registry fragment, router boost, and tests written.
- [x] VERIFY: `validate_skill.py` PASS; Jest and Mocha charter/router tests PASS; runtime loader resolves the skill.
- [x] DEBRIEF: notebook updated with the oracle rule and the resume-file lesson.

## Current Phase
- DEBRIEF

## Verification Gates
- [x] `skills/tests-expert/SKILL.md` is at or under 100 lines (48) and `validate_skill.py` reports 0 errors and 0 warnings.
- [x] A charter whose oracle is the implementation, a unit surface, or an edited expectation is rejected. Exit 2 on tamper. Exit 3 writes `RESUME.md`. PASS deletes it.
- [x] Default router limit 5 selects `tests-expert` for a bugfix and for new behavior, and omits it for an ADR request.
- [x] `RegistryLoader.loadSkills()` includes `tests-expert` owned by `codenavi-agent`.

## Factual Log
- 2026-10-08: `validate_skill.py skills/tests-expert` PASS, 26 checks, description 474 characters.
- 2026-10-08: Jest `tests-expert-charter` and `skill-router-overlay` PASS (14 tests). Mocha the same 14 PASS. `runtime-auth-broker` PASS (5 tests) after `npm --prefix runtime run build`.
- 2026-10-08: Frontmatter, single-agent, and continuity guards PASS before the notebook debrief edits.
- 2026-10-08: CI run `37850206011` failed `tests/node/skill-router.test.cjs`: `tests-expert` outranked `java-docs-bug-solver` on `corrigir bug Java com testes`. Correction aliases were removed from the tests-expert boost. Jest 17 suites / 107 tests PASS.

## Previous Missions
- ADR, ADL, AKM, and ASR skills plus the architecture-knowledge MCP. Fast-forward into `master` was still unverified at the previous handoff (PR #49).
- Governed `rag-node` MCP with the TLC `rag-api` causal knowledge map (PR #48, `be2dc781`).
