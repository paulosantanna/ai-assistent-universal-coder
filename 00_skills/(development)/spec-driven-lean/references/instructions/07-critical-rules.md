<!-- Package: 00_skills/(development)/spec-driven-lean; relative command/resource examples resolve from that package or workspace root. -->

## Critical rules

1. Resolve `<skill-dir>` as the directory that contains this `SKILL.md`. Run `python`/`py -3`/`python3` as `<skill-dir>/scripts/<name>.py`. Project data stays under `.specs/`; pass `--root` when cwd differs.
2. Every check is one observable claim with a concrete value plus the proof whose exit code settles it. No proof, no check.
3. Tests assert what the checks say, never what the code happens to do.
4. Never weaken, delete or skip a test to pass. A wrong check is stop-and-ask.
5. Checks and `Test policy` rows are fixed once approved. `Landing`, `Relations` and `Surface` are additive. `Flow` and `Impact` stay true.
6. `VerifierLens` is dispatched by the orchestrating turn, never by the builder, over `<feature base>..HEAD` with every check. The builder does not write `verification.md`.
7. Completion requires `<skill-dir>/scripts/validate_verification.py` exit 0.
8. Approved plan/checks authorize local edits and local commits only when the user has authorized commits. `git push`, deploy and production data changes need an explicit go-ahead.
