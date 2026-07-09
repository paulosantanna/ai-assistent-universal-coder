from pathlib import Path
from unittest.mock import MagicMock, patch


def _make_execution(evidence_dir: Path, eid: str, has_final_manifest: bool = False,
                    has_reports: bool = False):
    d = evidence_dir / eid
    d.mkdir(parents=True, exist_ok=True)
    (d / "dummy.txt").write_text("x")
    if has_final_manifest:
        (d / "evidence-manifest.json").write_text('{"files": [], "manifest_sha256": "abc"}')
    if has_reports:
        reports_dir = evidence_dir.parent / "reports" / eid
        reports_dir.mkdir(parents=True, exist_ok=True)
        (reports_dir / "judge-report.md").write_text("# Report")
    return d


@patch("aeos.cli.commands.judge.JudgeEngine")
def test_judge_latest_shows_explicit_cause(mock_engine_cls, tmp_path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence"
    _make_execution(evidence_dir, "exec-test", has_final_manifest=True)
    mock_engine = mock_engine_cls.return_value
    from aeos.core.judge.judge_models import JudgeResult, JUDGE_STATUS_ERROR
    mock_engine.evaluate.return_value = JudgeResult(
        execution_id="exec-test",
        status=JUDGE_STATUS_ERROR,
        score=0.7,
        missing_evidence=["evidence-manifest.json"],
        blocking_rules=["missing_evidence_manifest"],
        warnings=["No final manifest found"],
        recommendations=["Run full pipeline first"],
    )

    from aeos.cli.commands.judge import cmd_judge_run
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-test"
    exit_code = cmd_judge_run(args)
    captured = capsys.readouterr()
    assert "Judge result: ERROR" in captured.out
    assert "missing_evidence_manifest" in captured.out
    assert exit_code == 2


@patch("aeos.cli.commands.judge.JudgeEngine")
def test_judge_latest_shows_report_path(mock_engine_cls, tmp_path, capsys):
    evidence_dir = tmp_path / ".aeos" / "evidence"
    _make_execution(evidence_dir, "exec-ok", has_final_manifest=True, has_reports=True)
    mock_engine = mock_engine_cls.return_value
    from aeos.core.judge.judge_models import JudgeResult, JUDGE_STATUS_PASS
    mock_engine.evaluate.return_value = JudgeResult(
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
    assert "Report:" in captured.out
    assert exit_code == 0
