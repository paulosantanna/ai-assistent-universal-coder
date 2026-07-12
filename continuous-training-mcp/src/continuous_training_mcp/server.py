from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .config import load_config, merge_env_overrides
from .models import ContinuousTrainingConfig
from .research import (
    content_hash,
    fetch_page,
    list_curated_sources,
    list_training_sites,
    search_arxiv,
    search_github,
    search_paperswithcode,
    search_reddit,
    search_web,
)
from .sources import best_practices_catalog, source_registry, source_screening_policy

mcp = FastMCP("AEOS Continuous Training Documentation MCP")

config: ContinuousTrainingConfig = merge_env_overrides(load_config())


@mcp.tool()
async def web_search(query: str, max_results: int = 20) -> dict:
    """Search the web for continuous AI training documentation, best practices, and resources."""
    result = await search_web(query, max_results)
    return result.model_dump(mode="json")


@mcp.tool()
async def arxiv_search(query: str, max_results: int = 20) -> dict:
    """Search arXiv for academic papers on continuous training, fine-tuning, and ML training techniques."""
    result = await search_arxiv(query, max_results)
    return result.model_dump(mode="json")


@mcp.tool()
async def paperswithcode_search(query: str, max_results: int = 20) -> dict:
    """Search Papers with Code for benchmarks and implementations related to training methodologies."""
    result = await search_paperswithcode(query, max_results)
    return result.model_dump(mode="json")


@mcp.tool()
async def github_search(query: str, max_results: int = 20) -> dict:
    """Search GitHub repositories for training frameworks, fine-tuning tools, and ML infrastructure projects."""
    result = await search_github(query, max_results)
    return result.model_dump(mode="json")


@mcp.tool()
async def reddit_search(query: str, max_results: int = 20) -> dict:
    """Search Reddit for community discussions on training techniques, hardware, and best practices."""
    result = await search_reddit(query, max_results)
    return result.model_dump(mode="json")


@mcp.tool()
async def web_fetch(url: str, timeout: int = 30) -> dict:
    """Fetch and extract readable content from a documentation URL or web page."""
    result = await fetch_page(url, timeout)
    return result.model_dump(mode="json")


@mcp.tool()
def curated_sources(filters: dict | None = None) -> dict:
    """Return governed, curated documentation sources for continuous AI training. Can filter by domain, technique, framework, category, or authority."""
    return {"sources": list_curated_sources(filters), "count": len(list_curated_sources(filters))}


@mcp.tool()
def training_sites() -> dict:
    """Return the complete list of high-value training documentation sites across the internet."""
    return {"sites": list_training_sites(), "count": len(list_training_sites())}


@mcp.tool()
def best_practices() -> dict:
    """Return governed best practices for continuous AI training with evidence URLs and priority levels."""
    return {"practices": best_practices_catalog(), "count": len(best_practices_catalog())}


@mcp.tool()
def source_policy() -> dict:
    """Return the source screening policy for documentation quality and provenance."""
    return {"policy": source_screening_policy()}


@mcp.tool()
def source_registry_list() -> dict:
    """Return the complete governed source registry with authorities and categories."""
    return {"sources": source_registry(), "count": len(source_registry())}


@mcp.tool()
def full_search(query: str, max_results: int = 20) -> dict:
    """Search across all available sources (web, arxiv, github, paperswithcode, reddit) in parallel."""
    import asyncio

    async def _full():
        coros = [
            search_web(query, max_results // 2),
            search_arxiv(query, max_results // 2),
            search_github(query, max_results // 2),
            search_paperswithcode(query, max_results // 2),
            search_reddit(query, max_results // 2),
        ]
        results = await asyncio.gather(*coros, return_exceptions=True)
        all_resources = []
        errors = []
        for r in results:
            if isinstance(r, Exception):
                errors.append(str(r))
            elif hasattr(r, "resources"):
                all_resources.extend(r.resources)
                if r.error:
                    errors.append(r.error)
        all_resources.sort(key=lambda x: x.relevance_score, reverse=True)
        return {
            "query": query,
            "total_results": len(all_resources),
            "resources": [res.model_dump(mode="json") for res in all_resources[:max_results]],
            "errors": errors if errors else None,
        }

    return asyncio.run(_full())


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
