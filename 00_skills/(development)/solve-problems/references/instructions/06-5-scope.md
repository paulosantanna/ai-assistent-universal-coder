<!-- Package: 00_skills/(development)/solve-problems; relative command/resource examples resolve from that package or workspace root. -->

## 5. Scope

### Included

- Identify the programming language from file extensions, manifests, lockfiles, shebangs, compiler output, stack traces and test configuration.
- Read repository memory before choosing a fix, using this priority:
  - `memory/shared/apis/<ORG>/<PROJECT>/<API_ACRONYM>/` when org, project and API acronym are known;
  - `memory/parents/<domain>/` for domain memory;
  - `memory/root/` for cross-domain constraints;
  - local skill memory and knowledge when repository memory is absent.
- Understand what the repository does, how it does it, when it does it, with whom it communicates and why the failing code exists.
- Create an execution bundle with these folders: `Memory`, `Handoff`, `progress`, `Learning`, `evidencias` and `analise`.
- Populate `evidencias/linha-do-tempo-worktree-git.md`, `evidencias/testes.md`, `evidencias/logs-pods.md`, `evidencias/telemetria-observabilidade.md` and `evidencias/evidence-index.md` when applicable.
- Populate `analise/plano-diagnostico-detalhado.md` and `analise/proposta-correcao.md` before implementation.
- Generate multiple viable correction proposals when the root cause has more than one plausible fix.
- Select the best proposal through the honest evaluator before applying code changes.
- Apply only minimal changes in the affected language and existing local style.
- Remove unused imports, orphan variables, dead local assignments and artifacts introduced by the fix.
- Run repository-native checks and tests for the affected language and blast radius.

### Excluded

- Comments in created or altered source code.
- Orphan variables, unused imports, dead local assignments or unused generated files.
- Project restructuring, architecture changes, package layout changes or framework replacement.
- Opportunistic cleanup unrelated to the reported problem.
- Test weakening, assertion removal, skipped failures or hiding flaky behavior.
- Claiming that no new bugs were introduced without executed verification evidence.
