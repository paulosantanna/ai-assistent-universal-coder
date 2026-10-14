<!-- Package: 00_skills/(quality)/the-judge; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Example 1: routine review

User says: "revise esse PR" (on a branch with an open PR, 180 changed lines, TypeScript).
Actions: Steps 0-2 (research: one dep bump, checked its changelog), sequential passes, 1 should-fix + 2 nits survive verification, gate passes on second run (first run caught an exclamation mark), post as COMMENT.
Result: one consolidated review, three inline comments, summary with research log citing the changelog URL.

### Example 2: blocker found

User says: "judge this PR before I merge".
Actions: Pass A finds an unguarded division in a money path with a traced failing input; verification confirms at `src/billing/invoice.ts:142`; verdict REQUEST_CHANGES; PR author equals gh user, so post_review posts as COMMENT with the TL;DR stating REQUEST_CHANGES and a footer explaining the fallback.
Result: review posted, blocker anchored inline with file:line evidence and the lazy fix (guard clause, three lines).

### Example 3: claims without evidence

User says: "review this PR". PR description says "fixes the race condition in the worker pool". No test touches the pool.
Actions: Pass E flags the claim; no repro or test exists; the finding becomes a 🟠 question asking for a failing-then-passing test, not an assertion that the fix is wrong.
Result: comment asks for evidence instead of speculating.

### Example 4: round 2

User says: "julgue de novo" after pushing fixes.
Actions: Step 0 finds the previous review; round 2. Resolution check maps the ledger: F1 fixed in commit `a1b2c3d`, F2 declined with a reason that holds (recorded declined-accepted), F3 still open. Diff since last review scanned for new blockers only; none found. `findings` is empty, `carryover` is `{"blocker": 1, "should-fix": 0}` for F3, verdict REQUEST_CHANGES.
Result: a short review with only the Resolution table and TL;DR. No new comments, no new fronts, convergence preserved.
