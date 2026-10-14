<!-- Package: 00_skills/(development)/java-bug-solver; relative command/resource examples resolve from that package or workspace root. -->

## Mandatory Deep Bug Analysis Before Planning

Before creating any plan, patch proposal or implementation, this bug-solver MUST complete a deep evidence-first diagnostic for each destination API, project or acronym.

### Required destination workspace

Create or update one governed workspace per destination using this layout:

```text
.aeos/bug-solver/<api-projeto-sigla>/
|-- references/package-notes.md
|-- HANDOFF.md
|-- LEARNING.md
|-- MEMORY.md
|-- PROGRESS.md
|-- evidencias/
|   +-- linha-do-tempo-runs.md
+-- analise/
    |-- Diagnostico.md
    +-- PROPOSTA_CORRECAO.md
```

The destination identifier MUST be derived from explicit repository, API, project or acronym evidence. If it is ambiguous, stop with `BLOCKED` or `REVIEW` and record the ambiguity in `PROGRESS.md`.

### Required analysis before any plan

The diagnostic MUST run before any plan exists and MUST include:

- all local branches, remote branches and refs that are authorized for inspection;
- all commits reachable from all branches, using commands such as `git log --all` or repository-native equivalents;
- every worktree from `git worktree list`, including path, branch, commit and cleanliness state when accessible;
- all available GitHub Actions runs for the destination repository, recorded in `evidencias/linha-do-tempo-runs.md` together with worktree evidence;
- command, file, test, trace or run evidence explaining what is generating each observed error;
- top-down exception-chain analysis, from the outermost symptom through causal frames and wrapped exceptions to the evidence-backed root cause;
- project-layer analysis covering entrypoint/API, application flow, domain rules, data/schema, infrastructure, build/runtime, tests/CI and observability.

If GitHub Actions, branches, commits, worktrees or required history are unavailable because of permissions, missing tools or network limits, do not invent them. Record the exact blocker, attempted command or source, residual risk and required approval in `PROGRESS.md` and `HANDOFF.md`.

### Mandatory independent subagents

Use separate subagents before planning so diagnosis, correction and review do not share a single conflict-prone context. At minimum separate these responsibilities when the platform supports subagents:

- git-history/worktree investigator;
- runtime traceback and top-down exception-chain analyst;
- layer-by-layer root-cause analyst;
- correction proposal and verification planner;
- independent Judge reviewer.

Each subagent MUST receive a scoped handoff and return evidence references. The agent proposing the correction MUST NOT approve its own proposal.

### Artifact requirements

- `HANDOFF.md`: every handoff, scope, assumptions, forbidden paths, evidence refs, stop conditions and acknowledgement.
- `LEARNING.md`: candidate lessons only, clearly separated from validated knowledge.
- `MEMORY.md`: execution memory, decisions, failures, open risks and provenance for this destination.
- `PROGRESS.md`: chronological progress, commands attempted, blockers, retries, omissions and current status.
- `references/package-notes.md`: destination summary, scope, how to read the evidence bundle and current status.
- `evidencias/linha-do-tempo-runs.md`: complete timeline of inspected worktrees and GitHub Actions runs, with timestamps, refs, run IDs/statuses when available and evidence links.
- `analise/Diagnostico.md`: facts, symptoms, top-down exception chain, layer analysis, rejected hypotheses and evidence-backed root cause.
- `analise/PROPOSTA_CORRECAO.md`: proposed fix, blast radius, tests, rollback/roll-forward plan and traceability from root cause to each change.

### Planning gate

A patch plan or correction proposal may be created only after `Diagnostico.md`, `evidencias/linha-do-tempo-runs.md` and the required subagent handoffs exist or are explicitly blocked with evidence. Missing evidence is `UNVERIFIED`; it is not permission to continue silently.
