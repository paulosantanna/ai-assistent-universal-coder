# Defects and adaptation

## Contents

- Findings
- Evidence
- Grade

## Findings

- Original `SKILL.md` has 208 physical lines. The TLC cap is 100, so the operational body moved to `references/procedure.md`.
- Original frontmatter keys: name, description, license, metadata.
- Original description had no `Do NOT use` boundary in the routing line.
- The opening persona 'You are a cuDF expert' was rewritten as a lens of codenavi-agent.
- Upstream tracks release 26.12. Treat that as a label in the source, then re-read VERSION before acting.

## Evidence

- Entrypoint pattern hits:
- L30: `You are a cuDF expert helping an implementer work with GPU DataFrames. The user understands pandas and their data — your job is to get them to correct, fast GPU code with minimal f`
- Sample of relative links that do not resolve inside the upstream package (0 total):
- None in the copied markdown set.
- Scripts left upstream, not vendored:
- `evals/files/cudf-apply-udf/code/generate_data.py`
- `evals/files/cudf-apply-udf/code/udf_pipeline.py`
- `evals/files/source-cudf-null-fillna-semantics/code/null_cleanup.py`
- `evals/files/cudf-pivot-melt/code/reshape_analysis.py`
- `evals/files/cudf-pivot-melt/code/generate_data.py`
- `evals/files/cudf-multi-join/code/multi_join.py`
- `evals/files/cudf-multi-join/code/generate_data.py`
- `evals/files/cudf-string-ops/code/generate_data.py`
- `evals/files/cudf-string-ops/code/clean_contacts.py`
- `evals/files/cudf-groupby-agg/code/groupby_analysis.py`
- `evals/files/cudf-groupby-agg/code/generate_data.py`
- `evals/files/cudf-timeseries-resample/code/timeseries_analysis.py`
- `evals/files/cudf-timeseries-resample/code/generate_data.py`
- `evals/files/cudf-null-handling/code/null_pipeline.py`
- `evals/files/cudf-null-handling/code/generate_data.py`
- `evals/files/cudf-parquet-io/code/generate_data.py`
- `evals/files/cudf-parquet-io/code/parquet_pipeline.py`
- `evals/files/negative-deep-learning-training/code/train.py`
- `evals/files/cudf-csv-etl/code/generate_data.py`
- `evals/files/cudf-csv-etl/code/etl_pipeline.py`
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
