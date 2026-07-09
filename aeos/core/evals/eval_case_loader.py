from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml

from aeos.core.evals.eval_models import EvalCase


class EvalCaseLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def load_case(self, suite_id: str, case_id: str) -> Optional[EvalCase]:
        evals_dir = self.workspace_root / "aeos" / "evals"
        if not evals_dir.exists():
            return None
        for suite_dir in evals_dir.iterdir():
            if not suite_dir.is_dir():
                continue
            if suite_dir.name != suite_id and suite_dir.name != f"suite_{suite_id}":
                continue
            cases_dir = suite_dir / "cases"
            if not cases_dir.exists():
                continue
            for case_file in cases_dir.glob("*.case.md"):
                stem = case_file.stem.replace(".case", "")
                if stem == case_id:
                    return self._parse_case_file(case_file, suite_id)
        return None

    def load_cases_for_suite(self, suite_id: str) -> list[EvalCase]:
        evals_dir = self.workspace_root / "aeos" / "evals"
        cases: list[EvalCase] = []
        if not evals_dir.exists():
            return cases
        for suite_dir in evals_dir.iterdir():
            if not suite_dir.is_dir():
                continue
            if suite_dir.name != suite_id:
                continue
            cases_dir = suite_dir / "cases"
            if not cases_dir.exists():
                continue
            for case_file in sorted(cases_dir.glob("*.case.md")):
                case = self._parse_case_file(case_file, suite_id)
                if case is not None:
                    cases.append(case)
        return cases

    def _parse_case_file(self, path: Path, suite_id: str) -> Optional[EvalCase]:
        try:
            content = path.read_text(encoding="utf-8")
            frontmatter: dict[str, Any] = {}
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                    except yaml.YAMLError:
                        frontmatter = {}
            case_id = path.stem.replace(".case", "")
            return EvalCase(
                case_id=case_id,
                suite_id=suite_id,
                description=frontmatter.get("description", ""),
                severity=frontmatter.get("severity", "medium"),
                expected=frontmatter.get("expected", ""),
                inputs=frontmatter.get("inputs", {}),
                blocking=frontmatter.get("blocking", False),
            )
        except Exception:
            return None
