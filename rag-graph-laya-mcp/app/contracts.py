"""One schema source for MCP tools and the local HTTP API."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Input(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Empty(Input):
    pass


class SourceRefresh(Input):
    source_ids: list[str] = Field(min_length=1, max_length=100)


class Ingest(Input):
    source_id: str
    text: str | None = Field(default=None, max_length=2_000_000)
    action: Literal['index', 'remove'] = 'index'
    document_id: str | None = None


class Search(Input):
    query: str = Field(min_length=1, max_length=4000)
    limit: int = Field(default=10, ge=1, le=50)
    strategy: Literal['hybrid', 'lexical', 'graph', 'laya'] = 'hybrid'


class ReversaSearch(Input):
    query: str = Field(min_length=1, max_length=4000)
    limit: int = Field(default=5, ge=1, le=20)
    strategy: Literal['lexical', 'hybrid'] = 'lexical'


class Snapshot(Input):
    limit: int = Field(default=500, ge=1, le=2000)


class Neighbors(Input):
    node_id: str


class Decision(Input):
    state: str = Field(min_length=1, max_length=10000)
    questions: dict = Field(min_length=1, max_length=20)


class Dataset(Input):
    count: int = Field(default=2000, ge=20, le=10000)
    seed: int = 42
    generation: Literal['extractive', 'teacher'] = 'extractive'


class Train(Input):
    flow: Literal['laya', 'llm']
    dataset_id: str
    epochs: int = Field(default=2, ge=1, le=4)
    seed: int = 42


class Evaluate(Input):
    flow: Literal['laya', 'llm']
    dataset_id: str
    checkpoint: str | None = None
    require_human_review: bool = True
    seed: int = 42


class Job(Input):
    job_id: str


OPERATIONS = {
    'health': (Empty, 'Report actual runtime prerequisites; no model weights loaded.'),
    'sources_list': (Empty, 'List discovered/acquired/analyzed sources and provenance.'),
    'sources_refresh': (SourceRefresh, 'Acquire allowlisted official sources; returns a durable job_id.'),
    'ingest': (Ingest, 'Index or remove source-grounded documents with incremental Graphiti updates.'),
    'search': (Search, 'Retrieve evidence with lexical, graph, hybrid or Laya reranking.'),
    'answer': (Search, 'Generate a cited answer from active evidence or abstain.'),
    'reversa_search': (ReversaSearch, 'Search the local Reversa source index with file, line and hash provenance.'),
    'reversa_answer': (ReversaSearch, 'Generate a cited answer from current local Reversa source passages.'),
    'graph_snapshot': (Snapshot, 'Return a bounded graph snapshot and SSE replay cursor.'),
    'graph_neighbors': (Neighbors, 'Return one-hop neighbors and source provenance.'),
    'laya_decide': (Decision, 'Answer typed questions using the official Laya SDK; no text generation.'),
    'dataset_prepare': (Dataset, 'Generate source-family-disjoint domain datasets and human review exports.'),
    'train': (Train, 'Run a bounded, sequential Laya RLCD or LLM QLoRA experiment.'),
    'evaluate': (Evaluate, 'Compare model quality on a held-out dataset; human review is explicit.'),
    'job_status': (Job, 'Read persistent progress, result or actionable failure for a job.'),
    'job_cancel': (Job, 'Cancel a queued/running job; confirmed graph changes remain committed.'),
}


def tool_specs():
    return [{'name': name, 'description': description, 'inputSchema': model.model_json_schema()}
            for name, (model, description) in OPERATIONS.items()]
