<!-- Package: 00_skills/(quality)/the-judge; relative command/resource examples resolve from that package or workspace root. -->

## Troubleshooting

### Error: HTTP 422 on review submission
Cause: APPROVE/REQUEST_CHANGES on your own PR, or a comment anchored to a line not in the diff.
Solution: `post_review.py` auto-falls back to COMMENT for own PRs. For anchor failures, move the comment to a changed line shown in the patch, or drop `line` and fold it into the summary.

### Error: gh not authenticated
Cause: no `gh auth login` session.
Solution: ask the user to run `gh auth status` and authenticate. Do not attempt tokenless calls.

### Error: no PR for the current branch
Cause: branch never pushed or PR not opened.
Solution: report it and stop. Opening PRs is out of scope for The Judge (that is a different job).

### Gate keeps failing on the same body
Cause: rephrasing around a banned pattern instead of removing it.
Solution: delete the sentence containing the violation. The gate output names the exact pattern and location.
