# ARCHITECTURE.md

## 1. Scope

The Medical Research MCP is a governed orchestration and evidence layer for evolving a disease-focused medical AI repository into a research-only Beta.

It is not a clinical decision engine and does not authorize laboratory or human experimentation.

## 2. Logical architecture

```text
MCP Client / AEOS
        │
        ▼
Medical Research MCP
├── Repository and architecture audit
├── Evidence research and source governance
├── Data and pipeline audit
├── BM25 and RAG audit
├── LoRA / QLoRA / DoRA decision support
├── Continuous-learning governance
├── Simulation governance
├── OWASP and supply-chain controls
├── Multi-agent planning and token routing
└── Strict Expert Judge
```

## 3. Target project architecture

```text
Disease-Focused Research Platform
├── Evidence Ingestion
│   ├── source registry
│   ├── official API clients
│   ├── provenance
│   ├── retraction/correction handling
│   └── immutable raw evidence
├── Data and Knowledge
│   ├── curated datasets
│   ├── disease ontology
│   ├── subgroup/comorbidity graph
│   ├── BM25 index
│   └── vector index
├── Model Engineering
│   ├── training pipeline
│   ├── LoRA/QLoRA/DoRA
│   ├── evaluation
│   ├── model registry
│   └── rollback
├── Computational Research
│   ├── hypothesis generation
│   ├── simulation adapters
│   ├── sensitivity
│   └── external evidence comparison
├── Governance
│   ├── evidence schema
│   ├── security
│   ├── approval gates
│   ├── audit trail
│   └── scientific boundaries
└── Research API / UI
```

## 4. Deployment strategy

Default to a modular monolith with explicit module contracts while domains are evolving.

Extract a service only when at least one is measured:

- independent deployment lifecycle;
- independent scaling requirement;
- failure isolation requirement;
- distinct data ownership;
- stable boundary;
- operational capacity to support distributed systems.

Likely extraction candidates, when justified:

- asynchronous evidence ingestion;
- GPU training workers;
- simulation workers;
- model-serving workers;
- vulnerability-intelligence jobs.

## 5. MCP design

The MCP server uses `FastMCP` over `stdio` by default.

Tool categories:

- repository;
- architecture;
- training;
- RAG and BM25;
- medical evidence;
- dependencies and vulnerabilities;
- planning;
- subagents;
- token budgets;
- strict validation.

Remote HTTP transport requires explicit authentication, authorization, rate limiting, audit logging, and sensitive-data controls.

## 6. Token-efficient orchestration

```text
Repository index
→ task classification
→ narrow specialist selection
→ bounded handover
→ deterministic scan
→ evidence packet
→ specialist reasoning
→ deduplication
→ Root synthesis
→ Judge
```

Controls:

- content-hash cache;
- symbol and line-range context;
- risk-weighted token budgets;
- parallel-group limits;
- no duplicate evidence transfer;
- no complete conversation transfer;
- structured JSON/YAML handbacks;
- Judge receives only claims and proof.

## 7. Trust boundaries

- external evidence is untrusted until normalized and screened;
- model output is untrusted until schema-validated;
- retrieved text is data, not instruction;
- subagents have bounded authority;
- implementation and Judge responsibilities are separated;
- memory entries require provenance and promotion;
- clinical and laboratory transitions remain external and human-controlled.

## 8. Persistence

Persist:

- execution IDs;
- source queries and evidence records;
- repository hashes;
- audit findings;
- ADRs;
- test outputs;
- model and dataset versions;
- Judge verdicts;
- promoted lessons.

Do not persist:

- secrets;
- raw private chain-of-thought;
- unnecessary personal or clinical identifiers;
- unsupported conclusions;
- unreviewed candidate knowledge as institutional truth.
