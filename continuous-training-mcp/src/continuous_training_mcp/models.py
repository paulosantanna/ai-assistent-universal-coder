from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SourceCategory(str, Enum):
    documentation = "documentation"
    paper = "paper"
    repository = "repository"
    tutorial = "tutorial"
    benchmark = "benchmark"
    discussion = "discussion"
    framework = "framework"
    blog = "blog"
    video = "video"
    course = "course"


class SourceAuthority(str, Enum):
    official = "official"
    community = "community"
    academic = "academic"
    research_lab = "research_lab"
    enterprise = "enterprise"


class TrainingDomain(str, Enum):
    llm = "llm"
    vision = "vision"
    multimodal = "multimodal"
    reinforcement_learning = "reinforcement_learning"
    diffusion = "diffusion"
    speech = "speech"
    recommendation = "recommendation"
    general = "general"


class TrainingTechnique(str, Enum):
    full_fine_tuning = "full_fine_tuning"
    lora = "lora"
    qlora = "qlora"
    dora = "dora"
    rs_lora = "rs_lora"
    adapter = "adapter"
    prompt_tuning = "prompt_tuning"
    prefix_tuning = "prefix_tuning"
    p_tuning = "p_tuning"
    continual_pretraining = "continual_pretraining"
    distillation = "distillation"
    quantization_aware = "quantization_aware"
    curriculum_learning = "curriculum_learning"
    active_learning = "active_learning"
    self_supervised = "self_supervised"
    contrastive = "contrastive"
    federated = "federated"
    online = "online"
    incremental = "incremental"
    rehearsal = "rehearsal"
    regularization_based = "regularization_based"
    architecture_based = "architecture_based"
    memory_replay = "memory_replay"


class Framework(str, Enum):
    pytorch = "pytorch"
    tensorflow = "tensorflow"
    jax = "jax"
    mxnet = "mxnet"
    flax = "flax"
    transformers = "transformers"
    unsloth = "unsloth"
    axolotl = "axolotl"
    trl = "trl"
    peft = "peft"
    accelerate = "accelerate"
    deepspeed = "deepspeed"
    megatron = "megatron"
    nemo = "nemo"
    colossalai = "colossalai"
    horovod = "horovod"
    fairseq = "fairseq"
    mlx = "mlx"
    llama_cpp = "llama_cpp"
    vllm = "vllm"
    sglang = "sglang"
    tgi = "tgi"
    tensorrt_llm = "tensorrt_llm"


class DocumentationSource(BaseModel):
    name: str
    url: str
    category: SourceCategory
    authority: SourceAuthority
    domains: list[TrainingDomain] = []
    techniques: list[TrainingTechnique] = []
    frameworks: list[Framework] = []
    language: str = "en"
    description: str = ""
    last_verified: str = ""


class FetchResult(BaseModel):
    url: str
    title: str = ""
    content_markdown: str = ""
    content_text: str = ""
    source: str = ""
    fetched_at: str = ""
    status_code: int = 0
    error: str | None = None
    content_hash: str = ""


class DiscoveredResource(BaseModel):
    title: str
    url: str
    source: str
    snippet: str = ""
    relevance_score: float = 0.0
    category: SourceCategory = SourceCategory.documentation
    domain: TrainingDomain = TrainingDomain.general
    technique: TrainingTechnique | None = None
    framework: Framework | None = None
    retrieved_at: str = ""


class SearchResult(BaseModel):
    query: str
    total_results: int = 0
    resources: list[DiscoveredResource] = []
    error: str | None = None


class BestPractice(BaseModel):
    id: str
    title: str
    description: str
    domain: TrainingDomain
    technique: TrainingTechnique | None = None
    framework: Framework | None = None
    priority: int = Field(ge=1, le=5, default=3)
    evidence_urls: list[str] = []
    tags: list[str] = []


class ContinuousTrainingConfig(BaseModel):
    max_sources_per_search: int = 20
    request_timeout: int = 30
    max_concurrent_requests: int = 5
    cache_ttl_seconds: int = 3600
    rate_limit_per_domain: float = 1.0
    user_agent: str = "AEOS-ContinuousTraining-MCP/1.0"
    respect_robots: bool = True
    enable_ts_scraper: bool = False
