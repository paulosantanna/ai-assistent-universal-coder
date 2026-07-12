from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from .models import (
    DiscoveredResource,
    FetchResult,
    SearchResult,
    SourceCategory,
    TrainingDomain,
)

USER_AGENT = "AEOS-ContinuousTraining-MCP/1.0"
REQUEST_TIMEOUT = 30.0

CONTINUOUS_TRAINING_SITES: list[dict[str, str]] = [
    {"name": "GitHub", "url": "https://github.com/search", "type": "repository"},
    {"name": "arXiv", "url": "https://arxiv.org/search", "type": "paper"},
    {"name": "Papers with Code", "url": "https://paperswithcode.com/search", "type": "benchmark"},
    {"name": "Hugging Face Docs", "url": "https://huggingface.co/docs", "type": "documentation"},
    {"name": "Reddit", "url": "https://www.reddit.com/search", "type": "discussion"},
    {"name": "Stack Overflow", "url": "https://stackoverflow.com/search", "type": "discussion"},
    {"name": "Medium", "url": "https://medium.com/search", "type": "blog"},
    {"name": "YouTube", "url": "https://www.youtube.com/results", "type": "video"},
    {"name": "PyTorch Docs", "url": "https://pytorch.org/docs/stable/", "type": "documentation"},
    {"name": "TensorFlow Docs", "url": "https://www.tensorflow.org/guide", "type": "documentation"},
    {"name": "DeepSpeed Docs", "url": "https://www.deepspeed.ai/docs/", "type": "documentation"},
    {"name": "Unsloth Docs", "url": "https://docs.unsloth.ai/", "type": "documentation"},
    {"name": "Hugging Face PEFT", "url": "https://huggingface.co/docs/peft", "type": "documentation"},
    {"name": "NVIDIA Docs", "url": "https://docs.nvidia.com/deeplearning/", "type": "documentation"},
    {"name": "MLCommons", "url": "https://mlcommons.org/", "type": "benchmark"},
]


async def fetch_page(url: str, timeout: int = 30) -> FetchResult:
    now = datetime.now(timezone.utc).isoformat()
    try:
        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            content = response.text

            soup = BeautifulSoup(content, "lxml")
            title = ""
            if soup.title and soup.title.string:
                title = soup.title.string.strip()

            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            text = soup.get_text(separator="\n", strip=True)
            text = re.sub(r"\n{3,}", "\n\n", text)

            content_hash_val = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

            return FetchResult(
                url=url,
                title=title,
                content_text=text[:100000],
                source=urlparse(url).netloc,
                fetched_at=now,
                status_code=response.status_code,
                content_hash=content_hash_val,
            )
    except httpx.TimeoutException:
        return FetchResult(url=url, status_code=0, error=f"Request timed out after {timeout}s", fetched_at=now)
    except httpx.HTTPStatusError as e:
        return FetchResult(url=url, status_code=e.response.status_code, error=f"HTTP {e.response.status_code}", fetched_at=now)
    except Exception as e:
        return FetchResult(url=url, status_code=0, error=str(e), fetched_at=now)


async def search_web(query: str, max_results: int = 20) -> SearchResult:
    query_terms = _build_search_query(query)
    resources: list[DiscoveredResource] = []
    now = datetime.now(timezone.utc).isoformat()

    search_urls = _generate_search_urls(query_terms)

    async with httpx.AsyncClient(
        timeout=REQUEST_TIMEOUT,
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT},
    ) as client:
        for entry in search_urls[:max_results * 2]:
            try:
                resp = await client.get(entry["url"])
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "lxml")
                    results = _extract_results_from_html(soup, entry["source"])
                    for r in results:
                        r.retrieved_at = now
                        resources.append(r)
                        if len(resources) >= max_results:
                            break
                if len(resources) >= max_results:
                    break
            except Exception:
                continue

    return SearchResult(query=query, total_results=len(resources), resources=resources[:max_results])


async def search_arxiv(query: str, max_results: int = 20) -> SearchResult:
    url = "https://export.arxiv.org/api/query"
    safe_query = _build_search_query(query)
    params = {
        "search_query": f"all:{safe_query}",
        "start": 0,
        "max_results": min(max_results, 50),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    now = datetime.now(timezone.utc).isoformat()
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            resources = _parse_arxiv_atom(resp.text, now)
            return SearchResult(query=query, total_results=len(resources), resources=resources[:max_results])
    except Exception as e:
        return SearchResult(query=query, error=str(e))


async def search_paperswithcode(query: str, max_results: int = 20) -> SearchResult:
    now = datetime.now(timezone.utc).isoformat()
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            resp = await client.get(
                "https://paperswithcode.com/api/v1/search/",
                params={"q": query, "items_per_page": min(max_results, 50)},
            )
            resp.raise_for_status()
            data = resp.json()
            resources = []
            for item in data.get("results", []):
                resources.append(DiscoveredResource(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    source="paperswithcode",
                    snippet=item.get("abstract", "")[:300],
                    relevance_score=item.get("relevance", 0.0),
                    category=SourceCategory.benchmark,
                    retrieved_at=now,
                ))
            return SearchResult(query=query, total_results=len(resources), resources=resources[:max_results])
    except Exception as e:
        return SearchResult(query=query, error=str(e))


async def search_github(query: str, max_results: int = 20) -> SearchResult:
    now = datetime.now(timezone.utc).isoformat()
    try:
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"},
        ) as client:
            resp = await client.get(
                "https://api.github.com/search/repositories",
                params={"q": _build_search_query(query) + " topic:machine-learning", "per_page": min(max_results, 30), "sort": "stars"},
            )
            resp.raise_for_status()
            data = resp.json()
            resources = []
            for item in data.get("items", []):
                resources.append(DiscoveredResource(
                    title=item.get("full_name", ""),
                    url=item.get("html_url", ""),
                    source="github",
                    snippet=item.get("description", "")[:300],
                    relevance_score=item.get("score", 0.0),
                    category=SourceCategory.repository,
                    domain=_infer_domain_from_text(item.get("description", "") + str(item.get("topics", []))),
                    retrieved_at=now,
                ))
            return SearchResult(query=query, total_results=len(resources), resources=resources[:max_results])
    except Exception as e:
        return SearchResult(query=query, error=str(e))


async def search_reddit(query: str, max_results: int = 20) -> SearchResult:
    now = datetime.now(timezone.utc).isoformat()
    try:
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        ) as client:
            resp = await client.get(
                "https://www.reddit.com/search.json",
                params={"q": _build_search_query(query), "limit": min(max_results, 25), "sort": "relevance", "t": "year"},
            )
            resp.raise_for_status()
            data = resp.json()
            resources = []
            for child in data.get("data", {}).get("children", []):
                item = child.get("data", {})
                resources.append(DiscoveredResource(
                    title=item.get("title", ""),
                    url=f"https://www.reddit.com{item.get('permalink', '')}",
                    source="reddit",
                    snippet=item.get("selftext", "")[:300],
                    relevance_score=item.get("score", 0),
                    category=SourceCategory.discussion,
                    retrieved_at=now,
                ))
            return SearchResult(query=query, total_results=len(resources), resources=resources[:max_results])
    except Exception as e:
        return SearchResult(query=query, error=str(e))


def list_curated_sources(filters: dict | None = None) -> list[dict]:
    from .sources import CURATED_SOURCES

    sources = CURATED_SOURCES
    if filters:
        if "domain" in filters:
            sources = [s for s in sources if filters["domain"] in [d.value for d in s.domains]]
        if "technique" in filters:
            sources = [s for s in sources if filters["technique"] in [t.value for t in s.techniques]]
        if "framework" in filters:
            sources = [s for s in sources if filters["framework"] in [f.value for f in s.frameworks]]
        if "category" in filters:
            sources = [s for s in sources if s.category.value == filters["category"]]
        if "authority" in filters:
            sources = [s for s in sources if s.authority.value == filters["authority"]]
    return [s.model_dump() for s in sources]


def list_training_sites() -> list[dict]:
    return CONTINUOUS_TRAINING_SITES


def content_hash(payload: dict) -> str:
    raw = str(sorted(payload.items()))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def _build_search_query(query: str) -> str:
    return query.strip().replace(" ", "+")


def _generate_search_urls(query: str) -> list[dict[str, str]]:
    return [
        {"url": f"https://html.duckduckgo.com/html/?q={query}+machine+learning+training", "source": "duckduckgo"},
        {"url": f"https://www.google.com/search?q={query}+machine+learning+training", "source": "google"},
    ]


def _infer_category(url: str = "", text: str = "") -> SourceCategory:
    url_lower = url.lower()
    text_lower = text.lower()
    if any(d in url_lower for d in ["arxiv.org", "research", "paper"]):
        return SourceCategory.paper
    if any(d in url_lower for d in ["github.com", "gitlab", "bitbucket"]):
        return SourceCategory.repository
    if any(d in url_lower for d in ["paperswithcode", "benchmark"]):
        return SourceCategory.benchmark
    if any(d in url_lower for d in ["reddit.com", "stackoverflow", "discuss"]):
        return SourceCategory.discussion
    if any(d in url_lower for d in ["youtube", "video"]):
        return SourceCategory.video
    if any(d in url_lower for d in ["course", "learn", "tutorial"]):
        return SourceCategory.tutorial
    if any(d in url_lower for d in ["blog", "medium", "wordpress"]):
        return SourceCategory.blog
    if any(d in url_lower for d in ["framework", "pytorch", "tensorflow", "axolotl", "unsloth"]):
        return SourceCategory.framework
    if any(d in url_lower for d in ["docs", "documentation", "guide", "readthedocs"]):
        return SourceCategory.documentation
    return SourceCategory.documentation


def _infer_domain_from_text(text: str | list) -> TrainingDomain:
    if isinstance(text, list):
        text = " ".join(text)
    text = text.lower()
    if any(d in text for d in ["llm", "language model", "gpt", "transformer", "nlp"]):
        return TrainingDomain.llm
    if any(d in text for d in ["vision", "image", "cnn", "resnet", "vit"]):
        return TrainingDomain.vision
    if any(d in text for d in ["multimodal", "vision-language", "clip"]):
        return TrainingDomain.multimodal
    if any(d in text for d in ["reinforcement", "rlhf", "dpo", "ppo"]):
        return TrainingDomain.reinforcement_learning
    if any(d in text for d in ["diffusion", "stable diffusion", "dalle"]):
        return TrainingDomain.diffusion
    if any(d in text for d in ["speech", "audio", "whisper", "wav2vec"]):
        return TrainingDomain.speech
    return TrainingDomain.general


def _extract_results_from_html(soup: BeautifulSoup, source: str) -> list[DiscoveredResource]:
    results: list[DiscoveredResource] = []
    now = datetime.now(timezone.utc).isoformat()
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        text = link.get_text(strip=True)
        if not text or len(text) < 10:
            continue
        if "http" not in href and not href.startswith("/"):
            continue
        full_url = href if href.startswith("http") else f"https://{source}{href}"
        results.append(DiscoveredResource(
            title=text[:200],
            url=full_url,
            source=source,
            snippet="",
            category=_infer_category(url=href),
            domain=_infer_domain_from_text(text),
            retrieved_at=now,
        ))
    return results


def _parse_arxiv_atom(xml_text: str, now: str) -> list[DiscoveredResource]:
    resources: list[DiscoveredResource] = []
    try:
        soup = BeautifulSoup(xml_text, "lxml-xml")
        for entry in soup.find_all("entry"):
            title = entry.find("title")
            title_text = title.text.strip() if title else ""
            link = entry.find("link")
            url = link.get("href", "") if link else ""
            summary = entry.find("summary")
            snippet = summary.text.strip()[:300] if summary else ""
            resources.append(DiscoveredResource(
                title=title_text,
                url=url,
                source="arxiv",
                snippet=snippet,
                category=SourceCategory.paper,
                domain=_infer_domain_from_text(title_text + " " + snippet),
                retrieved_at=now,
            ))
    except Exception:
        pass
    return resources
