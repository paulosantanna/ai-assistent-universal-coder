<!-- Package: 00_skills/(quality)/the-judge; relative command/resource examples resolve from that package or workspace root. -->

## Severity and Verdict

| Severity | Emoji | Definition | Verdict effect |
|---|---|---|---|
| blocker | 🔴 | Changes whether the PR should merge: data loss, exploitable security, incorrect money, broken auth, irreversible migration, PII in logs | REQUEST_CHANGES |
| should-fix | 🟠 | Real defect, but not a merge risk | COMMENT |
| nit | 🟡 | Minor. Capped at 5 inline; overflow counted in summary | No effect |
| pre-existing | 🟣 | Bug the PR did not introduce. Summary only, never inline | No effect |

Verdict mapping: any 🔴 present, REQUEST_CHANGES. Zero 🔴 and zero 🟠, APPROVE. Anything else, COMMENT.

**Own-PR fallback:** GitHub returns 422 when you APPROVE or REQUEST_CHANGES your own PR. `scripts/post_review.py` detects when the PR author equals the authenticated `gh` user, posts as COMMENT, and appends a one-line footer at the end of the summary stating the intended verdict. The TL;DR already carries the verdict token, so the footer only explains the mechanics. Do not fight this; it is API behavior.
