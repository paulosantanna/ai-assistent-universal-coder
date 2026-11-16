# RAG, GraphRAG and Laya: source-backed engineering synthesis

Updated: 2026-10-15
Owner: codenavi-agent. Original synthesis under CC-BY-4.0; upstream sources retain their own licenses.
Entry point: sources.json. This document is an engineering synthesis, not a claim of exhaustive literature coverage or reproduced benchmarks.

## Foundations and the causal pipeline

RAG supplies external evidence to a generator. Retrieving a relevant passage is a different problem from generating a supported answer. The foundational paper combines parametric memory with non-parametric document retrieval; current modular implementations often index/retrieve separately from generator training. [Lewis et al.](https://arxiv.org/abs/2005.11401)

1. Define corpus authority, provenance, permissions and update rules before indexing. A persuasive answer grounded in the wrong version is still wrong.
2. Parse PDF/HTML/code without confusing navigation, executable instructions or repeated headers with evidence. Retain source offsets where available; OCR is an explicit prerequisite for image-only PDFs.
3. Normalize and deduplicate before splitting. Preserve table headings and code identifiers. Size/overlap is an experimentally chosen retrieval tradeoff, not a universal token constant.
4. Preserve document, chunk, source, version and permission metadata through every stage. Access control must precede both retrieval and generation.
5. Lexical retrieval recovers exact identifiers and rare terminology; dense retrieval handles paraphrases. Evaluate either independently before fusion.
6. Reciprocal-rank fusion combines ranked lists without assuming their raw scores have comparable scales. Reranking estimates query/candidate relevance after candidate generation.
7. Pack context under a measured tokenizer budget. Diversify sources, avoid duplicated evidence and preserve citations after any truncation.
8. Require the generator to abstain if evidence is insufficient. Valid citation identifiers establish traceability, not semantic entailment.
9. Separate retrieval recall/nDCG from answer correctness, faithfulness, citation validity, latency and cost. Changing an embedding model requires reindexing incompatible vectors.

## What a graph adds

A knowledge graph stores typed entities and relationships. Documents, their extracted assertions and model-generated summaries have different epistemic status; they must not be collapsed into an undifferentiated node label.

Entity extraction proposes names/types; entity resolution decides whether two mentions refer to the same entity. Similar surface forms do not prove identity. Relationship extraction must retain the source episode/chunk and temporal validity. Multi-hop traversal can connect relevant facts, but a longer path does not automatically produce a better explanation.

GraphRAG is a family of retrieval designs, not one interchangeable API. Microsoft's implementation extracts entities/relationships, identifies communities and constructs community reports to support corpus-wide questions. Local, global and other documented query modes have different evidence scopes. Prompt tuning changes extraction/generation prompts; it is not weight fine-tuning. [Microsoft documentation](https://microsoft.github.io/graphrag/), [original paper](https://arxiv.org/abs/2404.16130)

LightRAG combines graph structures with retrieval at different levels and supports document lifecycle operations. Its server/API and embedded SDK have different compatibility boundaries; use the documented surface and pin versions. Upstream benchmark advantages are dataset-dependent claims, not guarantees for a new corpus. [LightRAG](https://github.com/HKUDS/LightRAG)

Graphiti focuses on episodic, temporal knowledge and incremental changes. Its graph search combines semantic, keyword and graph signals. Facts can have validity windows and invalidation history; conflicting evidence should be visible instead of silently rewritten. The first implementation uses Graphiti/Neo4j; it does not imply all engines are installed. [Graphiti](https://github.com/getzep/graphiti)

## Tool landscape and selection

| Tool/family | Useful decision criterion | Integration boundary |
|---|---|---|
| Microsoft GraphRAG | Corpus-wide themes and community summarization | Its own index/query artifacts and documented APIs |
| LightRAG | Graph-enhanced retrieval and incremental document lifecycle | Prefer documented server/API contracts |
| Graphiti | Evolving episodic/temporal facts and incremental ingestion | Python SDK and supported graph drivers |
| Neo4j GraphRAG Python | Cypher, vector/hybrid retrievers and KG building | Official Neo4j package; do not use deprecated neo4j-genai |
| FalkorDB GraphRAG SDK | Graph storage plus domain ontology workflows | Verify its model/store configuration separately |
| Memgraph AI toolkit | Graph-backed applications, integrations and MCP tools | Toolkit availability is not a deployed database |
| LlamaIndex | Property-graph indexes and composable retrieval | Verify store integrations and retriever contracts |
| LangChain | Retrieval and application composition | Framework orchestration is not itself a graph database |
| Haystack | Explicit retrieval/generation/evaluation pipelines | Inspect graph integrations before asserting native support |
| RAGFlow | Document processing and a full RAG application | Operational stack is larger than an embedded SDK |
| Qdrant/Milvus/Weaviate | Vector or hybrid search baseline | Vector search alone does not implement temporal GraphRAG |
| Cytoscape.js | Interactive graph visualization | Browser rendering is not indexing or retrieval |

Comparison sources are the primary repository links in sources.json. Record current support/deprecation from each project when selecting it. In particular, Graphiti's documentation marks its Kuzu path deprecated; do not choose an unmaintained backend just because a tutorial still references it.

## Laya's role

Laya is a non-autoregressive decision model. It answers a set of typed questions in a forward pass rather than generating an open-ended response. `choice` selects a candidate, `score` represents ordinal levels, and `noul` represents a binary probability. Probabilities/confidence require held-out calibration evidence; the schema constrains the output shape but does not guarantee the decision is correct. [Official SDK](https://github.com/NandhaKishorM/laya)

Recommended RAG uses:
- Select lexical, hybrid or graph retrieval from a bounded policy; uncertain selection uses the measured deterministic baseline.
- Score candidate relevance after first-stage retrieval. Evaluate nDCG/MRR and latency against the baseline, not only classification accuracy.
- Decide whether evidence is sufficient using explicitly labelled examples; abstention thresholds are learned/evaluated on held-out data.
- Classify a corpus/document before choosing parsing/indexing policy; the classification never grants access or permission.

Laya cannot replace the LLM used to extract open-ended relations or write a cited explanation. It must not authorize shell commands, access credentials or override ACL filters. Exact token limits are checkpoint-specific; requests must account for state plus rendered question options rather than assuming all nominal context belongs to the document.

The official Laya MCP exposes typed prediction/routing tools. Reuse the SDK/protocol semantics instead of inventing a second decision representation. Local and remote MCP modes differ, including which shortlist/tournament tools are available. Read the installed package before assuming an optional integration exists.

## Two distinct training objectives

Laya's RLCD training specializes decisions and fits calibration parameters. Its `TrainConfig` and `finetune` accept typed question datasets; the selected base checkpoint and exported checkpoint layout must remain compatible. Validation/calibration/test sets have distinct roles. A calibration report based on too few examples is a limitation, not a passed confidence claim. [Training reference](https://nandhakishorm.github.io/laya/reference/train/)

LLM SFT trains supported response behavior. LoRA changes a small set of trainable adapter parameters; QLoRA combines adapter training with a quantized base to reduce memory. That does not train Laya's RLCD objective. Freeze the model revision, tokenizer, package versions, quantization configuration, seed and dataset hashes. [TRL](https://huggingface.co/docs/trl/sft_trainer), [PEFT](https://huggingface.co/docs/peft/package_reference/lora)

Training does not replace source freshness. A useful initial LLM task is learning to cite supplied context and abstain when it lacks support. Do not turn rapidly changing API details into unquestioned model memory.

## Evidence and contamination rules

- Group all document versions and derived chunks by source family before generating train/validation/test examples.
- Do not generate train labels from test answers or copy examples across partitions.
- Treat synthetic teacher labels as hypotheses. Reserve human-reviewed examples with explicit reviewer/approval fields.
- Negative contexts and misleading candidates must be represented, not only answerable questions.
- Report slices by language, task, corpus family and question difficulty where sample size supports it.
- Compare base and tuned checkpoints on the same frozen test set and serving configuration.
- Citation-format validity and token overlap are useful diagnostics; neither is a stand-in for human factual correctness or entailment.

## Live graph semantics

The dashboard receives graph changes only after the database has committed. SSE event IDs provide replay; snapshots carry a corresponding cursor. Preserve node positions during incremental updates, show bounded subgraphs instead of loading the entire graph, and offer accessible tabular evidence.

An event is not proof that a document was fully indexed. Track jobs independently and exclude partial/removed documents from answer evidence. Resume by durable IDs rather than re-uploading uncertain work. Keep original provenance when aliases/entities merge.

## Failure modes and verification

| Failure | Required behavior/check |
|---|---|
| Missing graph/model runtime | Actionable health report; no simulated success |
| Invalid extraction JSON | Reject/retry boundedly; never fabricate relations |
| Disconnected SSE | Replay after cursor or fetch a fresh snapshot |
| Changed source | New version, explicit old-version retirement, provenance retained |
| Cancelled ingestion | Report committed partial changes; no active partial retrieval |
| Invalid citations | Reject generated answer |
| Low-confidence Laya ranking | Retain deterministic hybrid order |
| CUDA/OOM/quantization failure | Preserve base weights and experiment failure evidence |
| Human review absent | No reviewed-quality or promotion claim |
| Unlicensed training source | Exclude from training; preserve knowledge-source attribution |

Package versions can differ from GitHub main: the initial release lookup found Graphiti0.32.0 in upstream source while PyPI offered0.30.2. Runtime contracts are verified against the pinned installed package. Similarly MCP2.3 uses constructor handlers instead of the former decorator API; examples written for another SDK major must not be copied blindly.
