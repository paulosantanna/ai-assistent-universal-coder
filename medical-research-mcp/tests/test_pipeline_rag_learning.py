from medical_research_mcp.AI_trainning_pipeline import audit_pipeline_artifacts, pipeline_blueprint
from medical_research_mcp.RAG import rag_audit
from medical_research_mcp.continuos_learning_architecture import continuous_learning_gate


def test_pipeline_blueprint_contains_promotion() -> None:
    assert any(stage["id"] == "promotion" for stage in pipeline_blueprint())


def test_pipeline_audit_detects_missing_artifacts() -> None:
    result = audit_pipeline_artifacts(["source_policy"])
    assert not result["complete"]
    assert result["findings"]


def test_rag_gate_passes_with_all_capabilities() -> None:
    capabilities = [
        "provenance", "bm25", "dense_retrieval", "fusion", "reranking",
        "citation_binding", "abstention", "contradiction_tests", "retrieval_metrics",
    ]
    assert rag_audit(capabilities)["passed"]


def test_continuous_learning_requires_rollback() -> None:
    capabilities = [
        "versioned_data", "versioned_models", "replay_suite",
        "drift_detection", "shadow_mode", "approval_gate",
    ]
    result = continuous_learning_gate(capabilities)
    assert not result["passed"]
    assert "rollback" in result["missing"]
