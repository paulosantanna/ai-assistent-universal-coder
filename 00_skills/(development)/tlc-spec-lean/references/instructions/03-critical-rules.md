<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Critical rules

The pinned set. These hold even if no reference file is read, and they are the only rules that
never scale down with the profile.

1. Every check is **one observable claim with a concrete value** plus the **proof** - the test
   or command whose exit code settles it. No proof, no check.
2. Tests assert what the checks say, never what the code happens to do. Never write a test by
   reading the implementation.
3. Never weaken an assertion, delete a test, or skip one to make a suite pass. A genuinely
   wrong check is a stop-and-ask, not an edit.
4. Checks and `Test policy` rows are fixed once approved. In the design, `Landing`, `Relations`
   and `Surface` are additive - a door discovered while building gets a row before the code that
   closes it, and a row the user approved is never rewritten. `Flow` and `Impact` are neither:
   they are **kept true**, so a different path changes the hop in that path's commit.
5. The **Verifier is a fresh sub-agent**, never the author, never optional, never waiting to
   be asked. Whoever holds the whole feature dispatches it after the **last commit of the
   feature** lands - over `<feature base>..HEAD`, with **every** check. Never by a builder,
   and never as a child of one. A builder finishes, reports, and stops. The work is not done
   at the last commit; it is done when the Verifier's report accounts for every check.
6. **The profile is a floor and it is not a secret.** The verification report names it, or "no
   faults injected" reads exactly like forgetting to inject them.
7. The completion gate is a script, not a feeling: `validate_verification.py` must exit 0.
8. **Blast radius:** an approved spec authorizes local edits and local commits. `git push`,
   deploy, and production data changes need an explicit go-ahead for that action.
