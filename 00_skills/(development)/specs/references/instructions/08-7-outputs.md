<!-- Package: 00_skills/(development)/specs; relative command/resource examples resolve from that package or workspace root. -->

## 7. Outputs

Return a spec package with:

- `spec_id`, `revision`, `status` and `scope`;
- `requirements` with IDs, priority and source;
- `acceptance_criteria` linked to requirement IDs;
- `design` with architecture, data/interface impact, rollback and observability notes;
- `tasks` with dependencies, target files and expected verification;
- `test_matrix` covering required AEOS applicability categories;
- `approval_gates` for human, security, architecture and policy review;
- `evidence_gates` that downstream skills must satisfy;
- `blocking_conditions` and residual risks.
