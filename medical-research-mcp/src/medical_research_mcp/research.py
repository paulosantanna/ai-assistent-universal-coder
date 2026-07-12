from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from typing import Any

import httpx

from .models import DiseaseProfile, EvidenceRecord

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CLINICAL_TRIALS_BASE = "https://clinicaltrials.gov/api/v2"
EUROPE_PMC_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"


def build_query(profile: DiseaseProfile, methods: list[str] | None = None) -> str:
    disease_terms = [profile.disease, *profile.aliases, *profile.subgroups]
    blocks = [f"({' OR '.join(sorted(set(disease_terms)))})"]
    if profile.comorbidities:
        blocks.append(f"({' OR '.join(sorted(set(profile.comorbidities)))})")
    if methods:
        blocks.append(f"({' OR '.join(sorted(set(methods)))})")
    return " AND ".join(blocks)


def build_method_discovery_queries(profile: DiseaseProfile) -> dict[str, str]:
    core = build_query(profile)
    return {
        "ai_architecture": f"{core} AND (artificial intelligence OR machine learning OR foundation model OR knowledge graph)",
        "retrieval": f"{core} AND (retrieval augmented generation OR information retrieval OR BM25 OR embeddings)",
        "fine_tuning": f"{core} AND (fine tuning OR parameter efficient fine tuning OR LoRA OR QLoRA OR DoRA)",
        "continual_learning": f"{core} AND (continual learning OR continuous learning OR concept drift OR model updating)",
        "simulation": f"{core} AND (computational simulation OR systems biology OR causal model OR digital twin)",
        "validation": f"{core} AND (external validation OR prospective validation OR clinical trial)",
    }


async def search_pubmed(query: str, retmax: int = 20) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(
            f"{PUBMED_BASE}/esearch.fcgi",
            params={
                "db": "pubmed",
                "term": query,
                "retmode": "json",
                "retmax": min(retmax, 100),
            },
        )
        response.raise_for_status()
        return response.json()


async def fetch_pubmed_summaries(pmids: list[str]) -> dict[str, Any]:
    if not pmids:
        return {"result": {}}
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(
            f"{PUBMED_BASE}/esummary.fcgi",
            params={
                "db": "pubmed",
                "id": ",".join(pmids[:100]),
                "retmode": "json",
            },
        )
        response.raise_for_status()
        return response.json()


async def search_europe_pmc(query: str, page_size: int = 20) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(
            f"{EUROPE_PMC_BASE}/search",
            params={
                "query": query,
                "format": "json",
                "pageSize": min(page_size, 100),
                "resultType": "core",
            },
        )
        response.raise_for_status()
        return response.json()


async def search_clinical_trials(query: str, page_size: int = 20) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(
            f"{CLINICAL_TRIALS_BASE}/studies",
            params={
                "query.term": query,
                "pageSize": min(page_size, 100),
                "format": "json",
            },
        )
        response.raise_for_status()
        return response.json()


def evidence_id(source: str, identifier: str) -> str:
    return hashlib.sha256(f"{source}:{identifier}".encode("utf-8")).hexdigest()[:24]


def raw_evidence_record(source: str, identifier: str, title: str) -> EvidenceRecord:
    return EvidenceRecord(
        id=evidence_id(source, identifier),
        source=source,
        source_type="registry_or_literature",
        retrieved_at=datetime.now(timezone.utc).isoformat(),
        title=title,
        identifiers={"primary": identifier},
        provenance=[source],
    )


def source_screening_requirements() -> list[str]:
    return [
        "capture query, source, retrieval date, stable identifier, and source version",
        "classify publication or trial type",
        "check corrections, retractions, and duplicate records",
        "record population, subgroup, comorbidities, intervention, outcomes, and limitations",
        "preserve negative and contradictory findings",
        "do not treat an abstract as equivalent to full evidence",
        "respect licensing and access restrictions",
    ]
