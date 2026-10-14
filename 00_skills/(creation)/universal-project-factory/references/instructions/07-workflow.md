<!-- Package: 00_skills/(creation)/universal-project-factory; relative command/resource examples resolve from that package or workspace root. -->

## Workflow

1. Validate required inputs and token budget before any broad planning.
2. Use `chromatic-decision` for architecture or deployment tradeoffs.
3. Use `project.plan`, `project.stack_matrix`, `project.scaffold_manifest` and `project.production_checklist`.
4. Use `project.scaffold_package` to generate concrete sandbox-first files.
5. Select language documentation MCPs only for the requested languages.
6. Write generated files only under approved sandbox output.
7. Emit `change-manifest.json`, `rollback-plan.json` and `rollback-plan.md` for generated files.
8. Require tests, CI, security, observability, deployment and rollback artifacts.
9. Stop with `REVIEW` when a human architecture, language or database decision is missing.
