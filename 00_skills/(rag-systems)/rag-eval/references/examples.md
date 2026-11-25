# Examples

## Examples

**Set API key without putting secrets in shell history (preferred patterns):** load from a gitignored env file or secrets manager; avoid committing `.env`; rotate keys if exposed. Details: [`references/benchmark-execution.md#credential-hygiene-nvidia_api_key`](upstream/benchmark-execution.md#credential-hygiene-nvidia_api_key).

**Minimal eval (key already in environment):**

```bash
uv sync --project scripts/eval
uv run --project scripts/eval python scripts/eval/evaluate_rag.py \
  --dataset-paths /path/to/my_dataset \
  --host localhost \
  --port 8081
```

**Pretty-print summary JSON:**

```bash
python3 -m json.tool results/my_dataset/rag_my_dataset_evaluation_summary.json
```

More examples (skip ingestion, quality sweeps): [`references/benchmark-execution.md`](upstream/benchmark-execution.md).

## Out of scope

- RAG Blueprint deploy
- latency benchmarking
- model training
