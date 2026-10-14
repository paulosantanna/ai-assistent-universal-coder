<!-- Package: 00_skills/(architecture)/staff-iii-architecture-governor; relative command/resource examples resolve from that package or workspace root. -->

## 8. Workflow

1. Create execution artifacts: `Memory`, `Handoff`, `progress`, `Learning`, `evidencias` and `analise`.
2. Read project memory by org, repo, project and API acronym when available.
3. Classify greenfield versus existing architecture change.
4. Identify missing business-rule decisions and ask only those questions that cannot be safely inferred.
5. Dispatch isolated subagents:
   - language-technology-strategist;
   - architecture-style-strategist;
   - database-architect;
   - devsecops-ci-cd-architect;
   - kubernetes-docker-platform-architect;
   - cybersecurity-threat-modeler;
   - observability-slo-architect;
   - ui-ux-product-architecture-advisor when user-facing software exists.
6. Require each subagent to produce facts, options, tradeoffs, rejected alternatives and evidence.
7. Build a decision matrix with at least three viable architecture options when possible.
8. Choose the simplest architecture that satisfies requirements and production constraints.
9. Define database choice with explicit comparison across relational, document, cache, search, graph, time-series and vector storage where relevant.
10. Define CI/CD and GitHub Actions with secure defaults, artifact provenance, secret boundaries and dependency gates.
11. Define Docker and Kubernetes deployment only when it is justified by runtime and operational needs.
12. Define cybersecurity controls using authoritative baselines in `references/SOURCES.md`.
13. Run the extremely honest Architect Staff III evaluator.
14. If any criterion is below 10/10, return `REWORK_REQUIRED` and revise the architecture.
15. Hand off only a 10/10 architecture plan to `staff-tdd-code-builder` or the integrator playbook.
