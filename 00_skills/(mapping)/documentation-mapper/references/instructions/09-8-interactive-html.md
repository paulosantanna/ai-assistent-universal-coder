<!-- Package: 00_skills/(mapping)/documentation-mapper; relative command/resource examples resolve from that package or workspace root. -->

## 8. Interactive HTML

The HTML output must:

1. Be a single self-contained file (all CSS/JS inline or linked locally)
2. Contain a navigation sidebar with all layers and views
3. Display Mermaid diagrams that are **clickable**:
   - Clicking an entity in diagram A navigates to diagram B where that entity is detailed
   - Clicking a database collection shows its schema
   - Clicking a service shows its API endpoints
   - Clicking an entity highlights all connected entities (drill-down expansion)
4. Include a search bar for full-text search across the entire documentation
5. Include a data dictionary section with expandable tables
6. Include all three stakeholder views as tabbed sections
7. Be responsive (desktop + tablet)
8. Include an "Improvement Plan" tab with the roadmap diagram
9. Export to PDF from the browser via `window.print()`

---
