import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from aeos.core.judge.judge_models import JudgeResult, JudgeInput, JUDGE_STATUS_ERROR, JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED


def _make_execution(evidence_dir: Path, eid: str,
                    has_final_manifest: bool = False,
                    has_runtime: bool = False,
                    has_judge_evidence: bool = False,
                    has_reports: bool = False):
    d = evidence_dir / eid
    d.mkdir(parents=True, exist_ok=True)
    (d / "dummy.txt").write_text("x")
    if has_final_manifest:
        (d / "evidence-manifest.json").write_text('{"files": [], "manifest_sha256": "abc"}')
    if has_runtime:
        (d / "runtime-evidence-manifest.json").write_text('{}')
    if has_judge_evidence:
        (d / "judge-result.json").write_text('{"status": "PASS"}')
    if has_reports:
        reports_dir = evidence_dir.parent / "reports" / eid
        reports_dir.mkdir(parents=True, exist_ok=True)
        (reports_dir / "judge-report.md").write_text("# Judge Report")
    return d


@patch("aeos.cli.commands.judge.JudgeEngine.evaluate")
def test_judge_latest_prints_explicit_cause(mock_evaluate, tmp_path: Path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence"
    _make_execution(evidence_dir, "exec-err", has_final_manifest=True)
    mock_evaluate.return_value = JudgeResult(
        execution_id="exec-err",
        status=JUDGE_STATUS_ERROR,
        score=0.7,
        missing_evidence=["evidence-manifest.json"],
        blocking_rules=["missing_evidence_manifest"],
        warnings=["No evidence manifest found"],
        recommendations=["Run a full pipeline first"],
    )

    from aeos.cli.commands.judge import cmd_judge_run
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-err"
    exit_code = cmd_judge_run(args)
    captured = capsys.readouterr()
    assert "Judge result: ERROR" in captured.out
    assert "missing_evidence_manifest" in captured.out
    assert "evidence-manifest.json" in captured.out
    assert exit_code == 2


@patch("aeos.cli.commands.judge.JudgeEngine.evaluate")
def test_judge_returns_missing_evidence_manifest(mock_evaluate, tmp_path: Path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence"
    _make_execution(evidence_dir, "exec-missing")
    mock_evaluate.return_value = JudgeResult(
        execution_id="exec-missing",
        status=JUDGE_STATUS_BLOCKED,
        score=0.5,
        missing_evidence=["evidence-manifest.json"],
        blocking_rules=["missing_evidence_manifest"],
    )

    from aeos.cli.commands.judge import cmd_judge_run
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-missing"
    exit_code = cmd_judge_run(args)
    captured = capsys.readouterr()
    assert "missing_evidence_manifest" in captured.out


@patch("aeos.cli.commands.judge.JudgeEngine.evaluate")
def test_judge_latest_passes_with_complete_execution(mock_evaluate, tmp_path: Path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence"
    _make_execution(evidence_dir, "exec-ok", has_final_manifest=True, has_reports=True)
    mock_evaluate.return_value = JudgeResult(
        execution_id="exec-ok",
        status=JUDGE_STATUS_PASS,
        score=0.95,
    )

    from aeos.cli.commands.judge import cmd_judge_run
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-ok"
    exit_code = cmd_judge_run(args)
    captured = capsys.readouterr()
    assert "Judge result: PASS" in captured.out
    assert exit_code == 0


def test_judge_blocks_when_final_manifest_missing(tmp_path: Path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence" / "exec-no-final"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "judge-result.json").write_text('{}')

    from aeos.cli.commands.judge import cmd_judge_run
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-no-final"
    exit_code = cmd_judge_run(args)
    captured = capsys.readouterr()
    assert "evidence-manifest.json not found" in captured.out
    assert "missing_evidence_manifest" in captured.out
    assert exit_code == 2
