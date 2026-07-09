from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from aeos.core.judge.judge_models import JudgeInput, JudgeResult, JudgeScorecard, JudgeStatus, JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED, JUDGE_STATUS_ERROR, JUDGE_STATUS_REVIEW
from aeos.core.judge.deterministic_judge import DeterministicJudge
from aeos.core.judge.judge_input_builder import JudgeInputBuilder
from aeos.core.judge.judge_gate_loader import JudgeGateLoader
from aeos.core.judge.judge_scorecard import JudgeScorecardGenerator
from aeos.core.judge.judge_result_validator import JudgeResultValidator
from aeos.core.judge.judge_reporter import JudgeReporter
from aeos.core.evidence.evidence_manifest import StagedManifestBuilder


class JudgeEngine:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.deterministic_judge = DeterministicJudge(workspace_root)
        self.input_builder = JudgeInputBuilder(workspace_root)
        self.gate_loader = JudgeGateLoader(workspace_root)
        self.scorecard_generator = JudgeScorecardGenerator()
        self.result_validator = JudgeResultValidator()
        self.reporter = JudgeReporter(workspace_root)

    def evaluate(self, execution_id: str, target_path: str = ".") -> JudgeResult:
        judge_input = self.input_builder.build(execution_id, target_path)
        return self.evaluate_with_input(judge_input)

    def evaluate_with_input(self, judge_input: JudgeInput) -> JudgeResult:
        self.gate_loader.save_judge_input(judge_input)

        result = self.deterministic_judge.evaluate(judge_input)

        scorecard = self.scorecard_generator.generate(result)
        self.gate_loader.save_judge_result(result)
        self.gate_loader.save_scorecard(scorecard)
        self.reporter.generate_report(result, scorecard)

        self._finalize_judge_manifest(judge_input.execution_id)

        return result

    def _finalize_judge_manifest(self, execution_id: str) -> None:
        """Finalize judge evidence manifest AFTER all judge outputs are written.
        
        Also regenerates the final evidence-manifest.json so it reflects the
        updated judge data. This prevents hash mismatches when judge is re-run
        on an already-finalized execution.
        
        Scans sibling evidence directories for eval and readiness manifests
        so they are included in the regenerated evidence-manifest.json.
        """
        evidence_root = self.workspace_root / ".aeos" / "evidence"
        evidence_dir = evidence_root / execution_id
        extra_dirs: list[str] = []
        if evidence_root.exists():
            for sibling in sorted(evidence_root.iterdir()):
                if sibling.is_dir() and sibling.name != execution_id:
                    if (sibling / "eval-evidence-manifest.json").exists() or \
                       (sibling / "readiness-evidence-manifest.json").exists():
                        extra_dirs.append(str(sibling))

        builder = StagedManifestBuilder(execution_id, str(evidence_dir), str(self.workspace_root))
        builder.finalize_judge_manifest()
        builder.finalize_evidence_manifest(extra_evidence_dirs=extra_dirs if extra_dirs else None)

    def evaluate_from_dict(self, data: dict[str, Any]) -> JudgeResult:
        judge_input = self.input_builder.build_from_dict(data)
        return self.evaluate_with_input(judge_input)

    def get_latest_result(self) -> Optional[JudgeResult]:
        return self.gate_loader.load_latest_judge_result()

    def get_result(self, execution_id: str) -> Optional[JudgeResult]:
        return self.gate_loader.load_judge_result(execution_id)

    def validate_result(self, result: JudgeResult) -> list[str]:
        return self.result_validator.validate(result)

    def is_valid_result(self, result: JudgeResult) -> bool:
        return self.result_validator.is_valid(result)

    def summarize(self, result: JudgeResult) -> dict:
        return self.reporter.generate_summary(result)
