<!-- Package: 00_skills/(tooling)/mermaid-studio; relative command/resource examples resolve from that package or workspace root. -->

## Golden Rules — Elegant Diagrams by Default

Every diagram MUST follow these principles. They are not optional — they define the difference between a mediocre diagram and a gold-standard one.

### Rule 1: Always Use an Init Directive for Professional Styling

**NEVER** create a diagram without an `%%{init}` directive or frontmatter config. The default Mermaid theme produces harsh black lines and generic colors. Always apply a curated palette.

**For general diagrams (flowchart, sequence, state, class, ERD):**

```
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#4f46e5', 'primaryTextColor': '#ffffff',
  'primaryBorderColor': '#3730a3', 'lineColor': '#94a3b8',
  'secondaryColor': '#10b981', 'tertiaryColor': '#f59e0b',
  'background': '#ffffff', 'mainBkg': '#f8fafc',
  'nodeBorder': '#cbd5e1', 'clusterBkg': '#f1f5f9',
  'clusterBorder': '#e2e8f0', 'titleColor': '#1e293b',
  'edgeLabelBackground': '#ffffff', 'textColor': '#334155'
}}}%%
```

**⚠️ Font Warning:** Do NOT set `fontFamily` in theme variables. The Mermaid default font (`trebuchet ms, verdana, arial, sans-serif`) works everywhere. Setting `system-ui`, `Segoe UI`, or `-apple-system` will render as Times New Roman in headless Chromium (used by `mmdc`).

**For C4 diagrams — see the dedicated C4 styling section below.**

**For architecture-beta diagrams — see the dedicated AWS/Architecture section below.**

### Rule 2: Soft Lines, Never Harsh Black

The single biggest visual improvement is using `lineColor: '#94a3b8'` (slate-400) instead of the default black. This creates a modern, breathable diagram. For dark themes, use `lineColor: '#64748b'` (slate-500).

### Rule 3: Limit Density — Breathe

- Maximum 15 nodes per diagram (not 20 — fewer is more elegant)
- Use `subgraph` or boundaries to create whitespace and visual grouping
- Prefer LR (left-right) for process flows — it reads more naturally
- Use invisible links (`A ~~~ B`) to add spacing when the layout is cramped

### Rule 4: Meaningful Labels and Consistent Style

- Node IDs: camelCase (`orderService`, not `s1` or `os`)
- Labels: short, clear natural language (`[Order Service]`)
- Arrows: action verbs with protocol info (`"Sends order via gRPC"`)
- Descriptions: one-line, role-focused (`"Handles order lifecycle"`)

### Rule 5: Color Harmony Over Color Variety

Use max 3-4 colors per diagram. Map colors to meaning:

- **Blue tones** (#4f46e5, #3b82f6) → primary systems, internal services
- **Green tones** (#10b981, #059669) → success states, data stores
- **Amber tones** (#f59e0b, #d97706) → external systems, warnings
- **Slate tones** (#64748b, #94a3b8) → lines, borders, secondary elements
- **Red tones** (#ef4444) → errors ONLY, never as decoration
