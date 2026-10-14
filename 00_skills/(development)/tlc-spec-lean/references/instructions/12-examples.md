<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Example 1: Plan a feature

User says: "tlc-spec-lean — plan the lockfile v2 migration"
Actions:

1. Read the repository and write `.specs/features/lockfile-v2/plan.md` (Problem, Flow, Impact, Relations, Surface, Landing, Criteria)
2. Run `python3 <skill-dir>/scripts/validate_plan.py lockfile-v2`
3. Stop for human review — no checks and no code yet

Result: A plan the user can object to. `validate_plan.py` exits 0. `checks.md` does not exist.

### Example 2: Write the checks and build

User says: "write the checks and build this plan"
Actions:

1. Derive `.specs/features/lockfile-v2/checks.md` from the approved plan (claims + proofs, Coverage join, Test policy, Swept)
2. Run `python3 <skill-dir>/scripts/validate_checks.py lockfile-v2`
3. Write `## Handoff` with the arithmetic. Under the budget: one builder, no ask. Over: stop and ask (handoff vs one builder); record the choice before any code
4. Write tests from the checks — never from the implementation — then implement, run each proof, and commit
5. After the last commit of the feature, dispatch a fresh Verifier with [verify.md](../tlc/references/verify.md) — same turn, no ask. A builder of one batch would have stopped after step 4 instead.

Result: Proof-backed checks, green proofs, coherent commits, and a Verifier report that accounts for every check. The author does not write `verification.md`.

### Example 3: Verify a feature that already landed

User says: "verify work" (recovery — the happy path never waits for this)
Actions:

1. The orchestrator — not the builder — dispatches a fresh Verifier over `<feature base>..HEAD` with every check
2. The Verifier writes `.specs/features/lockfile-v2/verification.md`
3. Run `python3 <skill-dir>/scripts/validate_verification.py lockfile-v2`

Result: An independent verification report. `validate_verification.py` exits 0. Author is not the verifier.
