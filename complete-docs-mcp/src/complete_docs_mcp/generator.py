from __future__ import annotations

import re

from .models import ALLOWED_DIAGRAM_TYPES, CLOUD_READINESS_DIMENSIONS, DEFAULT_SECTIONS


def documentation_plan(scope: str, audience: str = "engineering", depth: str = "complete") -> dict:
    sections = [
        {
            "id": section.id,
            "title": section.title,
            "purpose": section.purpose,
            "required_evidence": section.required_evidence,
        }
        for section in DEFAULT_SECTIONS
    ]
    return {
        "status": "PASS",
        "scope": scope,
        "audience": audience,
        "depth": depth,
        "sections": sections,
        "required_diagrams": ["architecture", "sequence", "dependency", "skill-mcp-lsp", "cloud-readiness"],
        "quality_gates": [
            "Every factual claim cites evidence.",
            "Every Mermaid diagram has a prose explanation and evidence refs.",
            "Assumptions and blockers are explicit.",
            "No secrets or sensitive values are included.",
            "Cloud readiness is scored from explicit evidence only.",
            "Architecture decisions that change runtime behavior produce ADR candidates.",
        ],
        "blocking_conditions": [],
    }


def mermaid_template(diagram_type: str, title: str = "System") -> dict:
    if diagram_type not in ALLOWED_DIAGRAM_TYPES:
        return {
            "status": "BLOCKED",
            "diagram_type": diagram_type,
            "blocking_conditions": [f"Unsupported diagram type: {diagram_type}"],
        }
    templates = {
        "architecture": f"flowchart TD\n  Client[Client] --> API[{title} API]\n  API --> Service[Service Layer]\n  Service --> Store[(Data Store)]",
        "sequence": f"sequenceDiagram\n  participant User\n  participant {safe_mermaid_id(title)}\n  User->>{safe_mermaid_id(title)}: Request\n  {safe_mermaid_id(title)}-->>User: Response",
        "flow": "flowchart TD\n  Start([Start]) --> Validate[Validate input]\n  Validate --> Execute[Execute]\n  Execute --> Done([Done])",
        "state": "stateDiagram-v2\n  [*] --> Draft\n  Draft --> Review\n  Review --> Published\n  Review --> Draft",
        "er": "erDiagram\n  ENTITY ||--o{ CHILD : owns\n  ENTITY {\n    string id\n    string name\n  }",
        "deployment": f"flowchart TD\n  CI[CI Pipeline] --> Artifact[Artifact]\n  Artifact --> Runtime[{title} Runtime]\n  Runtime --> Observability[Logs and Metrics]",
        "dependency": f"flowchart LR\n  {safe_mermaid_id(title)} --> DependencyA[Dependency A]\n  {safe_mermaid_id(title)} --> DependencyB[Dependency B]",
        "skill-mcp-lsp": (
            "flowchart TD\n"
            "  Skill[Skill] --> Router[Tool Router]\n"
            "  Router --> MCP[MCP]\n"
            "  Router --> LSP[LSP]\n"
            "  MCP --> Evidence[Evidence]"
        ),
        "cloud-readiness": (
            "flowchart TD\n"
            "  Package[Documentation Package] --> Readiness[Cloud Readiness]\n"
            "  Readiness --> Gates[Quality Gates]\n"
            "  Gates --> Decision{Deployable?}\n"
            "  Decision -->|Yes| Release[Cloud Deployment Candidate]\n"
            "  Decision -->|No| Backlog[Remediation Backlog]"
        ),
    }
    return {
        "status": "PASS",
        "diagram_type": diagram_type,
        "mermaid": templates[diagram_type],
        "usage_rules": [
            "Replace placeholder nodes with evidence-backed component names.",
            "Keep diagrams compact and split large graphs by concern.",
            "Do not include secrets, tokens, hostnames or credentials.",
        ],
        "blocking_conditions": [],
    }


def validate_mermaid(source: str) -> dict:
    stripped = source.strip()
    if not stripped:
        return {"status": "BLOCKED", "issues": ["Mermaid source is empty"], "blocking_conditions": ["empty diagram"]}
    first = stripped.splitlines()[0].strip()
    allowed_prefixes = (
        "flowchart",
        "sequenceDiagram",
        "stateDiagram",
        "stateDiagram-v2",
        "erDiagram",
        "classDiagram",
        "journey",
        "gantt",
        "timeline",
        "quadrantChart",
        "mindmap",
        "requirementDiagram",
        "block-beta",
        "architecture-beta",
    )
    issues = []
    if not first.startswith(allowed_prefixes):
        issues.append(f"Unsupported or missing Mermaid diagram header: {first}")
    if re.search(r"(?i)(password|secret|token|api[_-]?key|credential)", stripped):
        issues.append("Diagram appears to contain sensitive key names; redact before publishing.")
    if len(stripped.splitlines()) > 120:
        issues.append("Diagram is too large; split it into smaller diagrams.")
    return {
        "status": "PASS" if not issues else "REVIEW",
        "issues": issues,
        "line_count": len(stripped.splitlines()),
        "blocking_conditions": [],
    }


def documentation_package(scope: str, audience: str = "engineering", include_diagrams: bool = True) -> dict:
    plan = documentation_plan(scope, audience)
    diagrams = []
    if include_diagrams:
        for diagram_type in plan["required_diagrams"]:
            diagrams.append(mermaid_template(diagram_type, scope))
    artifact_files = architecture_documentation_files(scope, audience, diagrams)
    return {
        "status": "PASS",
        "plan": plan,
        "diagrams": diagrams,
        "output_files": [artifact["path"] for artifact in artifact_files],
        "artifacts": artifact_files,
        "adr_candidates": adr_candidates(scope),
        "cloud_readiness": cloud_readiness_matrix(),
        "evidence_required": [
            "files inspected",
            "component boundaries",
            "runtime entrypoints",
            "build/test commands",
            "generated diagrams",
            "deployment configuration",
            "observability configuration",
            "rollback procedure",
            "security gates",
        ],
        "blocking_conditions": [],
    }


def safe_mermaid_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "", value.title().replace(" ", ""))
    return cleaned or "System"


def architecture_package(scope: str, audience: str = "engineering", maturity_target: str = "cloud-ready") -> dict:
    package = documentation_package(scope, audience, include_diagrams=True)
    package["maturity_target"] = maturity_target
    package["review_order"] = [
        "README.md",
        "docs/ARCHITECTURE.md",
        "docs/RUNTIME_FLOW.md",
        "docs/SKILLS_MCPS_LSPS.md",
        "docs/CLOUD_READINESS.md",
        "docs/adr/0001-documentation-architecture-package.md",
    ]
    package["plan"]["quality_gates"].append("Package is reviewable as a cloud deployment readiness input.")
    return package


def architecture_documentation_files(scope: str, audience: str, diagrams: list[dict]) -> list[dict]:
    diagram_by_type = {diagram.get("diagram_type"): diagram.get("mermaid", "") for diagram in diagrams}
    return [
        {
            "path": "README.md",
            "purpose": "Technical onboarding entrypoint.",
            "content": "\n".join(
                [
                    f"# {scope}",
                    "",
                    "## Purpose",
                    f"Document `{scope}` for {audience} with evidence-backed architecture, operation and readiness notes.",
                    "",
                    "## Start Here",
                    "- Read `docs/ARCHITECTURE.md` for component boundaries.",
                    "- Read `docs/RUNTIME_FLOW.md` for execution flow.",
                    "- Read `docs/SKILLS_MCPS_LSPS.md` for AEOS skill, MCP and LSP routing.",
                    "- Read `docs/CLOUD_READINESS.md` before cloud deployment planning.",
                    "",
                    "## Evidence Rules",
                    "- Every factual claim must cite inspected files or tool output.",
                    "- Unknowns must remain explicit assumptions or blockers.",
                    "- Secrets and sensitive values must be redacted.",
                ]
            ),
        },
        {
            "path": "docs/ARCHITECTURE.md",
            "purpose": "Architecture map with Mermaid topology.",
            "content": markdown_with_diagram(
                "Architecture",
                "Component boundaries, entrypoints and data stores must be filled from inspected repository evidence.",
                diagram_by_type.get("architecture", ""),
                ["source tree", "module boundaries", "runtime entrypoints"],
            ),
        },
        {
            "path": "docs/RUNTIME_FLOW.md",
            "purpose": "Runtime and request/job/event flow.",
            "content": markdown_with_diagram(
                "Runtime Flow",
                "Describe how input becomes validated work, execution and output.",
                diagram_by_type.get("sequence", ""),
                ["handlers", "commands", "queues", "tests"],
            ),
        },
        {
            "path": "docs/SKILLS_MCPS_LSPS.md",
            "purpose": "Map how skills, MCPs and LSP services cooperate.",
            "content": markdown_with_diagram(
                "Skills, MCPs And LSPs",
                "Document execution boundaries between skills, Tool Router, MCP tools, LSP validation and evidence.",
                diagram_by_type.get("skill-mcp-lsp", ""),
                ["skills registry", "MCP registry", "LSP commands", "allowlist"],
            ),
        },
        {
            "path": "docs/CLOUD_READINESS.md",
            "purpose": "Cloud maturity scorecard and deployment blockers.",
            "content": cloud_readiness_markdown(diagram_by_type.get("cloud-readiness", "")),
        },
        {
            "path": "docs/adr/0001-documentation-architecture-package.md",
            "purpose": "ADR template for adopting evidence-backed architecture documentation packages.",
            "content": adr_markdown(scope),
        },
    ]


def markdown_with_diagram(title: str, body: str, mermaid: str, evidence: list[str]) -> str:
    evidence_lines = "\n".join(f"- {item}" for item in evidence)
    diagram_block = f"```mermaid\n{mermaid}\n```" if mermaid else "_Diagram pending evidence._"
    return "\n".join(
        [
            f"# {title}",
            "",
            body,
            "",
            "## Diagram",
            "",
            diagram_block,
            "",
            "## Required Evidence",
            "",
            evidence_lines,
            "",
            "## Assumptions",
            "",
            "- Add only assumptions that remain after repository inspection.",
            "",
            "## Blockers",
            "",
            "- Add blockers when required evidence is missing.",
        ]
    )


def cloud_readiness_markdown(mermaid: str) -> str:
    rows = "\n".join(
        f"| {dimension} | REVIEW | Evidence required before marking PASS |" for dimension in CLOUD_READINESS_DIMENSIONS
    )
    diagram_block = f"```mermaid\n{mermaid}\n```" if mermaid else "_Diagram pending evidence._"
    return "\n".join(
        [
            "# Cloud Readiness",
            "",
            "Use this report before any cloud deployment decision. Scores must be changed only from inspected evidence.",
            "",
            "## Decision Flow",
            "",
            diagram_block,
            "",
            "## Scorecard",
            "",
            "| Dimension | Status | Evidence Rule |",
            "| --- | --- | --- |",
            rows,
            "",
            "## Deployment Gate",
            "",
            "- `PASS`: all blocking dimensions have inspected evidence.",
            "- `REVIEW`: evidence exists but needs human confirmation.",
            "- `BLOCKED`: required evidence is missing or a quality gate fails.",
        ]
    )


def adr_markdown(scope: str) -> str:
    return "\n".join(
        [
            "# ADR 0001: Adopt Evidence-Backed Architecture Documentation Package",
            "",
            "## Status",
            "",
            "Proposed",
            "",
            "## Context",
            "",
            f"`{scope}` needs a repeatable documentation package before cloud maturity review.",
            "",
            "## Decision",
            "",
            "Use the complete-docs MCP to generate README, architecture, runtime, skill/MCP/LSP and cloud readiness artifacts.",
            "",
            "## Consequences",
            "",
            "- Documentation claims must be backed by inspected repository evidence.",
            "- Mermaid diagrams must be validated before publication.",
            "- Cloud deployment planning must consume the readiness scorecard.",
        ]
    )


def adr_candidates(scope: str) -> list[dict]:
    return [
        {
            "id": "0001-documentation-architecture-package",
            "title": "Adopt evidence-backed architecture documentation package",
            "status": "proposed",
            "trigger": f"{scope} requires repeatable documentation before cloud maturity review.",
            "required_evidence": ["documentation skill output", "complete-docs package", "registry validation"],
        },
        {
            "id": "0002-cloud-readiness-gates",
            "title": "Use explicit readiness gates before cloud deployment",
            "status": "proposed",
            "trigger": "Cloud deployment should proceed only after configuration, secrets, observability, tests and rollback evidence are present.",
            "required_evidence": ["deployment config", "CI results", "rollback plan", "security gates"],
        },
    ]


def cloud_readiness_matrix() -> list[dict]:
    return [
        {
            "dimension": dimension,
            "status": "REVIEW",
            "evidence_required": f"Inspect {dimension} files, config, tests or runbooks before marking PASS.",
        }
        for dimension in CLOUD_READINESS_DIMENSIONS
    ]
