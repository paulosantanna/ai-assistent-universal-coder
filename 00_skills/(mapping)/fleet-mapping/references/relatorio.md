# Offline consolidation contract

Updated: 2026-10-13
Entry point: ../SKILL.md. Source: IMG_2737–IMG_2738.

Use templates/relatorio-santander.template.html and the report-design design-contract/design-tokens for real reports. Required result: full coverage totals, per-sigla cards, evidenced dependency graph, scoped glossary, date, wrapping complete cells, relevance search, freeze-grid, resizable columns, body-anchored tooltips, per-column filters and actual export behavior. A basic template is a starting point, not proof all interactions exist.
Keep CSS and application JavaScript local/inlined; no network requirement for opening the report. If Mermaid is used, vendor the verified build locally, initialize/render each diagram separately, and show a text fallback on error. The reference photos use Mermaid 9.4.3 UMD; preserve a project's already verified compatible vendor when applicable rather than silently downgrading it.
Official Santander fonts and flame logo were pictured but not supplied; do not fabricate them or claim a system font is official. Record chosen fallback and absent assets. XLSX is available only if implemented and behavior-checked; do not label CSV as XLSX.
Verify keyboard/focus, filters, complete exports, resize/wrapping and file:// behavior using the actual generated report. All branded data/claims require evidence. Fix the generator and verify deterministic regeneration instead of patching its emitted report.
