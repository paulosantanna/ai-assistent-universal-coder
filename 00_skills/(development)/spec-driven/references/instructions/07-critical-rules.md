<!-- Package: 00_skills/(development)/spec-driven; relative command/resource examples resolve from that package or workspace root. -->

## Critical rules

1. Resolve `<skill-dir>` as the directory that contains this `SKILL.md`. Read referenced files completely. Run `python`/`py -3`/`python3` as `<skill-dir>/scripts/<name>.py`. Project data stays under `.specs/` at the project root; pass `--root` when cwd differs.
2. Tests assert spec-defined outcomes, never the implementation.
3. A task is done only when its gate passes.
4. One atomic local commit per formal task **only when the user has authorized commits**. Otherwise mark task state and stop for explicit commit approval. Never weaken or delete tests to pass.
5. After the last task, the `VerifierLens` always runs. Author of the implementation must not write `validation.md`.
6. Approved spec/tasks authorize local implementation only. `git push`, force-push, deploy, production DB changes and other remote/destructive operations need an explicit go-ahead for that action.
7. Non-zero validator exit means STOP and fix.
