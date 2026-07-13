from pathlib import Path
from unittest.mock import MagicMock


def test_cli_performance_benchmark_writes_report(tmp_path: Path):
    from aeos.cli.commands.performance import cmd_performance_benchmark

    args = MagicMock()
    args.target = str(tmp_path)
    args.aeos_root = "."
    args.iterations = 1
    args.profile = "quick"
    args.fail_on = "breach"
    args.json = False

    exit_code = cmd_performance_benchmark(args)

    assert exit_code in (0, 3)
    report_dir = tmp_path / ".aeos" / "reports" / "performance"
    assert any(report_dir.glob("performance-benchmark-*.json"))
    assert any(report_dir.glob("performance-benchmark-*.md"))
