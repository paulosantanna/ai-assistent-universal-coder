<!-- Package: 00_skills/(tooling)/mermaid-studio; relative command/resource examples resolve from that package or workspace root. -->

## Step 1: Understand the Request

Before writing any Mermaid code, determine:

1. **What to diagram** — system, flow, schema, architecture, code structure?
2. **Which diagram type** — use the Decision Matrix below
3. **Output format** — code only, SVG, PNG, or ASCII?
4. **Theme preference** — ask only if rendering; default to `base` theme with curated palette

### Diagram Type Decision Matrix

| User describes...                              | Diagram Type  | Syntax keyword       |
| ---------------------------------------------- | ------------- | -------------------- |
| Process, algorithm, decision tree, workflow    | Flowchart     | `flowchart TD/LR`    |
| API calls, message passing, request/response   | Sequence      | `sequenceDiagram`    |
| Database schema, table relationships           | ERD           | `erDiagram`          |
| OOP classes, domain model, interfaces          | Class         | `classDiagram`       |
| State machine, lifecycle, transitions          | State         | `stateDiagram-v2`    |
| High-level system overview (C4 Level 1)        | C4 Context    | `C4Context`          |
| Applications, databases, services (C4 Level 2) | C4 Container  | `C4Container`        |
| Internal components (C4 Level 3)               | C4 Component  | `C4Component`        |
| Request flows with numbered steps              | C4 Dynamic    | `C4Dynamic`          |
| Infrastructure, cloud deployment               | C4 Deployment | `C4Deployment`       |
| Cloud services with icons (AWS/GCP/Azure)      | Architecture  | `architecture-beta`  |
| Project timeline, scheduling                   | Gantt         | `gantt`              |
| Proportional data, percentages                 | Pie           | `pie`                |
| Brainstorming, hierarchical ideas              | Mindmap       | `mindmap`            |
| Historical events, chronology                  | Timeline      | `timeline`           |
| Branching strategy, git history                | Git Graph     | `gitGraph`           |
| Flow quantities, resource distribution         | Sankey        | `sankey-beta`        |
| X/Y data visualization                         | XY Chart      | `xychart-beta`       |
| Priority matrix, strategic positioning         | Quadrant      | `quadrantChart`      |
| Layout control, grid positioning               | Block         | `block-beta`         |
| Network packets, protocol headers              | Packet        | `packet-beta`        |
| Task boards, kanban workflow                   | Kanban        | `kanban`             |
| User experience, satisfaction scoring          | User Journey  | `journey`            |
| System requirements traceability               | Requirement   | `requirementDiagram` |

If the user's description doesn't clearly map to one type, suggest 2-3 options with a brief rationale for each, then let them choose.

### When to Load References

Load reference files ONLY when needed for the specific diagram type:

- **C4 diagrams** → Read `references/c4-architecture.md` BEFORE writing code
- **AWS/Cloud architecture** → Read `references/aws-architecture.md` BEFORE writing code
- **Code-to-diagram** → Read `references/code-to-diagram.md` BEFORE analyzing
- **Theming/styling** → Read `references/themes.md` when user requests custom themes
- **Syntax errors** → Read `references/troubleshooting.md` when validation fails
- **Any diagram type details** → Read `references/diagram-types.md` for comprehensive syntax
