from pathlib import Path

from aeos.core.performance.benchmark_runner import PerformanceBenchmarkRunner


def test_benchmark_runner_produces_cases_and_reports(tmp_path: Path):
    runner = PerformanceBenchmarkRunner(workspace_root=tmp_path, aeos_root=".")
    result = runner.run(iterations=1, profile="quick")
    reports = runner.write_reports(result, tmp_path / "reports")

    assert result["status"] in {"PASS", "WARN", "BREACHED"}
    assert {case["name"] for case in result["cases"]} == {
        "registry_load",
        "skill_contract_load",
        "scanner_pruned",
        "evidence_batch_write",
    }
    assert Path(reports["json"]).exists()
    assert Path(reports["markdown"]).exists()


def test_benchmark_runner_rejects_invalid_iterations(tmp_path: Path):
    runner = PerformanceBenchmarkRunner(workspace_root=tmp_path, aeos_root=".")

    try:
        runner.run(iterations=0)
    except ValueError as exc:
        assert "iterations" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_benchmark_runner_rejects_unknown_profile(tmp_path: Path):
    runner = PerformanceBenchmarkRunner(workspace_root=tmp_path, aeos_root=".")

    try:
        runner.run(iterations=1, profile="deep")
    except ValueError as exc:
        assert "Unsupported benchmark profile" in str(exc)
    else:
        raise AssertionError("expected ValueError")
