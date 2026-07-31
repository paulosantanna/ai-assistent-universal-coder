#!/usr/bin/env python3
"""AEOS Chromatic Mega Brain selector, integration inventory and run scaffold."""

from __future__ import annotations

import argparse
import json
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

COLOR_RULES = {
    "WHITE": ["evidence", "unknown", "uncertain", "fact", "source", "verify", "research"],
    "BLUE": ["architecture", "system", "dependency", "design", "migration", "scale"],
    "RED": ["security", "risk", "failure", "bug", "attack", "threat", "regression"],
    "GREEN": ["implement", "delivery", "code", "test", "deploy", "plan", "fix"],
    "YELLOW": ["optimize", "performance", "opportunity", "cost", "reuse", "improve"],
    "PURPLE": ["knowledge", "memory", "lesson", "learn", "standard", "history"],
    "ORANGE": ["user", "product", "team", "workflow", "adoption", "operation"],
    "BLACK": ["constraint", "approval", "regulatory", "clinical", "legal", "prohibited", "secret"],
}

DEFAULT_PAIRS = {
    "architecture": ["WHITE", "BLUE", "RED", "GREEN"],
    "security": ["WHITE", "RED", "BLACK", "GREEN"],
    "performance": ["WHITE", "BLUE", "YELLOW", "GREEN"],
    "strategy": ["WHITE", "BLUE", "RED", "YELLOW", "ORANGE"],
    "learning": ["WHITE", "PURPLE", "RED", "BLUE"],
}

EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
    "unsloth_compiled_cache",
}

DEFAULT_DO = [
    "route ambiguous, high-impact or cross-domain decisions through a minimal Chromatic color set",
    "record evidence references before candidate lessons are persisted",
    "store learning in the owning package memory or knowledge scope with provenance",
    "preserve do and do_not guidance separately so negative knowledge is not diluted",
]

DEFAULT_DO_NOT = [
    "do not promote raw execution output or unsupported conclusions as institutional knowledge",
    "do not activate every Chromatic color by default",
    "do not let an implementation agent judge its own work",
    "do not mark completion while required evidence, tests or learning capture are missing",
]


@dataclass(frozen=True)
class IntegratedEntity:
    entity_type: str
    entity_id: str
    path: str
    chromatic_entrypoint: str
    memory_scope: str
    do: list[str]
    do_not: list[str]
    evidence_refs: list[str]

    def to_dict(self) -> dict[str, object]:
        return {
            "type": self.entity_type,
            "id": self.entity_id,
            "path": self.path,
            "chromatic_entrypoint": self.chromatic_entrypoint,
            "memory_scope": self.memory_scope,
            "do": self.do,
            "do_not": self.do_not,
            "evidence_refs": self.evidence_refs,
        }


def _is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def _safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "unnamed"


def _front_matter_name(text: str) -> str | None:
    match = re.search(r"(?m)^name:\s*([^\n#]+)\s*$", text)
    return match.group(1).strip().strip("'\"") if match else None


def _yaml_field(text: str, field: str) -> str | None:
    match = re.search(rf"(?m)^\s{{2}}{re.escape(field)}:\s*([^\n#]+)\s*$", text)
    return match.group(1).strip().strip("'\"") if match else None


def _extract_bullets(text: str, heading_patterns: Iterable[str], limit: int = 12) -> list[str]:
    headings = "|".join(re.escape(item) for item in heading_patterns)
    pattern = re.compile(rf"(?ims)^#+\s+(?:\d+\.?\s*)?(?:{headings})\b.*?(?=^#+\s+|\Z)")
    bullets: list[str] = []
    for block in pattern.findall(text):
        for line in block.splitlines():
            stripped = line.strip()
            if stripped.startswith(("-", "*")):
                item = stripped[1:].strip()
            elif re.match(r"^\d+\.\s+", stripped):
                item = re.sub(r"^\d+\.\s+", "", stripped).strip()
            else:
                continue
            if item and item not in bullets:
                bullets.append(item)
            if len(bullets) >= limit:
                return bullets
    return bullets

def _extract_all_bullets(text: str, limit: int = 12) -> list[str]:
    bullets: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("-", "*")):
            item = stripped[1:].strip()
        elif re.match(r"^\d+\.\s+", stripped):
            item = re.sub(r"^\d+\.\s+", "", stripped).strip()
        else:
            continue
        if item and item not in bullets:
            bullets.append(item)
        if len(bullets) >= limit:
            break
    return bullets


def _load_learning_files(package_root: Path) -> tuple[list[str], list[str], list[str]]:
    do: list[str] = []
    do_not: list[str] = []
    refs: list[str] = []
    for rel, target in [
        ("knowledge/POSITIVE_KNOWLEDGE.md", do),
        ("knowledge/NEGATIVE_KNOWLEDGE.md", do_not),
        ("knowledge/CONTINUOUS_LEARNING.md", do),
        ("memory/LESSONS.md", do),
        ("memory/FAILURES.md", do_not),
        ("memory/OPEN_RISKS.md", do_not),
    ]:
        path = package_root / rel
        if not path.exists() or path.is_dir():
            continue
        refs.append(rel)
        text = _safe_read(path)
        extracted = _extract_bullets(
            text,
            [
                "Preferred patterns",
                "Known failure patterns",
                "After each run",
                "Lessons",
                "Failures",
                "Open risks",
            ],
        )
        if not extracted:
            extracted = _extract_all_bullets(text)
        target.extend(item for item in extracted if item not in target)
    return do[:12], do_not[:12], refs


def _skill_entity(path: Path, workspace_root: Path) -> IntegratedEntity:
    text = _safe_read(path)
    package_root = path.parent
    name = _front_matter_name(text) or _yaml_field(text, "slug") or package_root.name
    local_do = _extract_bullets(
        text,
        ["Allowed Actions", "Quality Gates", "Workflow", "Mission", "Completion", "Evidence"],
    )
    local_do_not = _extract_bullets(
        text,
        ["Forbidden Actions", "What not to do", "Non-activation", "Stop conditions", "Exclusions"],
    )
    knowledge_do, knowledge_do_not, learning_refs = _load_learning_files(package_root)
    do = list(dict.fromkeys(local_do + knowledge_do + DEFAULT_DO))[:16]
    do_not = list(dict.fromkeys(local_do_not + knowledge_do_not + DEFAULT_DO_NOT))[:16]
    rel_path = path.relative_to(workspace_root).as_posix()
    package_rel = package_root.relative_to(workspace_root).as_posix()
    refs = [rel_path, *[f"{package_rel}/{ref}" for ref in learning_refs]]
    return IntegratedEntity(
        entity_type="skill",
        entity_id=_slug(name),
        path=rel_path,
        chromatic_entrypoint="skill",
        memory_scope=f"{package_rel}/memory",
        do=do,
        do_not=do_not,
        evidence_refs=refs,
    )


def _playbook_entity(path: Path, workspace_root: Path) -> IntegratedEntity:
    text = _safe_read(path)
    package_root = path.parent
    name = _yaml_field(text, "id") or package_root.name
    policies = [
        item.strip()
        for item in re.findall(r"(?m)^\s*-\s+([a-zA-Z0-9][^\n#]+)\s*$", text)
        if " " not in item.strip() or item.strip().startswith(("no-", "evidence-", "memory-", "explicit-"))
    ]
    do = list(dict.fromkeys([f"honor playbook policy: {policy}" for policy in policies] + DEFAULT_DO))[:16]
    do_not = list(
        dict.fromkeys(
            [f"do not violate playbook policy: {policy}" for policy in policies if policy.startswith("no-")]
            + DEFAULT_DO_NOT
        )
    )[:16]
    rel_path = path.relative_to(workspace_root).as_posix()
    package_rel = package_root.relative_to(workspace_root).as_posix()
    return IntegratedEntity(
        entity_type="playbook",
        entity_id=_slug(name),
        path=rel_path,
        chromatic_entrypoint="playbook",
        memory_scope=f"{package_rel}/memory",
        do=do,
        do_not=do_not,
        evidence_refs=[rel_path],
    )


def discover_integrated_entities(workspace_root: Path) -> list[IntegratedEntity]:
    root = workspace_root.resolve()
    entities: list[IntegratedEntity] = []

    skill_paths = sorted(
        path
        for path in root.rglob("SKILL.md")
        if path.is_file() and not _is_excluded(path.relative_to(root))
    )
    playbook_paths = sorted(
        path
        for path in root.rglob("*.yaml")
        if path.is_file()
        and not _is_excluded(path.relative_to(root))
        and (path.name == "playbook.yaml" or path.name.endswith(".playbook.yaml"))
    )

    entities.extend(_skill_entity(path, root) for path in skill_paths)
    entities.extend(_playbook_entity(path, root) for path in playbook_paths)
    return sorted(entities, key=lambda item: (item.entity_type, item.path))


def integration_payload(workspace_root: Path) -> dict[str, object]:
    entities = discover_integrated_entities(workspace_root)
    return {
        "schema_version": "1.0.0",
        "integration": "chromatic-mega-brain-skill-playbook-learning",
        "workspace_root": workspace_root.as_posix(),
        "summary": {
            "skills": sum(1 for item in entities if item.entity_type == "skill"),
            "playbooks": sum(1 for item in entities if item.entity_type == "playbook"),
            "total": len(entities),
        },
        "learning_contract": {
            "do": DEFAULT_DO,
            "do_not": DEFAULT_DO_NOT,
            "promotion_rule": "Only evidence-backed candidate lessons reviewed by Judge or Knowledge Curator may become shared institutional knowledge.",
        },
        "entities": [item.to_dict() for item in entities],
    }


def write_integration_memory(workspace_root: Path, output_dir: Path) -> tuple[Path, Path]:
    payload = integration_payload(workspace_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "SKILL_PLAYBOOK_INTEGRATION.json"
    md_path = output_dir / "SKILL_PLAYBOOK_INTEGRATION.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    summary = payload["summary"]
    assert isinstance(summary, dict)
    lines = [
        "# Skill and Playbook Chromatic Integration",
        "",
        "Status: CANDIDATE_LEARNING",
        "Owner: Chromatic Mega Brain",
        "Validation: generated from repository files; promotion still requires Judge/Knowledge Curator review.",
        "",
        "## Summary",
        "",
        f"- skills: {summary['skills']}",
        f"- playbooks: {summary['playbooks']}",
        f"- total integrated entities: {summary['total']}",
        "",
        "## Do",
        "",
        *[f"- {item}" for item in DEFAULT_DO],
        "",
        "## Do Not",
        "",
        *[f"- {item}" for item in DEFAULT_DO_NOT],
        "",
        "## Evidence",
        "",
        f"- machine index: {json_path.name}",
        "- source files: every discovered SKILL.md, playbook.yaml and *.playbook.yaml outside excluded build/cache folders.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def select_colors(problem: str, max_colors: int = 5) -> list[str]:
    lower = problem.lower()
    scores = {color: 0 for color in COLOR_RULES}
    for color, terms in COLOR_RULES.items():
        scores[color] = sum(1 for term in terms if term in lower)

    for topic, colors in DEFAULT_PAIRS.items():
        if topic in lower:
            for color in colors:
                scores[color] += 2

    selected = [c for c, score in sorted(scores.items(), key=lambda x: (-x[1], x[0])) if score > 0]
    if "WHITE" not in selected:
        selected.insert(0, "WHITE")
    if len(selected) < 2:
        selected.append("BLUE")
    return selected[:max_colors]


def create_run(problem: str, output: Path, max_colors: int) -> Path:
    run_id = f"cbrain-{uuid.uuid4().hex[:12]}"
    colors = select_colors(problem, max_colors=max_colors)
    run_dir = output / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    data = {
        "run_id": run_id,
        "problem": problem,
        "selected_colors": colors,
        "status": "ANALYZING",
        "learning_contract": {
            "do": DEFAULT_DO,
            "do_not": DEFAULT_DO_NOT,
            "required_storage": [
                "execution evidence",
                "candidate lessons",
                "negative knowledge",
                "Judge or Curator validation status",
            ],
        },
    }
    (run_dir / "RUN.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    handoffs = run_dir / "handoffs"
    handoffs.mkdir()
    for color in colors:
        payload = {
            "run_id": run_id,
            "color": color,
            "objective": f"Analyze the problem from the {color} perspective.",
            "problem_frame": problem,
            "scope": "Assigned color contract only",
            "excluded_scope": "Final integrated decision",
            "evidence_available": [],
            "assumptions": [],
            "required_questions": [],
            "expected_output": "Structured color handback",
            "stop_conditions": ["insufficient evidence", "authority conflict", "unsafe action"],
            "memory_scope": "execution-local",
        }
        (handoffs / f"{color}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    (run_dir / "DECISION.md").write_text(
        "# Chromatic Decision\n\n"
        f"## Problem\n\n{problem}\n\n"
        f"## Selected Colors and Rationale\n\n{', '.join(colors)}\n\n"
        "## Evidence Map\n\n"
        "## Findings by Color\n\n"
        "## Contradictions\n\n"
        "## Options\n\n"
        "## Decision Matrix\n\n"
        "## Recommended Decision\n\n"
        "## Rejected Alternatives\n\n"
        "## Risks and Mitigations\n\n"
        "## Implementation Path\n\n"
        "## Validation Plan\n\n"
        "## Uncertainty\n\n"
        "## Judge Verdict\n\n"
        "## Candidate Lessons\n",
        encoding="utf-8",
    )
    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="AEOS Chromatic Mega Brain")
    sub = parser.add_subparsers(dest="command", required=True)

    select = sub.add_parser("select", help="Select cognitive colors")
    select.add_argument("--problem", required=True)
    select.add_argument("--max-colors", type=int, default=5, choices=range(2, 9))

    create = sub.add_parser("create-run", help="Create a chromatic run scaffold")
    create.add_argument("--problem", required=True)
    create.add_argument("--output", default="chromatic-runs")
    create.add_argument("--max-colors", type=int, default=5, choices=range(2, 9))

    inventory = sub.add_parser("inventory", help="Discover integrated skills and playbooks")
    inventory.add_argument("--workspace-root", default=".")
    inventory.add_argument("--json", action="store_true")

    sync = sub.add_parser("sync-integration", help="Write Chromatic skill/playbook integration memory")
    sync.add_argument("--workspace-root", default=".")
    sync.add_argument("--output-dir", default="skills/chromatic-mega-brain/memory")

    args = parser.parse_args()

    if args.command == "select":
        print(json.dumps({"colors": select_colors(args.problem, args.max_colors)}, indent=2))
        return 0

    if args.command == "inventory":
        payload = integration_payload(Path(args.workspace_root))
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            summary = payload["summary"]
            assert isinstance(summary, dict)
            print(
                "INTEGRATED: "
                f"{summary['skills']} skills, {summary['playbooks']} playbooks, {summary['total']} total"
            )
        return 0

    if args.command == "sync-integration":
        json_path, md_path = write_integration_memory(Path(args.workspace_root), Path(args.output_dir))
        print(f"WROTE: {json_path}")
        print(f"WROTE: {md_path}")
        return 0

    run = create_run(args.problem, Path(args.output).resolve(), args.max_colors)
    print(f"CREATED: {run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


