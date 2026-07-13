from __future__ import annotations

from .qualified_sites_for_medical_research_around_world import source_policy, source_registry


DIABETES_DOMAIN_MAP = {
    "core_disease": [
        "type 1 diabetes",
        "type 2 diabetes",
        "gestational diabetes",
        "monogenic diabetes",
        "latent autoimmune diabetes in adults",
        "ketosis-prone diabetes",
    ],
    "biology": [
        "beta-cell stress and dysfunction",
        "autoimmunity",
        "insulin resistance",
        "incretin biology",
        "adipose inflammation",
        "hepatic glucose production",
        "renal glucose handling",
        "microvascular and macrovascular injury pathways",
    ],
    "chemistry_and_pharmacology": [
        "insulin analogs",
        "metformin mechanisms",
        "GLP-1 receptor agonists",
        "SGLT2 inhibitors",
        "DPP-4 inhibitors",
        "thiazolidinediones",
        "sulfonylureas",
        "immunomodulatory therapies for selected type 1 diabetes contexts",
    ],
    "comorbidities": [
        "cardiovascular disease",
        "chronic kidney disease",
        "retinopathy",
        "neuropathy",
        "diabetic foot disease",
        "metabolic dysfunction-associated steatotic liver disease",
        "hypertension",
        "dyslipidemia",
        "depression and diabetes distress",
        "sleep apnea",
        "periodontal disease",
    ],
    "ai_system_domains": [
        "evidence ingestion",
        "source governance",
        "disease ontology",
        "subgroup and comorbidity graph",
        "retrieval augmented generation",
        "clinical safety guardrails",
        "model evaluation",
        "bias and equity evaluation",
        "audit trail",
        "human review workflow",
    ],
}


STAFF_READINESS_CRITERIA = [
    "Uses only governed sources for medical claims.",
    "Separates clinical evidence, mechanistic biology, chemistry, and AI implementation evidence.",
    "Models diabetes subtypes and comorbidities explicitly instead of treating diabetes as one flat label.",
    "Requires provenance, publication type, population, subgroup, outcomes, limitations, and evidence tier.",
    "Flags contraindication-like and safety-sensitive claims for qualified human review instead of autonomous action.",
    "Includes bias, equity, geography, age group, sex, pregnancy, kidney function, cardiovascular risk, and access constraints as evaluation dimensions.",
    "Blocks unsupported cure claims and autonomous diagnosis or treatment recommendations.",
    "Can evaluate whether an AI project architecture has ingestion, retrieval, knowledge graph, evaluation, audit, and human-review layers.",
]


def diabetes_expertise_map() -> dict:
    return {
        "scope": "research and AI-project evaluation support for diabetes and related biology, medicine, chemistry, and comorbidities",
        "not_for": [
            "autonomous diagnosis",
            "autonomous treatment recommendations",
            "emergency triage",
            "human or animal experimentation authorization",
            "unsupported cure claims",
        ],
        "domain_map": DIABETES_DOMAIN_MAP,
        "readiness_criteria": STAFF_READINESS_CRITERIA,
        "source_registry": source_registry(),
        "source_policy": source_policy(),
    }


def diabetes_ai_project_review_checklist() -> list[dict[str, object]]:
    return [
        {
            "area": "medical evidence",
            "required": ["source registry", "evidence schema", "retraction/correction checks", "human review gate"],
            "blocking_if_missing": True,
        },
        {
            "area": "diabetes ontology",
            "required": ["subtypes", "comorbidities", "biomarkers", "outcomes", "interventions", "contraindication-like safety flags"],
            "blocking_if_missing": True,
        },
        {
            "area": "AI architecture",
            "required": ["RAG or evidence retrieval", "BM25 baseline", "knowledge graph or structured facts", "evaluation harness", "model/version registry"],
            "blocking_if_missing": False,
        },
        {
            "area": "safety and governance",
            "required": ["no autonomous diagnosis", "no autonomous treatment", "audit trail", "redaction", "qualified human review"],
            "blocking_if_missing": True,
        },
        {
            "area": "evaluation",
            "required": ["subgroup tests", "comorbidity tests", "citation faithfulness", "abstention tests", "contradiction handling"],
            "blocking_if_missing": True,
        },
    ]
