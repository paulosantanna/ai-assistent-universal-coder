REQUIRED={"provenance","bm25","dense_retrieval","fusion","reranking","citation_binding","abstention","contradiction_tests","retrieval_metrics"}
def rag_audit(capabilities:list[str])->dict:
    missing=sorted(REQUIRED-set(capabilities))
    return {"passed":not missing,"missing":missing,
      "metrics":["Recall@k","Precision@k","nDCG@k","MRR","citation_correctness","unsupported_claim_rate","contradiction_recall"]}
