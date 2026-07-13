from __future__ import annotations

from dataclasses import dataclass, field


ALLOWED_DIAGRAM_TYPES = {
    "architecture",
    "sequence",
    "flow",
    "state",
    "er",
    "deployment",
    "dependency",
    "skill-mcp-lsp",
    "cloud-readiness",
}


@dataclass(frozen=True)
class DocumentationSection:
    id: str
    title: str
    purpose: str
    required_evidence: list[str] = field(default_factory=list)


DEFAULT_SECTIONS = [
    DocumentationSection("overview", "Overview", "Explain the system purpose and scope.", ["repository summary", "entrypoints"]),
    DocumentationSection("architecture", "Architecture", "Describe components and boundaries.", ["source tree", "module boundaries"]),
    DocumentationSection("runtime-flow", "Runtime Flow", "Show request, job or event flow.", ["controllers", "handlers", "queues"]),
    DocumentationSection("data-model", "Data Model", "Document persistent entities and relationships.", ["schemas", "models", "migrations"]),
    DocumentationSection("operations", "Operations", "Document build, run, test and deployment procedures.", ["scripts", "CI config"]),
    DocumentationSection("risks", "Risks And Assumptions", "Separate facts, assumptions, risks and blockers.", ["evidence refs", "validation results"]),
]


CLOUD_READINESS_DIMENSIONS = [
    "configuration",
    "secrets",
    "observability",
    "testing",
    "deployment",
    "rollback",
    "security",
    "documentation",
]
