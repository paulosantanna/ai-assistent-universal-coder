<!-- Package: 00_skills/(architecture)/legacy-migration-planner; relative command/resource examples resolve from that package or workspace root. -->

## Output Structure

```
./migration-plan/
├── 00-roadmap.md                    # Consolidated roadmap, phases, timeline
├── research/
│   ├── dependency-map.md            # Module dependencies with file:line refs
│   ├── domain-candidates.md         # Identified bounded contexts
│   ├── stack-research.md            # Current + target stack analysis
│   └── risk-assessment.md           # Risk matrix with mitigations
└── domains/
    ├── 01-domain-{name}.md          # Per-domain migration plan
    ├── 02-domain-{name}.md
    └── ...
```
