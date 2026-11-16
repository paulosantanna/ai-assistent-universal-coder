# GraphRAG + Laya MCP

Local-first MCP and dashboard owned by `codenavi-agent`, inheriting root `AGENTS.md`.
The stdio server uses the official MCP2.3 SDK. A single FastAPI execution service owns SQLite jobs/events, Graphiti/Neo4j and model calls. Protocol initialization never loads weights or requires credentials.

## Install

From this directory, with uv installed:

```powershell
uv sync --frozen --extra test --extra training
.\.venv\Scripts\python.exe scripts/bootstrap.py --assets --graph
.\.venv\Scripts\python.exe scripts/preflight.py
.\.venv\Scripts\python.exe scripts/launch.py
```

The locked CUDA13.0 wheel supports the Windows RTX5080 profile. The launcher starts only local hidden processes and stores its generated Neo4j credential in Windows Credential Manager, provider `CodENavi/GraphRAG-Laya/Neo4j`. No password enters tracked files, notebook, chat or logs. Portable Java21/Neo4j Community distributions and model cache live in ignored `.state/`; no Windows service is installed.

Open **http://127.0.0.1:8765**. Acquire a source, inspect its job, then index it. Query with lexical/hybrid/graph/Laya ranking. Only committed graph changes are published, with SSE replay and accessible tables. Partial indexes are excluded from answer evidence.

Linux/other environments: install the same lock without Windows bootstrap, start your own compatible Neo4j, configure `RGL_NEO4J_URL`, `RGL_NEO4J_USER`, `RGL_NEO4J_PASSWORD` through a runtime provider, and run `python model_server.py` and `python server.py --web` in separate terminals. The local execution service is a singleton.

## MCP client

Configure a stdio command array pointing at `python` and the absolute `server.py` path, with the package as working directory. The bootstrap automatically selects its isolated interpreter when present. Start the execution service for graph/model/jobs; `initialize`, `tools/list`, `ping`, resources and offline `health` work without it.

[Client configuration](client-config.json) contains the concrete path for this checkout and no credentials. Import its server entry into an MCP client supporting `mcpServers`; other checkouts must adjust the script path. The workspace inventory/protocol probe does not automatically attach the server to an already running editor session.

The schema source is `app/contracts.py`:16 tools (`health`, `sources_list`, `sources_refresh`, `ingest`, `search`, `answer`, `reversa_search`, `reversa_answer`, `graph_snapshot`, `graph_neighbors`, `laya_decide`, `dataset_prepare`, `train`, `evaluate`, `job_status`, `job_cancel`). Inputs reject extra fields. The HTTP equivalent is `POST /api/tools/{name}`. Long operations return `job_id`. Events: `GET /api/events?after=cursor`, with `Last-Event-ID` reconnection support.

`reversa_search` and `reversa_answer` use the separately built local corpus at `../07_mapeamentos/reversa-2026-11-01/`; `strategy` selects `lexical` (default) or `hybrid` (local E5 embeddings and lexical reciprocal-rank fusion). Citations include file, lines and source hash. They do not add documents to Graphiti or the training catalog. Sources are untrusted and stale files are excluded. Answer generation requires the configured model service; citation format is checked but entailment requires separate evaluation. The local vector index must match the installed E5 revision and the corpus snapshot.

Resources: `knowledge://rag-graph-laya/sources` and `knowledge://rag-graph-laya/research`. The catalog is expandable and reports discovered/acquired/analyzed status; it does not claim all literature or empirical validation of all tools.

Read acquired documents progressively with the resource template `knowledge://rag-graph-laya/source/{source_id}/{ordinal}`. Each passage contains at most12,000characters with hash/revision/URL and a continuation flag. Source acquisition, progressive reading and completed graph indexing are distinct states.

## Runtime configuration

| Variable | Default/meaning |
|---|---|
| RGL_STATE | `.state/`; local ledgers/datasets/experiments |
| RGL_SERVICE_URL | `http://127.0.0.1:8765`; stdio-to-service loopback endpoint |
| RGL_MODEL_URL | `http://127.0.0.1:8008/v1` |
| RGL_MODEL | `Qwen/Qwen3-4B-Instruct-2507` |
| RGL_EMBEDDING | `intfloat/multilingual-e5-base`,768 dimensions |
| RGL_LAYA_CHECKPOINT | `convaiinnovations/laya-multilingual` or local checkpoint |
| RGL_NEO4J_PASSWORD / RGL_MODEL_API_KEY | Runtime credentials only |
| RGL_ALLOW_EXTERNAL | `0`; HTTPS external model APIs require explicit enablement |
| RGL_LLM_ADAPTER | Optional local experiment adapter; no automatic promotion |

Source fetching is restricted to catalog IDs and primary-source hosts, with bounded redirect/body size. Source text is untrusted data; it never grants action permission. Local web mutations require the local Host and same origin. Model and embedding weights download only on use; no paid API is invoked by default.

Graphiti telemetry is disabled through its installed version's `GRAPHITI_TELEMETRY_ENABLED` setting; Hugging Face telemetry is disabled in the model/training processes.

## Domain training and review

Acquire at least10 training-permitted source families. `dataset_prepare` creates2,000 distinct examples per flow by default, with80/10/10 family-disjoint partitions. Its default `generation=extractive` builds bilingual template questions with source-verifiable extractive references, absence/title-only negative contexts and provisional route/relevance labels. The manifest records unique source passages, correlated-template limits, source/revision/hashes and100 held-out review examples per flow. `generation=teacher` uses the local generative model with bounded JSON retries and saves partial work. Neither method claims human-verified labels.

Review that file with correct labels/answers and set `review.approved=true`, a nonempty `review.reviewer` and optional notes. No automation marks the review complete. `evaluate` requires all exported examples approved by default; `require_human_review=false` produces explicitly synthetic-only metrics.

`train` executes Laya RLCD or Qwen QLoRA sequentially, with at most3 experiments per flow/dataset, bounded epochs, checkpoints and baseline/candidate validation metrics. Serving generation is paused/unloaded during training. The test set is not used to choose checkpoints. All candidates stay unpromoted. Citation-format validity/token F1 are diagnostics, not verified entailment or factual correctness.

The Windows QLoRA worker uses TRL data preparation and the public Transformers Trainer loss extension with standard causal cross entropy. This avoids TRL1.15's unconditional fused-LM-head Triton call, which failed in the verified Windows environment. Quantization and PEFT adapters remain active; completion labels alone receive the loss.

```powershell
.\.venv\Scripts\python.exe scripts/task.py dataset_prepare --wait
.\.venv\Scripts\python.exe scripts/task.py job_status --job-id JOB_ID
```

For cancellation use `job_cancel`. Cancelled/interrupted work retains committed partial changes; inspect IDs before retrying. Do not blindly repeat an uncertain ingestion/train operation.

For complex inputs, save JSON in a local file and use `--args-file PATH`; this avoids native PowerShell quote conversion.

## Verify

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check app worker.py model_server.py scripts tests
```

Workspace gates run from the repository root with `python quality/validate.py --runtime`. The capability inventory contains the exact declared tool schemas. CI installs the hash-pinned core requirements before this protocol check; GPU weights/training are separate real-runtime evidence, never inferred from protocol PASS.

Verification scope and remaining human/provider limits: [implementation report](VERIFICATION.md). Technical evidence: [research synthesis](knowledge/research.md), [primary sources](knowledge/sources.json). Source text, generated datasets/checkpoints, credentials and logs are never committed.

Review using the user-authorized local MongoDB data: [observed state, revised flow and correction priorities](docs/mongodb-review/README.md). The read-only inspector `scripts/review_mongodb.js` emits aggregate facts; it does not import the biomedical corpus into the technical catalog or train/promote models.
