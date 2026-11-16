# Verification and quality boundaries
Updated: 2026-10-15
Entry point: ../SKILL.md.

- Validate SKILL.md physical line count/frontmatter/modules, canonical catalog/discovery/registry and package-hash review. Static trigger review is not routing accuracy.
- Establish the pre-change behavioral baseline. Use a real MCP stdio handshake and meaningful ingestion/query/job tests. Fixture runs and real-provider checks must be labelled separately.
- Freeze queries/labels, document versions, dataset hashes, base revisions and tokenizer/provider settings. Group source families before splitting train/validation/test. Evaluate contamination and duplicate examples explicitly.
- Compare retrieval recall@k/nDCG/MRR; answer correctness/faithfulness/abstention/citations; graph update/deletion/contradiction behavior; model decision accuracy/ECE; latency/memory/cost. Choose only metrics meaningful to the actual task.
- Laya RLCD and LLM QLoRA are separate experiments. Reload both outputs and compare with their bases using identical held-out data. Maximum three experiments per flow/dataset is the initial bound. Preserve base weights and unpromoted candidates.
- Human review has explicit approved/reviewer/notes fields. Pending review blocks reviewed test-quality claims. Synthetic teacher labels, token F1 and citation-format validity cannot establish factual correctness by themselves.
- Promote only a candidate that improves the chosen task metric without a material regression in calibration, evidence support or abstention. If it does not improve, report the negative result; never infer success from lower train loss.

Current runtime verification and limitations are recorded in the implementation report; this skill's existence does not prove a provider is installed or a model is production-ready.
