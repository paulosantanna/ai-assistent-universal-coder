from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from aeos.core.judge.judge_models import JudgeInput, JudgeResult, JudgeScorecard


class JudgeGateLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)

    def load_judge_input(self, execution_id: str) -> Optional[JudgeInput]:
        path = self.workspace_root / ".aeos" / "evidence" / execution_id / "judge-input.json"
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return JudgeInput(**data)
        except (json.JSONDecodeError, IOError, TypeError):
            return None

    def save_judge_input(self, judge_input: JudgeInput) -> str:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / judge_input.execution_id
        evidence_dir.mkdir(parents=True, exist_ok=True)
        fp = evidence_dir / "judge-input.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(judge_input.to_dict(), f, indent=2, default=str)
        return str(fp)

    def save_judge_result(self, result: JudgeResult) -> str:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / result.execution_id
        evidence_dir.mkdir(parents=True, exist_ok=True)
        fp = evidence_dir / "judge-result.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, default=str)
        return str(fp)

    def save_scorecard(self, scorecard: JudgeScorecard) -> str:
        evidence_dir = self.workspace_root / ".aeos" / "evidence" / scorecard.execution_id
        evidence_dir.mkdir(parents=True, exist_ok=True)
        fp = evidence_dir / "judge-scorecard.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(scorecard.to_dict(), f, indent=2, default=str)
        return str(fp)

    def load_judge_result(self, execution_id: str) -> Optional[JudgeResult]:
        path = self.workspace_root / ".aeos" / "evidence" / execution_id / "judge-result.json"
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return JudgeResult(**data)
        except (json.JSONDecodeError, IOError, TypeError):
            return None

    def load_latest_judge_result(self) -> Optional[JudgeResult]:
        evidence_root = self.workspace_root / ".aeos" / "evidence"
        if not evidence_root.exists():
            return None
        dirs = sorted(
            [d for d in evidence_root.iterdir() if d.is_dir()],
            key=lambda d: d.stat().st_mtime, reverse=True,
        )
        for d in dirs:
            result = self.load_judge_result(d.name)
            if result is not None:
                return result
        return None
