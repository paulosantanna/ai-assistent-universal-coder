<!-- Package: 00_skills/(quality)/the-judge; relative command/resource examples resolve from that package or workspace root. -->

## Convergence Contract

The Judge is decisive: it converges reviews instead of stretching them. Round 1 is exhaustive; every later round shrinks. The failure mode this contract kills is the infinite ping-pong where each round discovers a new front.

**Round N (N >= 2) scope is exactly two things:**

1. **Resolution check.** For every finding in the previous ledger, verify against the new commits: resolved (cite the fixing commit), still open, or declined by the author. Report all of them in the Resolution table. This is the focus of the re-review; it is a checklist verification, not a fresh hunt.
2. **New blockers only.** The diff since the last reviewed commit is examined solely for 🔴 introduced by the fix itself. No new 🟠, no new 🟡, no new 🟣, ever. Code that was visible in round 1 and not flagged then is forfeited: the reviewer eats the miss. The single exception is a genuine 🔴 (exploitable security, data loss, money) discovered late, which is always raised, labeled factually as missed in round 1.

**Declined findings.** When the author declines with a reason, first consider that they are closer to the code and may be right; if the reasoning holds from a code-health perspective, record declined-accepted and drop it permanently. If it does not hold, re-argue once with new evidence, at most once. Still unresolved after that: mark it open, state that the disagreement moves out of the review thread, and stop re-raising. Comment threads do not resolve philosophy.

**Round cap.** By round 3, every remaining open finding is either fixed, converted to a follow-up issue by agreement, or escalated out of the thread. The Judge never runs a fourth round on the same finding set.

**Approval bar.** Approve as soon as the PR definitely improves overall code health, even if imperfect; perfect code does not exist, only better code. Unresolved 🟡 never blocks an APPROVE (approve with nits). Withholding approval to extract polish beyond the severity table is scope creep by the reviewer.

The gate enforces the mechanical half of this contract: with `"round": 2` or higher it rejects any non-blocker finding, requires the Resolution section, and requires `carryover` so the verdict reflects still-open previous findings.
