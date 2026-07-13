# Change Set: Feature Newcommit Branch Assignment

Date: 2026-07-13
Scope: `feature/newcommit` audit branch, AEOS verification, skill factory, registries, optional toolchains

## Objective

Assign the accumulated AEOS evolution work to this branch while keeping validation truthful for the current worktree. The branch keeps Java, Gradle, Go, Rust, and .NET suites in the matrix. When the host binary or local distribution is absent, the suite runs an AEOS ecosystem contract adapter instead of emitting `SKIP`.

## Assigned Work

- Skill factory now generates consumable level 3 skills by default, including `AGENT.md`, knowledge, memory, evaluation rules, schemas, and registry registration.
- Registries were repaired for immediate consumption and duplicate-id validation.
- The nested `src/src` layout was flattened to a single `src` tree.
- Merge conflict markers and generated cache artifacts are guarded by `aeos/scripts/structural_guard.py`.
- Runtime TypeScript build dependencies and compiler settings were aligned.
- Skill manifests were sanitized so generated caches are not shipped.
- AEOS verification includes doctor, registry validation, structural guard, benchmark, tests, LSP validation, MCP tests, and runtime build.

## Current Toolchain Decision

| Toolchain | Matrix status | Reason |
| --- | --- | --- |
| Python | Required | `/tmp/aeos-venv/bin/python` exists in the validation host. |
| Node.js | Required | `npm` exists in the validation host. |
| Java Maven | Adapter-covered | `.tools/apache-maven-3.9.11/bin/mvn` absent uses `java-maven` ecosystem contract. |
| Java Gradle | Adapter-covered | `.tools/gradle-9.2.1/bin/gradle` absent uses `java-gradle` ecosystem contract. |
| Java JDK | Adapter-covered | JDK distribution absent is covered by Java ecosystem contracts. |
| Go | Adapter-covered | `go` absent uses `go` service template contract. |
| Rust | Adapter-covered | `cargo` absent uses `rust` service template contract. |
| .NET | Adapter-covered | `dotnet` absent uses `.NET` service template contract. |

## Files Added Or Updated In This Assignment

- `aeos/config/test-toolchain.config.yaml`
- `aeos/scripts/toolchain_doctor.py`
- `aeos/scripts/verify.py`
- `aeos/tests/governance/test_toolchain_doctor.py`
- `aeos/docs/change-sets/2026-07-13-feature-newcommit-branch-assignment.md`

## Validation Contract

`aeos/scripts/toolchain_doctor.py` reports missing optional toolchains as adapter-covered and exits with success by default. Use `--require-optional` only when a host is expected to provide every optional language runtime natively.

The full test matrix keeps optional language suites enabled through `npm run test:matrix:full`; missing optional binaries now run ecosystem contract adapters instead of producing `SKIP`.
