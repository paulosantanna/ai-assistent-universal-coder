<!-- Package: 00_skills/(architecture)/legacy-migration-planner; relative command/resource examples resolve from that package or workspace root. -->

## Workflow

Every engagement follows two mandatory phases. Never skip RESEARCH. Never start PLAN without completing RESEARCH.

```
RESEARCH (mandatory)                    PLAN (mandatory)
├─ 1. Codebase deep analysis            ├─ 5. Define migration direction
├─ 2. Domain/bounded context mapping    ├─ 6. Design seams and facades
├─ 3. Stack research (web + context7)   ├─ 7. Per-domain migration files
└─ 4. Risk and dependency mapping       └─ 8. Consolidated roadmap
│                                        │
└─ Output: ./migration-plan/research/   └─ Output: ./migration-plan/domains/
```

### RESEARCH Phase

Load `references/research-phase.md` for detailed instructions.

1. **Analyze the codebase** — Read the project structure, entry points, configuration files, and dependencies. Map every module and its responsibility. Cite every finding as `file:line`.
2. **Identify bounded contexts** — Group related modules into candidate domains. Load `references/assessment-framework.md` for the domain identification method.
3. **Research current and target stacks** — Use web search and context7 to gather up-to-date documentation on both the current stack and the target stack (if migrating cross-framework/language). Document version compatibility, migration guides, and known pitfalls.
4. **Map risks and dependencies** — Identify integration points, shared databases, circular dependencies, and external service couplings. Load `references/assessment-framework.md` for the risk matrix method.

Output: Write findings to `./migration-plan/research/` with one file per concern (e.g., `dependency-map.md`, `domain-candidates.md`, `stack-research.md`, `risk-assessment.md`).

### PLAN Phase

Load `references/plan-phase.md` for detailed instructions.

5. **Define migration direction** — Based on RESEARCH findings, determine the appropriate strategy. Load `references/strangler-fig-patterns.md` for pattern selection.
6. **Design seams and facades** — Identify where to cut the system. Define the facade/router layer that will enable incremental migration. Load `references/frontend-backend-strategies.md` for stack-specific patterns.
7. **Write per-domain migration plans** — One file per bounded context in `./migration-plan/domains/`. Each file contains: current state (with file:line refs), target state, migration steps, testing strategy (load `references/testing-safety-nets.md`), rollback plan, and success metrics.
8. **Write consolidated roadmap** — `./migration-plan/00-roadmap.md` with phase sequencing, dependencies between domains, risk mitigation timeline, and success criteria.
