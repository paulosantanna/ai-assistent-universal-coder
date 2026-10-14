<!-- Package: 00_skills/(tooling)/github-operations; relative command/resource examples resolve from that package or workspace root. -->

## Pull request Why contract

Every open pull request MUST describe **why** the change exists, not only what changed. The Why/Porquê section is required so later worktrees, reviews and continuity notes keep adequate context.

Required body section (English `Why` or Portuguese `Porquê`/`Porque`):

```markdown
## Why
<motivation, problem, constraint or knowledge gap this change exists to solve>
```

Rules:

- `github.pull_request.create` and `github.pull_request.update` are blocked when the body lacks a Why/Porquê section, the section is empty, or it is a placeholder (`TBD`, `N/A`, `see title`, `see diff`).
- Why must explain motivation/context for the worktree. Restating the title or listing files is not sufficient.
- Merge readiness and merge execution inherit this gate. A green pipeline does not authorize merge when Why is missing.
- Do not invent a Why. If the operator cannot state why the change exists, stop and request that context.
