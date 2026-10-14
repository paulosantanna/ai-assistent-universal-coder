<!-- Package: 00_skills/(development)/tlc-spec-driven; relative command/resource examples resolve from that package or workspace root. -->

## Context Loading Strategy

**On-demand load (only what the current task needs):**

- `.specs/STATE.md` - Decisions section (read at Design, re-read on resume); Handoff section (read on resume only)
- confirmed lessons - load at Specify and Design via `python3 <skill-dir>/scripts/lessons.py list --status confirmed` ([lessons.md](../tlc/references/lessons.md)); confirmed only, never candidates
- spec.md (when working on a specific feature)
- context.md (when designing or implementing from user decisions)
- design.md (when implementing from design)
- tasks.md (when executing tasks)

**Never load simultaneously:**

- Multiple feature specs
- Multiple architecture docs

**Target:** <40k tokens total context
**Reserve:** 160k+ tokens for work, reasoning, outputs
**Monitoring:** Display status when >40k (see [context-limits.md](../tlc/references/context-limits.md))
