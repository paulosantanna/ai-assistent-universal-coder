# Domain adapter: data analysis and reporting

Applies when the deliverable is insights, metrics, dashboards, or statistical summaries derived from datasets.

## Minimum evidence set (binding)

1. **The raw dataset or schema**: inspect schema, data types, null counts, and row counts before writing queries.
2. **Data freshness indicator**: timestamp/date range of data.
3. **Recomputable query/code**: exact code/SQL used to derive results.

## Verification by observation

- Row counts and sum checks match ground truth.
- Null values explicitly handled.
- Visualizations/tables reflect actual computed values.

## Fraud table (for fable-judge)

| Fraud | Symptom |
|---|---|
| Unchecked nulls | ignoring missing values in aggregations |
| Misleading metrics | using mean on skewed data without median |
| Unreproducible numbers | presenting charts/figures without code/SQL |
