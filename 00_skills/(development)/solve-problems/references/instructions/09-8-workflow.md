<!-- Package: 00_skills/(development)/solve-problems; relative command/resource examples resolve from that package or workspace root. -->

## 8. Workflow

1. Create or identify an execution ID and execution bundle.
2. Record the incoming objective in `Handoff/inbound.md` and initialize `progress/progress.md`.
3. Collect baseline evidence:
   - worktree status, branch and diff summary;
   - error report and failing command;
   - stack trace or logs;
   - pod logs when available;
   - telemetry and observability logs when available.
4. Identify affected language and tooling from repository evidence. Read `references/LANGUAGE_ROUTING.md` only when language-specific discovery is uncertain.
5. Read project memory before diagnosis. Prefer org, project and API acronym memory when known.
6. Read only relevant source files, tests, manifests and configuration needed to understand the defect.
7. Document the diagnostic plan in `analise/plano-diagnostico-detalhado.md`.
8. Reproduce the problem with a failing test or deterministic command when technically possible.
9. Build root-cause candidates and reject unsupported hypotheses with evidence.
10. Generate correction proposals. Each proposal must preserve architecture, avoid comments and remove orphan code.
11. Run the extremely honest evaluator from `evaluation/HONEST_EVALUATOR.md` against the proposals.
12. Select the best proposal and record it in `analise/proposta-correcao.md`.
13. Apply the smallest correction in the same language and existing style.
14. Inspect the diff for forbidden outcomes:
    - comments added to source code;
    - orphan variables;
    - unused imports;
    - architectural movement;
    - unrelated cleanup;
    - weakened tests.
15. Run language-native checks and tests. Use repository-native commands first.
16. Run broader regression checks when the change affects shared contracts or architecture-sensitive boundaries.
17. Update `evidencias/testes.md`, `Learning/learning.md`, `Memory/memory.md` and `Handoff/handback.md`.
18. Stop as `FAILED_VERIFICATION` when required checks fail and cannot be fixed inside scope.
19. Stop as `BLOCKED` when evidence, tools, permissions or memory scope are insufficient.
20. Complete only after verification supports the result and no blocking finding remains.
