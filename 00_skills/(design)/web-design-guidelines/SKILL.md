---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices". Focuses on visual design and interaction patterns. Do NOT use for performance audits (use core-web-vitals), SEO (use seo), or comprehensive site audits (use web-quality-audit).
license: CC-BY-4.0
metadata:
  author: vercel
  version: 1.0.0
  argument-hint: <file-or-pattern>
  owner_agent: codenavi-agent
---

# Web Interface Guidelines

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Read the guidelines from `#[[file:references/guideline.md]]`
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the guidelines
4. Output findings in the terse `file:line` format

## Guidelines Reference

All rules and output format instructions are in:

```
#[[file:references/guideline.md]]
```

The guidelines cover:

- Accessibility (ARIA, semantic HTML, keyboard navigation)
- Focus states and keyboard interaction
- Forms (autocomplete, validation, labels)
- Animation (reduced motion, performance)
- Typography (proper characters, number formatting)
- Content handling (overflow, empty states)
- Images (dimensions, lazy loading)
- Performance (virtualization, DOM reads)
- Navigation & state (URL sync, deep linking)
- Touch & interaction (tap delays, safe areas)
- Dark mode & theming
- Locale & i18n
- Hydration safety
- Common anti-patterns to flag

## Usage

When a user provides a file or pattern argument:

1. Read the guidelines from `references/guideline.md`
2. Read the specified files
3. Apply all rules from the guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

## Output Format

Follow the format in the guidelines:

- Group findings by file
- Use `file:line` format (VS Code clickable)
- Terse, high signal-to-noise
- State issue + location
- Skip explanation unless fix is non-obvious

## TLC source

For the catalog workflow and its local resources, read [TLC contract](references/tlc/UPSTREAM.md). Apply root governance and the local constraints above; upstream does not grant extra authority.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
