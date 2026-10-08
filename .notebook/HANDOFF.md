# HANDOFF

Updated: 2026-10-08

## Objective
- Add `tests-expert`: real functional and end-to-end checks after a bug fix or new behavior, with the user request as the only oracle.

## Last Verified State
- `skills/tests-expert/SKILL.md` is 48 lines. `skills/skill-architect/scripts/validate_skill.py` PASS (26 checks, 0 warnings).
- Charter gate: an expectation edit against an unchanged user request exits 2. A recorded application failure writes `.aeos/tests-expert/RESUME.md` and exits 3. PASS requires raw evidence and deletes the resume file.
- The router selects `tests-expert` inside the default limit of 5 for a bugfix and for new behavior, and does not select it for an ADR request.
- The runtime loader resolves `tests-expert` from `aeos/registries/skills.tests-expert.additions.yaml`.

## Working Set
- `skills/tests-expert/`
- `.agents/skills/tests-expert/SKILL.md` (Cursor activation entry; the contract is `skills/tests-expert/SKILL.md`)
- `aeos/registries/skills.tests-expert.additions.yaml`
- `aeos/registries/overlay.registry.index.yaml`
- `scripts/aeos-skill-router.mjs`
- `tests/node/tests-expert-charter.test.cjs`
- `tests/node/skill-router-overlay.test.cjs`
- `tests/node/runtime-auth-broker.test.cjs`

## Decisions Already Made
- The oracle is the user request. Code may be read only to find the URL, command, or selector.
- An open failure lives in `.aeos/tests-expert/RESUME.md` plus a pointer in this file. It is not a `MEMORY.md` fact.
- Unit and class tests stay outside this skill.

## Blockers And Risks
- Prior mission, not part of this change: the architecture-knowledge fast-forward into `master` was still unverified at the previous handoff (PR #49).
- `RESUME.md` is gitignored under `.aeos/`. A later window must use the same workspace checkout to read it.
- The charter gate does not detect an evidence file composed by hand. The skill requires raw tool output.

## Evidence Pointers
- `skills/tests-expert/scripts/charter.mjs`
- `tests/node/tests-expert-charter.test.cjs`
- `tests/node/skill-router-overlay.test.cjs`

## Exact Next Actions
- None for this skill. After a bug fix or new behavior, load `tests-expert` and follow `skills/tests-expert/SKILL.md`.

## Validation Still Required
- None for the charter gate, router selection, or runtime registration. This mission did not run a live application in a browser.

Updated: 2026-10-08
