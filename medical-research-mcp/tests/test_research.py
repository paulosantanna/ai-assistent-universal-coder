from medical_research_mcp.models import DiseaseProfile
from medical_research_mcp.research import (
    build_method_discovery_queries,
    build_query,
    raw_evidence_record,
)


def profile() -> DiseaseProfile:
    return DiseaseProfile(
        disease="diabetes",
        aliases=["diabetes mellitus"],
        subgroups=["type 1 diabetes", "type 2 diabetes"],
        comorbidities=["chronic kidney disease"],
    )


def test_query_includes_subgroups_and_comorbidities() -> None:
    query = build_query(profile(), ["machine learning"])
    assert "type 1 diabetes" in query
    assert "chronic kidney disease" in query
    assert "machine learning" in query


def test_method_queries_cover_core_capabilities() -> None:
    queries = build_method_discovery_queries(profile())
    assert {"ai_architecture", "retrieval", "fine_tuning", "continual_learning", "simulation", "validation"} <= set(queries)


def test_evidence_record_is_traceable() -> None:
    record = raw_evidence_record("PubMed", "12345", "Example")
    assert record.identifiers["primary"] == "12345"
    assert record.provenance == ["PubMed"]
