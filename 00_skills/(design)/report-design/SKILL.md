---
name: report-design
description: Apply the pictured offline report layout with semantic theme tokens, complete grids, tooltips, filters/export, drill-down and accessible diagrams. Use when the user says melhorar o relatório HTML, tabela sem filtro or relatório regrediu. Do NOT use for data collection (fleet-mapping), schema changes, skill evaluation, or meeting media (acta-aurea).
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Report Design

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Apply the pictured offline report layout with semantic theme tokens, complete grids, tooltips, filters/export, drill-down and accessible diagrams.

## Workflow

1. Inspect the report generator, real data/schema, chosen brand assets and current rendered HTML before changing the design.
2. Read [design-contract](references/design-contract.md) and [design-tokens](references/design-tokens.md); keep brand, action, error and risk colors as separate roles.
3. Put local assets beside the output; generate HTML from the source template, with complete data, headers/tooltips, per-column filters and explicit CSV/XLSX capability.
4. Preserve drill-down/back navigation and isolate each Mermaid render; reserve diagram height before restoring anchors.
5. Run structural checks and real headless browser inspection of keyboard focus, reduced motion, overflow, export/filter behavior and offline requests.
6. Regenerate twice from the same source; compare bytes. Fix the generator rather than editing emitted HTML.

## Rules

- No silent row/cell truncation. A declared top N must show N and the total.
- Do not claim branded fonts/logo or XLSX functionality is present unless actual assets and implementation exist.
- Explanatory panels are additive and must not change data; preserve readable wrapping instead of collapsing a column to one character.

## Inputs and outputs

Inputs: the user-requested target, authorized source paths/access, scope and expected result.

A regenerated portable report, used asset paths, design check results, browser observations and explicit unavailable capabilities.

## Verification and stop

Verify the actual outputs and relevant contract checks. Missing evidence, dependency, source asset, input or permission blocks its dependent stage; report the precise gap.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
