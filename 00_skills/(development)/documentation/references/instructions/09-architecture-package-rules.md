<!-- Package: 00_skills/(development)/documentation; relative command/resource examples resolve from that package or workspace root. -->

## Architecture Package Rules

- Produce `README.md`, `docs/ARCHITECTURE.md`, `docs/RUNTIME_FLOW.md`, `docs/SKILLS_MCPS_LSPS.md`, `docs/CLOUD_READINESS.md` and ADR candidates for complete architecture packages.
- Treat cloud readiness as a gated review, not as a deployment approval.
- Mark every readiness dimension as `PASS`, `REVIEW` or `BLOCKED` from evidence only.
- Require ADR candidates for architecture, runtime, Tool Router, MCP, LSP, security or deployment decisions.
- Stop with `REVIEW` when the package can be generated but maturity evidence is incomplete.
