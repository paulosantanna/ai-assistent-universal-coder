# Skill: kinghost-data-analysis

## Mission
Analyze databases and operational/site data on authorized KingHost environments without allowing analysis to become uncontrolled mutation.

## Uses MCP
- kinghost-commerce

## Scope
SQL databases, supported document databases, application logs, access/error logs, commerce catalog/order/inventory datasets and server/application metrics exposed by the authorized environment.

## Capabilities
- Schema/entity/relationship discovery.
- Data profiling: cardinality, nulls, duplicates, distributions and anomalies.
- Query analysis with EXPLAIN/EXPLAIN ANALYZE when safe.
- Index and query optimization recommendations.
- Referential-integrity and consistency analysis.
- Commerce reconciliation: SKU, price, inventory, order and fulfillment divergence.
- Time-series analysis of traffic/errors/latency/resource consumption.
- Generate read-only SQL/query plans and evidence-backed reports.

## Safety Contract
Read-only by default. DML/DDL is not data analysis and must be delegated to an approved mutation/migration workflow. Never SELECT or export credential/secret columns merely because they are queryable. Minimize PII and redact durable evidence.

## Required Inputs
- session_ref
- data_scope
- analysis_objective
- sensitivity_classification

## Output Schema
```json
{"status":"PASS|WARN|BLOCKED","datasets":[],"quality_findings":[],"query_findings":[],"performance_findings":[],"business_findings":[],"recommendations":[],"evidence_refs":[]}
```

## Quality Gates
Queries bounded; sensitive columns excluded/minimized; claims tied to query/metric evidence; sampling explicitly identified; recommendations separate from mutations.
