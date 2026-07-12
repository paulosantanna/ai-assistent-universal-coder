from __future__ import annotations

from dataclasses import asdict, dataclass

from .token_budget import TokenBudget, task_budget


@dataclass(frozen=True)
class Subagent:
    id: str
    specialty: str
    mission: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    default_risk: str = "MEDIUM"
    parallel_group: str = "engineering"


SUBAGENTS = {
    "repository-cartographer": Subagent(
        "repository-cartographer", "repository topology",
        "Map code, dependencies, data flow, tests, documentation, and runtime boundaries.",
        ("repository_path", "allowed_paths"), ("inventory", "architecture_map", "evidence_index"),
        "MEDIUM", "discovery",
    ),
    "architecture-governor": Subagent(
        "architecture-governor", "software and AI architecture",
        "Compare current, modular-monolith, hybrid, and microservice options using evidence.",
        ("inventory", "quality_attributes", "constraints"), ("adr", "boundary_map", "migration_plan"),
        "HIGH", "architecture",
    ),
    "medical-evidence-researcher": Subagent(
        "medical-evidence-researcher", "biomedical evidence",
        "Build reproducible searches and normalized evidence records.",
        ("disease_profile", "source_policy", "research_questions"), ("queries", "records", "gaps"),
        "HIGH", "research",
    ),
    "qualified-source-curator": Subagent(
        "qualified-source-curator", "source governance",
        "Approve sources, access methods, licensing rules, corrections, and retractions.",
        ("candidate_sources", "official_registry"), ("approved_sources", "rejected_sources", "access_policy"),
        "HIGH", "research",
    ),
    "data-governance-specialist": Subagent(
        "data-governance-specialist", "data governance",
        "Validate provenance, privacy, licensing, deduplication, lineage, and leakage.",
        ("data_inventory", "schemas", "split_logic"), ("lineage", "leakage_report", "dataset_card_requirements"),
        "CRITICAL", "data",
    ),
    "training-pipeline-specialist": Subagent(
        "training-pipeline-specialist", "AI training pipeline",
        "Audit curation, splits, training, evaluation, artifacts, and reproducibility.",
        ("training_modules", "datasets", "configs"), ("pipeline_map", "missing_gates", "reproducibility_report"),
        "HIGH", "ml",
    ),
    "rag-specialist": Subagent(
        "rag-specialist", "RAG and grounding",
        "Audit dense retrieval, fusion, reranking, citations, abstention, and contradiction handling.",
        ("rag_modules", "evaluation_sets"), ("rag_report", "tests", "recommendations"),
        "HIGH", "retrieval",
    ),
    "bm25-specialist": Subagent(
        "bm25-specialist", "sparse retrieval",
        "Establish and optimize an explainable BM25 baseline.",
        ("corpus_stats", "queries", "relevance_judgments"), ("baseline", "parameter_evidence", "error_analysis"),
        "MEDIUM", "retrieval",
    ),
    "adapter-specialist": Subagent(
        "adapter-specialist", "LoRA, QLoRA, DoRA, and adapter composition",
        "Select adapter methods through hardware and benchmark evidence.",
        ("base_model", "hardware", "training_data", "baselines"), ("method_decision", "config", "benchmark"),
        "HIGH", "ml",
    ),
    "continuous-learning-specialist": Subagent(
        "continuous-learning-specialist", "governed continual learning",
        "Design replay, drift, shadow validation, approval, promotion, and rollback.",
        ("current_loop", "artifact_registry", "replay_suite"), ("learning_architecture", "promotion_policy", "rollback"),
        "CRITICAL", "ml",
    ),
    "simulation-scientist": Subagent(
        "simulation-scientist", "computational simulation",
        "Validate assumptions, calibration, controls, sensitivity, uncertainty, and falsifiability.",
        ("simulation_modules", "mechanistic_evidence", "calibration_data"), ("assumption_register", "sensitivity_plan", "limits"),
        "CRITICAL", "science",
    ),
    "owasp-ai-security-specialist": Subagent(
        "owasp-ai-security-specialist", "OWASP and GenAI security",
        "Audit application, API, prompt, tool, vector, output, data-poisoning, and agency risks.",
        ("architecture", "tools", "data_paths", "deployment"), ("threat_model", "control_matrix", "adversarial_tests"),
        "CRITICAL", "security",
    ),
    "vulnerability-intelligence-specialist": Subagent(
        "vulnerability-intelligence-specialist", "supply-chain vulnerability intelligence",
        "Correlate SBOM reachability with OSV, GHSA, NVD, KEV, EPSS, and vendor advisories.",
        ("sbom", "lockfiles", "exposure"), ("prioritized_report", "upgrade_plan", "exceptions"),
        "CRITICAL", "security",
    ),
    "python-staff-engineer": Subagent(
        "python-staff-engineer", "Python engineering",
        "Implement bounded, typed, secure, tested changes.",
        ("approved_handover", "relevant_symbols", "tests"), ("diff", "tests", "evidence"),
        "HIGH", "implementation",
    ),
    "test-evaluation-engineer": Subagent(
        "test-evaluation-engineer", "software and model evaluation",
        "Build software, data, retrieval, model, subgroup, security, and reproducibility tests.",
        ("changes", "criteria", "baselines"), ("test_suite", "executed_results", "coverage_gaps"),
        "HIGH", "verification",
    ),
    "documentation-engineer": Subagent(
        "documentation-engineer", "technical and scientific documentation",
        "Document verified implementation, operations, security, limitations, and traceability.",
        ("verified_code", "configuration", "test_evidence"), ("documentation_diff", "traceability"),
        "MEDIUM", "documentation",
    ),
    "token-context-governor": Subagent(
        "token-context-governor", "context and token economics",
        "Allocate context, cache evidence, deduplicate work, and prevent context bloat.",
        ("task_graph", "repository_index", "risk", "budget"), ("allocation", "context_packets", "cache_keys"),
        "MEDIUM", "orchestration",
    ),
    "planning-orchestrator": Subagent(
        "planning-orchestrator", "execution planning",
        "Build the dependency-aware execution DAG, checkpoints, and handovers.",
        ("findings", "architecture_decision", "constraints"), ("execution_dag", "handovers", "checkpoints"),
        "HIGH", "orchestration",
    ),
    "expert-judge": Subagent(
        "expert-judge", "independent validation",
        "Apply the strict evidence-based 10.0 completion gate.",
        ("scope", "diffs", "tests", "evidence", "risks", "documentation"), ("criterion_scores", "blockers", "verdict"),
        "CRITICAL", "judge",
    ),
}


def registry() -> dict:
    return {key: asdict(value) for key, value in SUBAGENTS.items()}


def create_tasks(objective: str, total_token_budget: int = 60000) -> list[dict]:
    allocation = TokenBudget(total_token_budget).allocate()
    specialist_agents = [a for a in SUBAGENTS.values() if a.id not in {"expert-judge", "token-context-governor"}]
    base = max(allocation["specialists"] // max(len(specialist_agents), 1), 512)
    tasks: list[dict] = []

    for agent in SUBAGENTS.values():
        if agent.id == "expert-judge":
            context = allocation["judge"]
        elif agent.id == "token-context-governor":
            context = allocation["root"] // 2
        else:
            context = task_budget(base, agent.default_risk)
        tasks.append({
            "task_id": f"{agent.id}:{abs(hash((objective, agent.id))) % 10_000_000}",
            "agent_id": agent.id,
            "objective": objective,
            "parallel_group": agent.parallel_group,
            "context_budget_tokens": context,
            "output_budget_tokens": max(min(context // 4, 3500), 256),
            "required_evidence": list(agent.outputs),
            "status": "PENDING",
        })
    return tasks
