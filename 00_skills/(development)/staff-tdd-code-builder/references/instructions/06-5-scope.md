<!-- Package: 00_skills/(development)/staff-tdd-code-builder; relative command/resource examples resolve from that package or workspace root. -->

## 5. Scope

### Included

- Read architecture plan, project memory and acceptance criteria before coding.
- Use TDD by default: write failing tests first, then code, then refactor.
- If the user explicitly requests code first, record the exception and create tests immediately after implementation.
- Generate simple code that follows local style and appropriate patterns.
- Use SOLID and design patterns only when they reduce real complexity.
- Screen dependencies and generated stack against multiple vulnerability sources.
- Create CI/CD, Docker, Kubernetes and GitHub Actions files only when the architecture handoff requires them.
- Add documentation artifacts outside source code, never source-code comments.
- Run stress-oriented, negative, edge, boundary, error-path, security and regression tests.

### Excluded

- Source-code comments in created or altered files.
- Tests that merely satisfy the implementation.
- Weakening tests, skipping failures or changing assertions outside the requirement.
- Arbitrary framework swaps, architecture changes or unrelated refactors.
- Adding dependencies without CVE and supply-chain review.
- Accepting a score below 10/10 as production-ready.
