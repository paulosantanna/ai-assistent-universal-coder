# Change Set: Performance Benchmark Gate

Date: 2026-07-13
Scope: Add a measurable AEOS performance benchmark gate for hot-path regression control.
Status: Verified with available runtime; pytest unavailable in this session.

## Summary

This change set turns AEOS performance work into an executable gate:

- Adds `PerformanceBenchmarkRunner` for deterministic quick benchmarks.
- Adds `aeos performance benchmark` CLI command.
- Adds JSON and Markdown benchmark reports under `.aeos/reports/performance`.
- Adds `--fail-on warn|breach` so local runs can be strict while CI/verify blocks only on budget breach.
- Adds the benchmark step to `aeos/scripts/verify.py`.
- Adds performance benchmark to enterprise CI gate config.
- Adds tests for the runner and CLI command.

## Files Changed In This Change Set

| File | Change | Current SHA-256 |
| --- | --- | --- |
| `aeos/core/performance/benchmark_runner.py` | New deterministic performance benchmark runner. | `8b8b6c33a191481840dfd38dd5469a7d7f89d34db81b9e98466b9883a60ea1a0` |
| `aeos/cli/commands/performance.py` | New CLI command for performance benchmarks. | `0a1a9e630d9dc5a73ae9cfb68822dc54433d992c59bfb12a3d0c71eae6b2c037` |
| `aeos/cli/main.py` | Registered `performance benchmark` command and options. | `3fff2970570050b9c78ee132df08503141599d9fa496ea8680e1cf43f3a13404` |
| `aeos/scripts/verify.py` | Added performance benchmark gate before core tests. | `a3f3cb69135bade1c0e3eca5ed150fb77198a43d4f8ae0c431b9f48239c19afe` |
| `aeos/tests/enterprise/test_performance_benchmark_runner.py` | New benchmark runner tests. | `6ef325045e7758cc884fcdcad3a5cca85b2e2f0fdadf682eb596c6a68426c30b` |
| `aeos/tests/cli/test_cli_performance.py` | New CLI benchmark test. | `dc4cd12abec75351e4351110a7ea95b9b7339067bd66366618a36b64c07fe040` |
| `aeos/config/performance-budgets.yaml` | Added scanner benchmark and suite budgets. | `5f8ae54a873f22dbbe9ffe032f6112e9c353008f653fae21bd55ebe21b843b5a` |
| `aeos/config/enterprise-ci-gates.yaml` | Added `performance_benchmark` and `performance_budget_breach` gate entries. | `7d11fd55a6c8a5e43a1925a4d60b81ce4c3e3190514978839f8d6de636cb8ff1` |

## Benchmark Cases

| Case | Purpose |
| --- | --- |
| `registry_load` | Measures cold skill registry load and YAML parse path. |
| `skill_contract_load` | Measures cached skill contract resolution. |
| `scanner_pruned` | Measures pruned repository scan behavior. |
| `evidence_batch_write` | Measures batched evidence and hash-chain writes. |

## Rollback Plan

Rollback this change set as a single group.

1. Remove these new files:
   - `aeos/core/performance/benchmark_runner.py`
   - `aeos/cli/commands/performance.py`
   - `aeos/tests/enterprise/test_performance_benchmark_runner.py`
   - `aeos/tests/cli/test_cli_performance.py`
   - `aeos/docs/change-sets/2026-07-13-performance-benchmark-gate.md`
2. Revert only the benchmark/gate hunks in:
   - `aeos/cli/main.py`
   - `aeos/scripts/verify.py`
   - `aeos/config/performance-budgets.yaml`
   - `aeos/config/enterprise-ci-gates.yaml`
3. Re-run syntax, registry and benchmark smoke checks.

Do not use broad reset commands because the worktree contains unrelated AEOS evolution changes from earlier phases.

## Validation

Commands executed:

```bash
python -m py_compile aeos/core/performance/benchmark_runner.py aeos/cli/commands/performance.py aeos/cli/main.py aeos/scripts/verify.py aeos/tests/enterprise/test_performance_benchmark_runner.py aeos/tests/cli/test_cli_performance.py
python -m aeos.cli.main registry validate
python -m aeos.cli.main performance benchmark --aeos-root . --target /tmp/aeos-benchmark-smoke --iterations 1 --fail-on breach --json
npm run build
python aeos/scripts/verify.py --suite quick --python python
```

Results:

- Python compile: PASS
- YAML load check: PASS
- Registry validation: PASS, 189 entries across 5 types
- Benchmark smoke: PASS
- Manual execution of new test functions: PASS
- Runtime build: PASS
- `verify.py --suite quick`: doctor, registry and benchmark PASS; core pytest step could not run because `pytest` is not installed in this session's Python environment.

Pytest-specific note:

- `python -m pytest --version` failed with `No module named pytest`.
- No alternate Python with pytest was found under `/tmp` or `/workspace`.
- The missing pytest dependency is an environment limitation in this session, not a benchmark gate failure.
