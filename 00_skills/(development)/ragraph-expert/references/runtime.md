# Local runtime and tool contracts
Updated: 2026-10-15
Entry point: ../SKILL.md. Implementation: [runtime README](../../../../rag-graph-laya-mcp/README.md).

1. Invoke health: check the execution service, Neo4j and model prerequisites. A valid MCP handshake alone is not graph/model readiness.
2. sources_list describes discovery/acquisition/analysis. sources_refresh accepts allowlisted source IDs and returns job_id; inspect terminal job_status before ingest.
3. ingest indexes or removes one source document. Long operations remain jobs; do not automatically retry an uncertain completion. graph_snapshot supplies committed nodes/edges and a replay cursor; graph_neighbors provides bounded evidence exploration.
4. search selects lexical/graph/hybrid/Laya-assisted retrieval. answer validates citation IDs and abstains if evidence is empty. Structural citation checks do not prove entailment.
5. laya_decide accepts bounded choice/score/noul questions. Preserve probabilities and checkpoint identity. The typed decision never grants execution authorization.
6. dataset_prepare generates distinct source-family partitions and human-review exports. train runs separate sequential Laya/LLM experiments; evaluate requires explicit human review by default. job_cancel requests cancellation, retaining committed partial changes.

Use local runtime environment references for model/Neo4j secrets. The Windows launcher stores its generated Neo4j credential only in Windows Credential Manager; the notebook may contain the provider identifier, never the credential value. No document content enters tracked model datasets or provider logs.

Missing service -> start the documented local service. Invalid input -> correct the declared schema. Provider/model failure -> preserve the failed job/partial artifacts and inspect preflight; never substitute invented evidence.
