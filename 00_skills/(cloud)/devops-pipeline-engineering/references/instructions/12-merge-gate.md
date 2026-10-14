<!-- Package: 00_skills/(cloud)/devops-pipeline-engineering; relative command/resource examples resolve from that package or workspace root. -->

## Merge gate

Default mode: `approval_required`.

Merge prerequisites:

- expected head SHA unchanged;
- all required checks successful on that SHA;
- branch protection satisfied;
- no unresolved mandatory review/environment gate;
- open PR body contains a verified Why/Porquê section (motivation/context for the worktree, not a placeholder);
- secret scan PASS;
- Judge PASS;
- Evidence Verify PASS;
- rollback/compensation documented.

Never merge using stale CI evidence.
