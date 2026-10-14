<!-- Package: 00_skills/(development)/documentation; relative command/resource examples resolve from that package or workspace root. -->

## Complete Documentation Workflow

Use this workflow only when the user asks for complete, architectural, onboarding, operational or system documentation.

1. Inspect authorized repository evidence before making architecture claims.
2. Call `complete-docs` with `docs.plan` or `docs.package` to define required sections, evidence and diagrams.
3. Call `docs.architecture_package` when the request asks for complete architecture documentation, AI workspace engineering, cloud maturity or deployment readiness.
4. Generate Mermaid diagrams for architecture, runtime flow, skill/MCP/LSP routing, dependencies and cloud readiness when the requested documentation is complete.
5. Validate every Mermaid block with `docs.validate_mermaid` before finalizing.
6. Include README, architecture, runtime flow, skills/MCPs/LSPs, cloud readiness and ADR artifacts when using the architecture package workflow.
7. Keep diagrams compact; split large graphs by concern instead of producing unreadable diagrams.
8. Place generated documentation only in approved report or sandbox locations.
