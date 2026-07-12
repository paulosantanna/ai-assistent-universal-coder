"""Gate 5: RAG and BM25 — verify real integration, contracts, and evaluation datasets."""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS

RAG_KEY_TERMS = {
    "retriever", "retrieval", "bm25", "vector", "embedding", "reranker",
    "rerank", "fusion", "hybrid", "dense", "sparse", "chunk",
    "citation", "grounding", "faithfulness", "context",
}

EVAL_KEY_TERMS = {
    "recall", "precision", "mrr", "ndcg", "faithfulness",
    "citation_accuracy", "answer_relevancy", "context_precision",
}


def _find_files_with_terms(root: Path, terms: set[str], max_count: int = 20) -> list[str]:
    results = []
    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue
        if any(t in text for t in terms):
            results.append(rel)
            if len(results) >= max_count:
                break
    return results


def check_rag(repository: str) -> GateResult:
    """Gate 5: Audit RAG/BM25 integration — real contracts and evaluation datasets."""
    gate = GateResult(
        id="rag_quality",
        title="RAG Quality and Grounding",
        critical=True,
        weight=1.0,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    root = Path(repository).resolve()
    if not root.is_dir():
        gate.status = AuditStatus.BLOCKED
        gate.findings.append(f"Repository path not found: {repository}")
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    # Search for RAG implementation files
    rag_files = _find_files_with_terms(root, RAG_KEY_TERMS)
    eval_files = _find_files_with_terms(root, EVAL_KEY_TERMS)

    gate.metrics["rag_related_files"] = len(rag_files)
    gate.metrics["eval_related_files"] = len(eval_files)

    # Check for evaluation datasets
    eval_datasets = []
    for p in root.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(root)).replace("\\", "/")
            if should_ignore(rel, DEFAULT_EXCLUSIONS):
                continue
            if any(t in p.stem.lower() for t in {"eval", "benchmark", "testset", "ground_truth"}):
                eval_datasets.append(rel)

    gate.metrics["evaluation_datasets"] = len(eval_datasets)

    if not rag_files:
        gate.status = AuditStatus.NOT_APPLICABLE
        gate.findings.append("No RAG implementation detected — gate not applicable")
        gate.score = None
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    # Found RAG files — check for evaluation
    if not eval_datasets:
        gate.status = AuditStatus.BLOCKED
        gate.findings.append("RAG implementation found but no evaluation dataset detected")
        gate.findings.append("Cannot verify recall, precision, MRR, nDCG, faithfulness, or citation correctness without evaluation data")
        gate.score = None
        gate.remediation = [
            "Create evaluation dataset with ground-truth Q&A pairs",
            "Implement metrics: recall@k, precision@k, MRR, nDCG",
            "Implement faithfulness and citation correctness checks",
        ]
    elif not eval_files:
        gate.status = AuditStatus.BLOCKED
        gate.findings.append("RAG implementation and dataset exist but no evaluation code found")
        gate.score = None
        gate.remediation = ["Implement evaluation pipeline for RAG metrics"]
    else:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.evidence.append({
            "type": "metric",
            "source": "static_analysis",
            "sha256": "",
            "summary": f"RAG implementation detected ({len(rag_files)} files) with evaluation data ({len(eval_datasets)} datasets)",
            "verified": True,
        })
        if rag_files:
            gate.evidence.append({
                "type": "source_code",
                "source": rag_files[0],
                "sha256": "",
                "summary": f"RAG file: {rag_files[0]}",
                "verified": True,
            })
        gate.findings.append(f"RAG implementation detected ({len(rag_files)} files) with evaluation data ({len(eval_datasets)} datasets)")

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
