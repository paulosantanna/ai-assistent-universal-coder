<!-- Package: 00_skills/(development)/architecturally-significant-requirement; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Example 1: Regulatory retention

User says: "É arquiteturalmente significativo reter dados de clientes por 10 anos por exigência regulatória?"
Actions: C1 (fines), C2 (compliance auditor), C4 (archive storage provider), C5 (every data store) are met; run the script.
Result: band `high`, `significant`; next step is an ADR on the archival storage and hosting model, citing ASR-007.

### Example 2: Pipeline automation

User says: "Do we need an ADR for automating the deployment pipeline?"
Actions: only C5 is met (team-internal, cross-cutting).
Result: band `low-medium`, `borderline`; discuss with the team, no ADR unless a hard-to-reverse tool choice follows.

### Example 3: Unknown partner SLA

User says: "Partners will call our pricing API at 10,000 requests per minute; we do not know their retry behavior."
Actions: C1 met; C3 and C4 are `?`; write the scenario with response measure "p95 under 300 ms at peak".
Result: `open`; spike the partner retry behavior, then rerun the test.
