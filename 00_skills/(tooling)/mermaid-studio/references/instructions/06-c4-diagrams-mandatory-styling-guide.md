<!-- Package: 00_skills/(tooling)/mermaid-studio; relative command/resource examples resolve from that package or workspace root. -->

## C4 Diagrams — Mandatory Styling Guide

C4 diagrams have **fixed element styling** (blue boxes for systems, gray for persons, etc.), but their **relationship lines default to harsh black** which creates visual noise. You MUST apply these styling rules:

### The C4 Styling Pattern

Every C4 diagram MUST include these directives at the end:

```
    %% === MANDATORY STYLING ===
    %% Apply soft line colors to ALL relationships
    UpdateRelStyle(fromAlias, toAlias, $textColor="#475569", $lineColor="#94a3b8")
    %% Repeat for each Rel() in the diagram

    %% Optimize layout spacing
    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

### C4 Color Values Reference

| Purpose           | Color     | Hex       | Notes                                    |
| ----------------- | --------- | --------- | ---------------------------------------- |
| Soft line color   | Slate-400 | `#94a3b8` | Replaces harsh default black             |
| Line text color   | Slate-600 | `#475569` | Readable but not dominant                |
| Accent line       | Blue-400  | `#60a5fa` | For highlighted or primary relationships |
| Warning line      | Amber-500 | `#f59e0b` | For external/risky connections           |
| Custom element bg | Emerald   | `#10b981` | For data stores or success highlights    |
| Custom element bg | Indigo    | `#4f46e5` | For primary system emphasis              |

### C4 Layout Tips

**CRITICAL — Maximum 6 `Rel()` per diagram.** More than 6 relationships causes Dagre to route arrows through nodes, creating unreadable spaghetti. If your system needs more connections, split it into multiple focused diagrams.

- Use `$c4ShapeInRow="3"` for most diagrams (prevents horizontal crowding)
- Use `$c4ShapeInRow="2"` for diagrams with long labels
- Use `$c4BoundaryInRow="1"` always (stacks boundaries vertically for clarity)
- Apply `$offsetY="-10"` to `UpdateRelStyle` when labels overlap with elements
- Prefer tree-shaped topologies (1 in, 1-2 out per node) over mesh topologies
- Declare elements in flow order — the order of `Container()` declarations affects layout
- Use directional `Rel_D`, `Rel_R`, etc. only as a last resort when auto-layout creates overlapping

For comprehensive C4 syntax, examples, and patterns, read `references/c4-architecture.md`.
