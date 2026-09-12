# Playbook: tlc-catalog-skills

## Required agent

- `codenavi-agent` only.

## Required skills

Select the matching skill. Do not load the whole catalog by default.

- `not-your-babysitter` — autonomous evidence-or-stop execution
- `cursor-subagent-creator` — Cursor lens work units, never a new agent
- `skill-architect` — new skill design
- `technical-design-doc-creator` — architecture TDD
- `best-practices` — web security/compatibility/quality
- `the-fool` — challenge only
- `the-jury` — panel then verdict
- `ai-seo` — programmatic SEO / GEO
- `nx-workspace` — Nx monorepo explore/configure/affected/CI
- `subagent-creator` — generic lens work units, never a new agent; Cursor-only uses `cursor-subagent-creator`
- `tlc-plan` — cut a decided source into `.tasks/`; not discovery or implement
- `learning-opportunities` — optional teaching exercises; durable lessons via `learning-curator`
- `perf-astro` — Astro-only Lighthouse/critters/compress/LCP; not generic web perf
- `core-web-vitals` — LCP/INP/CLS remediations from measured evidence
- `perf-lighthouse` — run/parse Lighthouse and budgets; do not implement CWV here
- `perf-web-optimization` — generic page-speed/bundle/image/cache work
- `security-best-practices` — language/framework AppSec review with file:line evidence
- `security-ownership-map` — git ownership / bus factor; Python scripts; redact emails
- `security-threat-model` — repo-grounded abuse-path model; not a generic checklist
- `web-quality-audit` — multi-area perf/a11y/SEO/hygiene; specialists for single-area work

## Required LCPs

- `global-rules`
- `security-governance`

## Flow

1. Route to one skill from the list above.
2. Read that skill's `SKILL.md`, then `references/ORIGINAL_SKILL.md` when executing the original method.
3. Keep `owner_agent` as `codenavi-agent`. Jurors and Cursor specialists are lenses.
4. Run shipped Python gates when the skill declares them (`validate_skill.py`, `tally.py`).
5. Promote only verified durable facts into `.notebook/MEMORY.md`.

## Failure policy

A request to create another agent identity, persist secrets, or waive `specs`/security gates blocks completion.
