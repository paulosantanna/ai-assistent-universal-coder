<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Scripts

Resolve `<skill-dir>` as the directory containing this `SKILL.md` and invoke
`python3 <skill-dir>/scripts/<name>.py`. Project data under `.specs/` stays relative to the
project root; pass `--root` when cwd differs. A non-zero exit means STOP and fix.

| When | Command |
| --- | --- |
| Before presenting the plan | `validate_plan.py <feature>` |
| Before starting to build | `validate_checks.py <feature>` |
| Before each commit | `check_commit.py --message "<msg>"` |
| Before declaring done | `validate_verification.py <feature>` |
| At distillation | `lessons.py add ...` |
| After editing a validator or template | `selftest.py` |

`validate_plan.py` runs the closure gate and guards the shape half against becoming what it
replaced: it fails a criterion with no SHALL, an assumption with no chosen default, an `Observable`
row whose landing is blank or whose `n/a` carries no reason, a `Landing`
row with no literal shape or no rejected alternative, columns and types inside `Relations`, a
`Surface` route with no statuses, and any section left blank rather than answered with
`None - <why>`. `validate_checks.py` is the omission catcher: it fails a check with no proof, a
coverage row whose declared size exceeds the members actually assigned, a missing swept dimension,
and a missing profile line, and warns on a route the plan reviewed that no check mentions.
`validate_verification.py` fails a PASS report that cites no `file:line`, records a surviving
mutant, leaves an `Unproven` member, or was written by the author.

Skip a script only when no code-execution tool exists; then perform the same checks by reading
the artifact and say once in chat that you are in the degraded path.

`selftest.py` applies this skill's own discipline to its gates: it mutates a filled-in fixture
set once per rule and requires every mutant to be killed, runs negative controls proving a
profile-scoped gate does **not** fire below its profile, and smoke-runs every script shipped
here - an unexercised script is where a crash hides, and the completion gate once exited 0 with
nothing gated. Run it after editing a validator or a
template - a validator that exits 0 on everything is decoration, one that exits 1 on everything
makes `light` unusable, and only injection tells the two apart. The fixtures in
`scripts/fixtures/` are also a complete worked example of a passing `standard` artifact set.
