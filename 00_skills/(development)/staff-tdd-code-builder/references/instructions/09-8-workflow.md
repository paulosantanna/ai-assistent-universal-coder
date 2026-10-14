<!-- Package: 00_skills/(development)/staff-tdd-code-builder; relative command/resource examples resolve from that package or workspace root. -->

## 8. Workflow

1. Create execution artifacts: `Memory`, `Handoff`, `progress`, `Learning`, `evidencias` and `analise`.
2. Read architecture handoff and reject implementation if the plan is missing or below 10/10.
3. Read project memory and dependency history.
4. Identify language-native build, lint, type, unit, integration, security and stress test commands.
5. Write tests before code unless the user explicitly ordered code first.
6. Make the initial tests fail for the right reason.
7. Implement the smallest code that satisfies the tests and architecture.
8. Refactor only within the approved architecture.
9. Inspect diff for forbidden outcomes:
   - source-code comments;
   - unused imports;
   - orphan variables;
   - dead code;
   - unrelated architecture changes;
   - tests weakened to pass.
10. Run vulnerability checks using multiple sources when dependency or generated stack is involved: NVD, OSV, GitHub Advisory Database, CISA KEV and ecosystem-native scanners.
11. Run tests that stress behavior, including positive, negative, boundary, edge, error-path, concurrency, resource and adversarial cases where applicable.
12. Run evaluator. If any category is below 10/10, rework. Do not mark ready.
13. Update documentation artifacts, learning and evidence outside source code.
14. Hand back to the integrator or documentation skill.
