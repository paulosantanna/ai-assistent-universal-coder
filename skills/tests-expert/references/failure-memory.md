# Failure memory

Read this when a run fails, when resume prints a failure, or when `.aeos/tests-expert/RESUME.md` already exists.

## Files

| Path | Role |
| --- | --- |
| `.aeos/tests-expert/charter.json` | the frozen request and checks |
| `.aeos/tests-expert/state.json` | hashes, attempts, and status |
| `.aeos/tests-expert/RESUME.md` | what the next context window reads |
| `.aeos/tests-expert/evidence/` | raw application output |

`.aeos/` is gitignored. `RESUME.md` is the resume memory. It is not a `.notebook/MEMORY.md` entry. Memory stays for durable facts; this file is the open failure.

On exit 3, add a pointer to `.notebook/HANDOFF.md`: objective, charter hash, `RESUME.md` path, and the next action "fix the application and re-run the same checks". Do not paste secrets. Do not copy the transcript into `MEMORY.md`.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | freeze succeeded, or `record` returned PASS |
| 1 | invalid charter, missing evidence, or resume found nothing open |
| 2 | `ORACLE_TAMPERED` or `OPEN_FAILURE_BLOCKING` |
| 3 | the application failed; `RESUME.md` was written |

Exit 3 is a recorded product failure, not a broken script.

## Continue until pass

Write `RESUME.md` before editing the application again. The same window may fix and re-record immediately. A later window that does not still hold the failure does this instead:

1. Read `RESUME.md` and `skills/tests-expert/SKILL.md`.
2. Reconstruct `charter.json` from `state.charter` if the file is gone. Do not edit it.
3. Fix the application.
4. Re-run the same surfaces and `record` again.

Repeat until `record` exits 0. There is no attempt cap. A pass deletes `RESUME.md`. Do not declare the request done while status is `open`.

`--allow-new-request` replaces the frozen user request. Use it only when the user stated a different request. Do not use it to unlock a failing check.
