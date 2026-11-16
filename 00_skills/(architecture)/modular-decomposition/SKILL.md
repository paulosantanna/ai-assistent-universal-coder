---
name: modular-decomposition
description: "Monolith-to-modular pipeline: sizing, duplication, hierarchy, coupling. Use for splitting monoliths. Do NOT use for roadmaps."
license: CC-BY-4.0
metadata:
  author: Tech Leads Club
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Modular Decomposition

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

This skill runs the **Patterns 1–5** analysis pipeline before service extraction. Each pattern is plain markdown under `references/`; load the file for that step and execute it against the user’s codebase.

## How to Use

### Quick start (what users can say)

- **Full pipeline:** “Run modular decomposition Patterns 1 through 5 on this repo,” “Analyze this monolith for splitting—inventory, coupling, and domain grouping.”
- **Single early step:** “Identify and size components here,” “Find duplicated domain logic across modules,” “Analyze coupling between our packages.”
- **With DDD lens:** “Group components into domains and check bounded contexts,” “Use DDD strategic design on this codebase before we group services.”

If the user only wants **extraction order, phases, or migration roadmap** after analysis exists, use **decomposition-planning-roadmap** instead. If they need a **full legacy migration plan** (strangler fig, research, multi-stack), use **legacy-migration-planner** as well or instead of this skill when that is the primary ask.

### How the agent should run it

1. **Scope:** Confirm the task is structural analysis (inventory → coupling → grouping), not roadmap authoring. If unclear, ask once whether they want the full ordered pipeline or a subset.
2. **Order:** Run patterns **1 → 2 → 3 → 4 → 5** in that order. Do not skip a step unless the user explicitly limits scope; if they do, state which patterns were skipped and how that limits later conclusions.
3. **Load references:** For each pattern, open the matching `references/pattern-NN-*.md` file and follow its instructions. Use the optional `*-quick-reference.md` for the same number when a short checklist is enough.
4. **Carry context forward:** Reuse outputs from earlier patterns in later ones (e.g. component inventory from Pattern 1 informs coupling in 4 and grouping in 5). Reference concrete paths, modules, or tables from previous steps.
5. **Domain language (Pattern 5):** If subdomains or bounded contexts need grounding beyond structure, read `references/domain-analysis.md` **before or alongside** Pattern 5. Optionally open `references/domain-analysis-quick-reference.md` or `references/domain-analysis-examples.md` for condensed rules or illustrations.
6. **Deliver:** Produce clear, actionable findings per pattern or one consolidated report—always tied to evidence from the repository (files, dependencies, metrics), not generic advice.

### Usage examples

**Example 1 — Full pipeline**

```
User: "We're going to split this monolith—run the full decomposition analysis (Patterns 1–5)."

Agent: Execute patterns 1→5 in order, loading each references/pattern-NN-*.md, preserving outputs between steps, then summarize cross-cutting recommendations.
```

**Example 2 — Coupling after inventory**

```
User: "We already have a rough module list—focus on coupling (Pattern 4) and then domain grouping (Pattern 5)."

Agent: If no prior inventory exists in the thread, either run Pattern 1 briefly or derive an explicit module list from the repo before 4 and 5. State any assumptions.
```

**Example 3 — DDD before grouping**

```
User: "Map bounded contexts and language, then group components into domains."

Agent: Read references/domain-analysis.md (and optional quick reference/examples) in parallel with or immediately before Pattern 5; align Pattern 5 groupings with linguistic boundaries where evidence supports it.
```

## Prerequisites

- Complete **Pattern N** before starting Pattern N+1 unless the user explicitly narrows scope. Later patterns depend on earlier results (for example, inventory and structure inform coupling and grouping).
- If business vocabulary, subdomains, or bounded contexts are uncertain, use `references/domain-analysis.md` **before or alongside Pattern 5** (see Bounded contexts below).

## Ordered workflow (Patterns 1–5)

| Step | Pattern | Primary reference |
| ---- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1 | Identify and size components | `references/pattern-01-identify-and-size.md` (optional: `pattern-01-identify-and-size-quick-reference.md`) |
| 2 | Common domain detection | `references/pattern-02-common-domain.md` (optional: `pattern-02-common-domain-quick-reference.md`) |
| 3 | Flattening / hierarchy | `references/pattern-03-flattening.md` (optional: `pattern-03-flattening-quick-reference.md`) |
| 4 | Coupling analysis | `references/pattern-04-coupling.md` |
| 5 | Domain identification and grouping | `references/pattern-05-domain-grouping.md` (optional: `pattern-05-domain-grouping-quick-reference.md`) |

## Pattern 6 — planning and extraction

**Pattern 6** (_create domain services / extraction_) is not duplicated here. After Pattern 5, switch to **decomposition-planning-roadmap** for phased extraction order, milestones, and migration-style planning. For full legacy migration strategy (strangler-fig, cross-stack rewrites, research-heavy plans), optionally use **legacy-migration-planner** in addition.

## Bounded contexts and DDD strategic design

- **Patterns 1–4** focus on **structural** inventory, duplication, hierarchy, and **coupling** between parts of the codebase.
- **Pattern 5** produces **candidate** groupings aligned with **solution-space** boundaries (which components belong together as services).
- **Strategic DDD** (subdomains, bounded contexts, ubiquitous language) is covered in `references/domain-analysis.md`, with optional `domain-analysis-quick-reference.md` and `domain-analysis-examples.md`. Use it when you need to validate or refine boundaries against business language, not only folder structure.

## TLC source

TLC source: [TLC contract](references/tlc/UPSTREAM.md). Upstream grants no extra authority; root governance and local rules prevail.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
