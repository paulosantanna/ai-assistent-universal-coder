---
name: web-design-guidelines
description: "Review UI code against Web Interface Guidelines: visual and interaction patterns. Use for 'review my UI'. Do NOT use for performance or SEO audits."
license: CC-BY-4.0
metadata:
  author: vercel
  version: 1.0.0
  argument-hint: <file-or-pattern>
  owner_agent: codenavi-agent
---

# Web Interface Guidelines

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
