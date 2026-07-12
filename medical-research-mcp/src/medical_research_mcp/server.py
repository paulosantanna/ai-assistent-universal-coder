from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .AI_architecture import recommend_architecture
from .AI_architecture_best_practices import evaluate_architecture_practices
from .AI_trainning_pipeline import audit_pipeline_artifacts, pipeline_blueprint
from .AI_OWASP import security_checklist
from .AI_best_practises import AI_BEST_PRACTICES
from .RAG import rag_audit
from medical_research_mcp.audit import audit_repository as audit_repository_v2
from .bm25 import BM25Index
from .continuos_learning_architecture import continuous_learning_gate
from .dependency_security import (
    fetch_cisa_kev,
    fetch_epss,
    inventory_dependencies,
    query_osv,
    vulnerability_source_policy,
)
from .expert_validator import validate_10_0
from .lora_qora_dora_doubleLora import recommend_adapter
from .models import DiseaseProfile, ValidationCriterion
from .planning import create_complete_plan
from .qualified_sites_for_medical_research_around_world import source_policy, source_registry
from .research import (
    build_method_discovery_queries,
    build_query,
    fetch_pubmed_summaries,
    search_clinical_trials,
    search_europe_pmc,
    search_pubmed,
    source_screening_requirements,
)
from .repository import architecture_inventory, scan_repository
from .subagents import registry
from .token_budget import TokenBudget, context_compaction_policy, context_cache_key

mcp = FastMCP("AEOS Medical Research MCP")


@mcp.tool()
def repository_scan(repository: str) -> dict:
    """Inspect repository files, languages, manifests, tests, documentation, and AI pipeline candidates."""
    return scan_repository(repository)


@mcp.tool()
def repository_architecture_inventory(repository: str) -> dict:
    """Map ingestion, knowledge, training, simulation, evaluation, governance, and observability."""
    return architecture_inventory(repository)


@mcp.tool()
def medical_ai_audit(
    repository: str,
    mode: str = "deep",
    timeout_seconds: int = 900,
    run_tests: bool = True,
    run_security: bool = True,
    run_dependency_audit: bool = True,
    output: str | None = None,
) -> dict:
    """Audit the repository with real evidence checks and honest scoring.
    
    Args:
        repository: Path to the repository to audit
        mode: 'structural' (inventory only, no scores) or 'deep' (evidence-based)
        timeout_seconds: Maximum execution time in seconds
        run_tests: Whether to execute pytest
        run_security: Whether to run security scans
        run_dependency_audit: Whether to run dependency auditing
        output: Path to write detailed report JSON (optional)
    
    Returns:
        Executive summary with status, score, coverage, and key findings.
        Full report is written to `output` if provided.
    """
    report = audit_repository_v2(
        repository=repository,
        mode=mode,
        timeout_seconds=timeout_seconds,
        run_tests=run_tests,
        run_security=run_security,
        run_dependency_audit=run_dependency_audit,
        read_only=True,
        output=output,
    )
    # Return summarized output for MCP (not the full inventory)
    return {
        "target": report.target,
        "mode": report.mode,
        "status": report.status.value,
        "score": report.score,
        "coverage": report.coverage,
        "executed_gates": report.executed_gates,
        "total_gates": report.total_gates,
        "critical_not_executed": report.critical_not_executed,
        "executive_summary": report.executive_summary,
        "findings": report.findings[:20],
        "report_path": report.report_path,
        "report_sha256": report.report_sha256,
    }


@mcp.tool()
def architecture_recommendation(
    repository: str,
    team_size: int = 1,
    deployment_targets: int = 1,
) -> dict:
    """Recommend modular monolith, hybrid, or microservices from repository and operational evidence."""
    return recommend_architecture(repository, team_size, deployment_targets)


@mcp.tool()
def architecture_best_practices_gate(capabilities: list[str]) -> dict:
    """Validate architecture capabilities against the medical AI baseline."""
    return evaluate_architecture_practices(capabilities)


@mcp.tool()
def training_pipeline_design() -> list[dict]:
    """Return the governed training, evaluation, simulation, and promotion pipeline."""
    return pipeline_blueprint()


@mcp.tool()
def training_pipeline_audit(artifacts: list[str]) -> dict:
    """Check declared pipeline artifacts and stage gates."""
    return audit_pipeline_artifacts(artifacts)


@mcp.tool()
def owasp_ai_gate(enabled_controls: list[str]) -> dict:
    """Evaluate controls against OWASP GenAI risk categories."""
    return security_checklist(enabled_controls)


@mcp.tool()
def rag_quality_gate(capabilities: list[str]) -> dict:
    """Audit sparse, dense, hybrid retrieval, citations, abstention, and contradiction tests."""
    return rag_audit(capabilities)


@mcp.tool()
def continuous_learning_quality_gate(capabilities: list[str]) -> dict:
    """Validate versioning, replay, drift, shadow promotion, approval, and rollback."""
    return continuous_learning_gate(capabilities)


@mcp.tool()
def adapter_recommendation(
    available_vram_gb: float,
    base_model_billion_parameters: float,
    comparative_evidence: dict[str, float] | None = None,
) -> dict:
    """Compare LoRA, QLoRA, DoRA, and adapter composition."""
    return recommend_adapter(
        available_vram_gb,
        base_model_billion_parameters,
        comparative_evidence,
    )


@mcp.tool()
def bm25_search(documents: list[str], query: str, top_k: int = 5) -> list[dict]:
    """Run a deterministic BM25 baseline over supplied documents."""
    return [
        {"document_index": index, "score": score}
        for index, score in BM25Index(documents).search(query, top_k)
    ]


@mcp.tool()
def qualified_medical_sources() -> dict:
    """Return governed international source registries and access policy."""
    return {"sources": source_registry(), "policy": source_policy()}


@mcp.tool()
def build_disease_research_query(
    profile: dict,
    methods: list[str] | None = None,
) -> str:
    """Build a reproducible disease, subgroup, comorbidity, and method query."""
    return build_query(DiseaseProfile.model_validate(profile), methods)


@mcp.tool()
def build_research_method_queries(profile: dict) -> dict:
    """Build queries for architectures, RAG, adapters, continual learning, simulation, and validation."""
    return build_method_discovery_queries(DiseaseProfile.model_validate(profile))


@mcp.tool()
async def pubmed_research(query: str, retmax: int = 20) -> dict:
    """Search PubMed using official NCBI E-utilities."""
    return await search_pubmed(query, retmax)


@mcp.tool()
async def pubmed_summaries(pmids: list[str]) -> dict:
    """Fetch PubMed summaries for a bounded PMID list."""
    return await fetch_pubmed_summaries(pmids)


@mcp.tool()
async def europe_pmc_research(query: str, page_size: int = 20) -> dict:
    """Search Europe PMC through its REST API."""
    return await search_europe_pmc(query, page_size)


@mcp.tool()
async def clinical_trials_research(query: str, page_size: int = 20) -> dict:
    """Search ClinicalTrials.gov using API v2."""
    return await search_clinical_trials(query, page_size)


@mcp.tool()
def medical_evidence_screening_policy() -> list[str]:
    """Return minimum screening and provenance requirements."""
    return source_screening_requirements()


@mcp.tool()
def dependency_inventory(repository: str) -> list[dict]:
    """Inventory Python, npm, and Maven dependencies from repository manifests."""
    return inventory_dependencies(repository)


@mcp.tool()
async def osv_vulnerability_query(dependencies: list[dict]) -> dict:
    """Query OSV for exact ecosystem, package, and version records."""
    return await query_osv(dependencies)


@mcp.tool()
async def cisa_known_exploited_vulnerabilities() -> dict:
    """Fetch the CISA Known Exploited Vulnerabilities catalog."""
    return await fetch_cisa_kev()


@mcp.tool()
async def epss_scores(cves: list[str]) -> dict:
    """Fetch FIRST EPSS scores for a bounded CVE list."""
    return await fetch_epss(cves)


@mcp.tool()
def vulnerability_intelligence_policy() -> dict:
    """Return required multi-source vulnerability intelligence policy."""
    return vulnerability_source_policy()


@mcp.tool()
def specialized_subagents() -> dict:
    """Return the specialist subagent registry and unique responsibilities."""
    return registry()


@mcp.tool()
def token_budget_plan(total_tokens: int = 60000) -> dict:
    """Allocate Root, evidence, specialist, synthesis, and Judge token budgets."""
    return {
        "allocation": TokenBudget(total_tokens).allocate(),
        "policies": context_compaction_policy(),
    }


@mcp.tool()
def context_hash(payload: dict) -> str:
    """Create a deterministic cache key for context and evidence packets."""
    return context_cache_key(payload)


@mcp.tool()
def complete_beta_plan(
    repository: str,
    disease: str,
    token_budget: int = 60000,
) -> dict:
    """Create a phase-based, token-budgeted multi-agent Beta evolution plan."""
    return create_complete_plan(repository, disease, token_budget)


@mcp.tool()
def expert_validation_10_0(criteria: list[dict]) -> dict:
    """Accept only when every mandatory criterion passes with evidence and score is 10.0."""
    parsed = [ValidationCriterion.model_validate(item) for item in criteria]
    return validate_10_0(parsed).model_dump(mode="json")


@mcp.tool()
def ai_engineering_practices() -> dict:
    """Return the governed medical AI engineering practice catalog."""
    return AI_BEST_PRACTICES


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
