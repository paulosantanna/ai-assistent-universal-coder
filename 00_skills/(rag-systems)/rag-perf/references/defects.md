# Defects and adaptation

## Contents

- Findings
- Evidence
- Grade

## Findings

- Original `SKILL.md` has 179 physical lines. The TLC cap is 100, so the operational body moved to `references/procedure.md`.
- Original frontmatter keys: name, version, description, license, compatibility, metadata, allowed-tools.
- Original description had no `Do NOT use` boundary in the routing line.
- Upstream links jump to `scripts/rag-perf` and docs outside the skill directory. Those targets are not in this package.

## Evidence

- Entrypoint pattern hits:
- L32: `allowed-tools: Read Grep Glob Bash(ls *) Bash(python3 *) Bash(uv *) Bash(cat *) Bash(curl *) Write Edit`
- Sample of relative links that do not resolve inside the upstream package (10 total):
- `references/config-schema.md -> ../../../scripts/rag-perf/rag_perf/config.py`
- `references/config-schema.md -> ../../../docs/performance-benchmarking.md`
- `references/config-schema.md -> ../../../scripts/rag-perf/rag_perf/query.py`
- `references/config-schema.md -> ../../../scripts/rag-perf/rag_perf/runner.py`
- `references/output-and-analysis.md -> ../../../scripts/rag-perf/rag_perf/runner.py`
- `references/output-and-analysis.md -> ../../../scripts/rag-perf/rag_perf/reporting.py`
- `references/output-and-analysis.md -> ../../../scripts/rag-perf/rag_perf/reporting.py`
- `references/synthetic-generation.md -> ../../../scripts/rag-perf/rag_perf/query.py`
- `references/synthetic-generation.md -> ../../../scripts/rag-perf/prompts/default_prompts.yaml`
- `references/synthetic-generation.md -> ../../../scripts/rag-perf/prompts/default_prompts.yaml`
- Scripts left upstream, not vendored:
- None.
- Signature files omitted: skill.oms.sig
- Eval, benchmark, and agent-identity files were not copied. They are not evidence for this workspace.

## Grade

Diagnostic rubric from `00_skills/(creation)/skill-architect/references/quality-checklist.md`. Not a measured routing accuracy.

| Dimension | Weight | Before | After |
| --- | --- | --- | --- |
| routing | 20 | 2 | 4 |
| procedure | 25 | 4 | 4 |
| examples | 15 | 4 | 4 |
| errors | 15 | 4 | 4 |
| disclosure | 15 | 2 | 4 |
| verification | 10 | 2 | 3 |

Before 62.0. After 78.0. Verification stays at 3 because this workspace did not rerun GPU, cluster, or clinical jobs.
