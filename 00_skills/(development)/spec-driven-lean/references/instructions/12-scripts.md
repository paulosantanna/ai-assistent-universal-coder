<!-- Package: 00_skills/(development)/spec-driven-lean; relative command/resource examples resolve from that package or workspace root. -->

## Scripts

| When | Command |
| --- | --- |
| Before presenting the plan | `validate_plan.py <feature>` |
| Before starting to build | `validate_checks.py <feature>` |
| Before each authorized commit | `check_commit.py --message "<msg>"` |
| Before declaring done | `validate_verification.py <feature>` |
| After editing a validator or template | `selftest.py` |

Non-zero exit means STOP and fix. Degrade to manual artifact reading only when Python cannot run.
