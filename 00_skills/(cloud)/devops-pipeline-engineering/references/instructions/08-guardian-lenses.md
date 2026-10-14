<!-- Package: 00_skills/(cloud)/devops-pipeline-engineering; relative command/resource examples resolve from that package or workspace root. -->

## Guardian lenses

The skill may instantiate these bounded lenses/work units under `codenavi-agent`:

- `workflow-guardian`: one per relevant workflow run;
- `job-guardian`: one per job/matrix child;
- `github-actions-architecture`: workflow YAML, expressions, permissions, matrix and reusable workflows;
- `python-ci`: pytest, packaging, lint, typing and Python compatibility;
- `java-maven-ci`: Maven/JUnit/Surefire/Failsafe/JaCoCo;
- `java-gradle-ci`: Gradle wrapper/tasks/tests/caches;
- `node-ci`: npm/pnpm/yarn/Bun, TypeScript and frontend builds;
- `docker-ci`: Dockerfile/buildx/compose/registry/container smoke;
- `infrastructure-ci`: Terraform/Kubernetes/Helm validation without unauthorized deploy;
- `security-ci`: secret scanning, permissions, OIDC, supply chain and artifact integrity;
- `dependency-recovery`: lockfiles, constraints and dependency conflicts;
- `test-recovery`: deterministic reproduction, fixture isolation and flaky-test diagnosis;
- `performance-ci`: timeout, resource and cache analysis;
- `release-engineering`: artifacts, tags, bundles, provenance and release readiness;
- `branch-protection`: required checks and protection validation without bypass;
- `pr-governance`: review/readiness/merge evidence and the required Why/Porquê section;
- `rollback-recovery`: safe compensation plan;
- `token-economy`: compact evidence packets, cache and budget enforcement.

Each lens asks: **Would a Chief/Staff engineer of this specialization implement the fix this way, given root cause, architecture, security, maintainability, cost, observability, rollback and production impact?** Verdicts are `APPROVED`, `NEEDS_REWORK` or `REJECTED`.
