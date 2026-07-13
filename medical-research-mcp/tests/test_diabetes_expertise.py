from medical_research_mcp.diabetes_expertise import diabetes_ai_project_review_checklist, diabetes_expertise_map
from medical_research_mcp.qualified_sites_for_medical_research_around_world import source_policy, source_registry


def test_source_registry_has_global_diabetes_authorities():
    registry = source_registry()
    guideline_names = {entry["name"] for entry in registry["clinical_guidelines"]}

    assert "American Diabetes Association Standards of Care" in guideline_names
    assert "WHO Diabetes" in guideline_names
    assert "KDIGO Diabetes and CKD" in guideline_names
    assert "NICE Type 2 Diabetes NG28" in guideline_names
    assert "bio_chemistry" in registry


def test_source_policy_blocks_autonomous_medical_action():
    policy = " ".join(source_policy()).lower()

    assert "autonomous diagnosis" in policy
    assert "treatment recommendation" in policy
    assert "cure claim" in policy


def test_diabetes_expertise_map_covers_comorbidities_and_ai_architecture():
    expertise = diabetes_expertise_map()
    domain_map = expertise["domain_map"]

    assert "chronic kidney disease" in domain_map["comorbidities"]
    assert "cardiovascular disease" in domain_map["comorbidities"]
    assert "retinopathy" in domain_map["comorbidities"]
    assert "retrieval augmented generation" in domain_map["ai_system_domains"]
    assert "clinical safety guardrails" in domain_map["ai_system_domains"]
    assert "autonomous diagnosis" in expertise["not_for"]


def test_diabetes_ai_project_review_gate_has_blocking_safety_controls():
    checklist = diabetes_ai_project_review_checklist()
    safety = next(item for item in checklist if item["area"] == "safety and governance")

    assert safety["blocking_if_missing"] is True
    assert "no autonomous diagnosis" in safety["required"]
    assert "qualified human review" in safety["required"]
