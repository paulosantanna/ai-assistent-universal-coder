from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

import yaml

from aeos.core.evals.eval_models import EvalSuite, EvalCase


class EvalSuiteLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self._suites: list[EvalSuite] = []

    def load_all(self) -> list[EvalSuite]:
        self._suites.clear()
        evals_dir = self.workspace_root / "aeos" / "evals"
        if not evals_dir.exists():
            return self._suites
        for suite_dir in sorted(evals_dir.iterdir()):
            if not suite_dir.is_dir():
                continue
            suite_path = suite_dir / "suite.yaml"
            if suite_path.exists():
                suite = self._load_suite(suite_path)
                if suite is not None:
                    self._suites.append(suite)
        return self._suites

    def load_by_id(self, suite_id: str) -> Optional[EvalSuite]:
        evals_dir = self.workspace_root / "aeos" / "evals"
        if not evals_dir.exists():
            return None
        for suite_dir in sorted(evals_dir.iterdir()):
            if not suite_dir.is_dir():
                continue
            suite_path = suite_dir / "suite.yaml"
            if suite_path.exists():
                suite = self._load_suite(suite_path)
                if suite is not None and suite.suite_id == suite_id:
                    return suite
        return None

    def _load_suite(self, path: Path) -> Optional[EvalSuite]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            suite_id = data.get("id", path.parent.name)
            cases_dir = path.parent / "cases"
            cases: list[EvalCase] = []
            if cases_dir.exists():
                for case_file in sorted(cases_dir.glob("*.case.md")):
                    case = self._load_case(case_file, suite_id)
                    if case is not None:
                        cases.append(case)
            return EvalSuite(
                suite_id=suite_id,
                description=data.get("description", ""),
                cases=cases,
                blocking=data.get("blocking", False),
                min_pass_score=data.get("min_pass_score", 1.0),
            )
        except Exception:
            return None

    def _load_case(self, path: Path, suite_id: str) -> Optional[EvalCase]:
        try:
            # Parse frontmatter from .case.md
            content = path.read_text(encoding="utf-8")
            frontmatter: dict[str, Any] = {}
            body = content
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                    except yaml.YAMLError:
                        frontmatter = {}
                    body = parts[2].strip() if len(parts) > 2 else ""
            return EvalCase(
                case_id=path.stem.replace(".case", ""),
                suite_id=suite_id,
                description=frontmatter.get("description", body[:100]),
                severity=frontmatter.get("severity", "medium"),
                expected=frontmatter.get("expected", ""),
                inputs=frontmatter.get("inputs", {}),
                blocking=frontmatter.get("blocking", False),
            )
        except Exception:
            return None

    def list_suites(self) -> list[dict[str, Any]]:
        return [
            {"id": s.suite_id, "cases": len(s.cases), "blocking": s.blocking}
            for s in self._suites
        ]

    def get_suites(self) -> list[EvalSuite]:
        return list(self._suites)
