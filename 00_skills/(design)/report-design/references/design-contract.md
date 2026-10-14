# Offline report design contract

Updated: 2026-10-12
Source: IMG_2214–IMG_2222, IMG_2322–IMG_2324 and IMG_2444–IMG_2452.

Read while implementing or reviewing the report generator.

1. Carry authorized CSS, JS, logo and fonts locally with relative URLs; a self-contained HTML may inline CSS/JS. No silent CDN dependency.
2. Distinguish brand/action/error/status tokens from `design-tokens.md`. Preserve the user's chosen brand; missing official assets are a gap, not permission to invent them.
3. Every grid keeps complete values, readable wrapping, descriptions and body-anchored tooltips that cannot be clipped by overflow. Never collapse compact columns to one character.
4. Provide declared per-column value filtering, sort, AND across filters, clear/reset, frozen headers and export. Verify CSV escaping and XLSX file contents if XLSX is offered; a renamed CSV is not XLSX.
5. A row/cell limit must be explicit with both shown and total counts. Preserve the underlying complete data; explanations are additive `<details>` panels.
6. Drill-down reveals contributing repositories/journeys and has a return route preserving position. Anchor restoration waits for asynchronous diagrams and reserved height.
7. Render each Mermaid diagram independently; shared initialization must not leak entities between ER diagrams. Include legends and supported zoom/pan/fullscreen/node search.
8. Interactive controls have visible keyboard focus and accessible names. Respect reduced motion and user contrast; test small screens, zoom and table overflow.
9. KPI counts, risk colors, dependency edges and version provenance come from the source data. Unknown CVE/EOL state is distinct from a safe state.
10. Regeneration from identical inputs must be byte-identical. Edit generator/template/assets, then rebuild; never fix emitted HTML alone.

Verification records HTML/asset hashes, no offline network requests, real keyboard/filter/export/drill behavior, representative browser screenshots and exact failures. Missing implementations/assets must be reported before claiming the full contract passed.
