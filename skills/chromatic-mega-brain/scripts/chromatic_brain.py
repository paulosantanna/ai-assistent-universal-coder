#!/usr/bin/env python3
"""AEOS Chromatic Mega Brain selector and run scaffold."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from pathlib import Path

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

    args = parser.parse_args()

    if args.command == "select":
        print(json.dumps({"colors": select_colors(args.problem, args.max_colors)}, indent=2))
        return 0

    run = create_run(args.problem, Path(args.output).resolve(), args.max_colors)
    print(f"CREATED: {run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
