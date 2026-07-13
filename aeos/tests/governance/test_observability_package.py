from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "observability_package.py"
spec = importlib.util.spec_from_file_location("observability_package", MODULE_PATH)
observability_package = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["observability_package"] = observability_package
spec.loader.exec_module(observability_package)


def test_observability_package_generates_dashboards_and_collector(tmp_path: Path):
    written = observability_package.generate(tmp_path, "orders-api", ["java", "python"], "grafana")

    assert tmp_path / "otel-collector.yaml" in written
    assert tmp_path / "grafana-dashboard.json" in written
    assert tmp_path / "dynatrace-dashboard.json" in written
    assert tmp_path / "instrumentation-checklist.md" in written

    dashboard = json.loads((tmp_path / "grafana-dashboard.json").read_text(encoding="utf-8"))
    assert dashboard["title"] == "orders-api Observability"
    assert {panel["title"] for panel in dashboard["panels"]} >= {"Request Rate", "Error Rate", "Latency p95"}

    collector = (tmp_path / "otel-collector.yaml").read_text(encoding="utf-8")
    assert "service.name" in collector
    assert "orders-api" in collector
    assert "otlp" in collector


def test_observability_package_dynatrace_uses_token_placeholder(tmp_path: Path):
    observability_package.generate(tmp_path, "billing", ["dotnet"], "dynatrace")

    collector = (tmp_path / "otel-collector.yaml").read_text(encoding="utf-8")
    assert "${DT_API_TOKEN}" in collector
    assert "Api-Token" in collector
