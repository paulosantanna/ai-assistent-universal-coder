import pytest
from datetime import datetime, timezone

from continuous_training_mcp.models import (
    BestPractice,
    ContinuousTrainingConfig,
    DiscoveredResource,
    DocumentationSource,
    FetchResult,
    SearchResult,
    SourceAuthority,
    SourceCategory,
    TrainingDomain,
    TrainingTechnique,
)
from continuous_training_mcp.sources import BEST_PRACTICES, CURATED_SOURCES
from continuous_training_mcp.research import (
    _build_search_query,
    _infer_category,
    _infer_domain_from_text,
    content_hash,
)


class TestModels:
    def test_documentation_source_defaults(self):
        src = DocumentationSource(name="Test", url="https://example.com", category=SourceCategory.documentation, authority=SourceAuthority.official)
        assert src.language == "en"
        assert src.last_verified == ""

    def test_best_practice_priority_bounds(self):
        with pytest.raises(ValueError):
            BestPractice(id="x", title="x", description="x", domain=TrainingDomain.general, priority=0)
        with pytest.raises(ValueError):
            BestPractice(id="x", title="x", description="x", domain=TrainingDomain.general, priority=6)

    def test_discovered_resource_defaults(self):
        r = DiscoveredResource(title="Test", url="https://example.com", source="test")
        assert r.relevance_score == 0.0
        assert r.category == SourceCategory.documentation
        assert r.domain == TrainingDomain.general

    def test_fetch_result_defaults(self):
        r = FetchResult(url="https://example.com", status_code=200)
        assert r.title == ""
        assert r.error is None

    def test_search_result_defaults(self):
        r = SearchResult(query="test")
        assert r.total_results == 0
        assert r.resources == []

    def test_config_defaults(self):
        c = ContinuousTrainingConfig()
        assert c.max_sources_per_search == 20
        assert c.request_timeout == 30
        assert c.rate_limit_per_domain == 1.0


class TestSources:
    def test_curated_sources_populated(self):
        assert len(CURATED_SOURCES) >= 20

    def test_curated_sources_have_urls(self):
        for s in CURATED_SOURCES:
            assert s.url.startswith("http"), f"{s.name} missing URL"

    def test_best_practices_populated(self):
        assert len(BEST_PRACTICES) >= 10

    def test_best_practices_have_ids(self):
        for bp in BEST_PRACTICES:
            assert bp.id.startswith("bp-"), f"Missing bp- prefix: {bp.id}"


class TestResearch:
    def test_build_search_query(self):
        assert _build_search_query("hello world") == "hello+world"
        assert _build_search_query("  spaced  ") == "spaced"

    def test_infer_category_paper(self):
        assert _infer_category(url="https://arxiv.org/abs/2301.12345") == SourceCategory.paper

    def test_infer_category_github(self):
        assert _infer_category(url="https://github.com/user/repo") == SourceCategory.repository

    def test_infer_category_reddit(self):
        assert _infer_category(url="https://www.reddit.com/r/MachineLearning/") == SourceCategory.discussion

    def test_infer_domain_llm(self):
        assert _infer_domain_from_text("LLM fine-tuning with transformers") == TrainingDomain.llm

    def test_infer_domain_vision(self):
        assert _infer_domain_from_text("convolutional neural network image classification resnet") == TrainingDomain.vision

    def test_infer_domain_general(self):
        assert _infer_domain_from_text("some random text") == TrainingDomain.general

    def test_content_hash_deterministic(self):
        p1 = {"a": 1, "b": 2}
        p2 = {"b": 2, "a": 1}
        assert content_hash(p1) == content_hash(p2)

    def test_content_hash_different(self):
        assert content_hash({"a": 1}) != content_hash({"a": 2})
