# Examples

## Examples

**Profile-only (quickest signal on retrieval / reranker tuning):**

```bash
uv run --project scripts/rag-perf rag-perf -c scripts/rag-perf/configs/quick_profile.yaml
```

Output: `rag-perf-results/quick_profile/run_<ts>/{profile_report.md, profile_results.json, profiling/}`. The `aiperf_rag_on/` directory is omitted. Filenames are `profile_*` because `aiperf.enabled: false`.

**Single benchmark point with full report:**

```bash
uv run --project scripts/rag-perf rag-perf -c scripts/rag-perf/configs/single_run.yaml
```

Output: flat `run_<ts>/{report.md, results.json, results.csv, profiling/, aiperf_rag_on/}`.

**Concurrency sweep:**

```bash
uv run --project scripts/rag-perf rag-perf -c scripts/rag-perf/configs/sweep.yaml
```

Output: nested `run_<ts>/iter_1/<CR:_VDB-K:_RERANKER-K:_…>/{profiling,aiperf_rag_on}/` per point, plus aggregate `report.md` / `results.json` / `results.csv` at the run root.

**Run unit tests:**

```bash
uv sync --project scripts/rag-perf --extra dev   # one-time, installs pytest-asyncio
uv run --project scripts/rag-perf python -m pytest tests/unit/test_rag_perf/
```

## Out of scope

- quality scoring
- blueprint deploy
- clinical ASR
