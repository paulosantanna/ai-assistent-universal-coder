#!/usr/bin/env python3
"""Generate an AEOS observability package for a target project."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = REPO_ROOT / "aeos" / "templates" / "observability"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def grafana_dashboard(service_name: str, datasource: str) -> dict:
    return {
        "title": f"{service_name} Observability",
        "uid": f"{service_name.lower().replace('_', '-').replace(' ', '-')}-observability",
        "schemaVersion": 39,
        "version": 1,
        "tags": ["aeos", "opentelemetry", "observability"],
        "templating": {"list": [{"name": "service", "type": "constant", "query": service_name}]},
        "panels": [
            {"title": "Request Rate", "type": "timeseries", "targets": [{"datasource": datasource, "expr": "sum(rate(http_server_request_duration_seconds_count{service_name=\"$service\"}[5m]))"}]},
            {"title": "Error Rate", "type": "timeseries", "targets": [{"datasource": datasource, "expr": "sum(rate(http_server_request_duration_seconds_count{service_name=\"$service\", http_response_status_code=~\"5..\"}[5m]))"}]},
            {"title": "Latency p95", "type": "timeseries", "targets": [{"datasource": datasource, "expr": "histogram_quantile(0.95, sum(rate(http_server_request_duration_seconds_bucket{service_name=\"$service\"}[5m])) by (le))"}]},
            {"title": "Trace Spans", "type": "timeseries", "targets": [{"datasource": datasource, "expr": "sum(rate(traces_spanmetrics_calls_total{service_name=\"$service\"}[5m]))"}]},
            {"title": "Log Events", "type": "timeseries", "targets": [{"datasource": datasource, "expr": "sum(rate(logs_total{service_name=\"$service\"}[5m]))"}]},
        ],
    }


def dynatrace_dashboard(service_name: str) -> dict:
    return {
        "dashboardMetadata": {"name": f"{service_name} AEOS Observability", "owner": "AEOS"},
        "tiles": [
            {"name": "Service health", "tileType": "DATA_EXPLORER", "query": f'builtin:service.errors.server.successCount:filter(eq("dt.entity.service","{service_name}"))'},
            {"name": "Latency", "tileType": "DATA_EXPLORER", "query": f'builtin:service.response.time:filter(eq("dt.entity.service","{service_name}"))'},
            {"name": "Throughput", "tileType": "DATA_EXPLORER", "query": f'builtin:service.requestCount.total:filter(eq("dt.entity.service","{service_name}"))'},
        ],
    }


def collector_config(service_name: str, exporter: str) -> str:
    exporters = {
        "grafana": "    otlphttp:\n      endpoint: ${OTEL_EXPORTER_OTLP_ENDPOINT}\n",
        "dynatrace": "    otlphttp/dynatrace:\n      endpoint: ${DT_OTLP_ENDPOINT}\n      headers:\n        Authorization: \"Api-Token ${DT_API_TOKEN}\"\n",
        "stdout": "    debug:\n      verbosity: basic\n",
    }
    selected = exporters.get(exporter, exporters["stdout"])
    exporter_name = "otlphttp/dynatrace" if exporter == "dynatrace" else ("otlphttp" if exporter == "grafana" else "debug")
    return (
        "receivers:\n"
        "  otlp:\n"
        "    protocols:\n"
        "      grpc:\n"
        "      http:\n\n"
        "processors:\n"
        "  resource:\n"
        "    attributes:\n"
        f"      - key: service.name\n        value: {service_name}\n        action: upsert\n"
        "  batch:\n\n"
        "exporters:\n"
        f"{selected}\n"
        "service:\n"
        "  pipelines:\n"
        f"    traces:\n      receivers: [otlp]\n      processors: [resource, batch]\n      exporters: [{exporter_name}]\n"
        f"    metrics:\n      receivers: [otlp]\n      processors: [resource, batch]\n      exporters: [{exporter_name}]\n"
        f"    logs:\n      receivers: [otlp]\n      processors: [resource, batch]\n      exporters: [{exporter_name}]\n"
    )


def instrumentation_readme(service_name: str, languages: list[str], backend: str) -> str:
    language_list = ", ".join(languages)
    return (
        f"# {service_name} Observability Package\n\n"
        f"Backend target: `{backend}`\n\n"
        f"Languages in scope: `{language_list}`\n\n"
        "## Generated Artifacts\n\n"
        "- `otel-collector.yaml`\n"
        "- `grafana-dashboard.json`\n"
        "- `dynatrace-dashboard.json`\n"
        "- `instrumentation-checklist.md`\n\n"
        "## Required Signals\n\n"
        "- traces for inbound requests and critical internal calls;\n"
        "- metrics for rate, errors, duration, saturation and business KPIs;\n"
        "- structured logs with trace and span correlation;\n"
        "- redaction of secrets, tokens and personal sensitive values;\n"
        "- health and readiness endpoints where the stack supports them.\n\n"
        "## Validation\n\n"
        "1. Start the application with OTLP exporter settings.\n"
        "2. Send smoke traffic.\n"
        "3. Verify traces, metrics and logs arrive in the selected backend.\n"
        "4. Import the generated dashboard JSON into Grafana or Dynatrace.\n"
        "5. Confirm every panel has data or a documented reason for no data.\n"
    )


def generate(target: Path, service_name: str, languages: list[str], backend: str) -> list[Path]:
    target.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    collector = target / "otel-collector.yaml"
    collector.write_text(collector_config(service_name, backend), encoding="utf-8")
    written.append(collector)

    grafana = target / "grafana-dashboard.json"
    write_json(grafana, grafana_dashboard(service_name, "Prometheus"))
    written.append(grafana)

    dynatrace = target / "dynatrace-dashboard.json"
    write_json(dynatrace, dynatrace_dashboard(service_name))
    written.append(dynatrace)

    checklist = target / "instrumentation-checklist.md"
    checklist.write_text(instrumentation_readme(service_name, languages, backend), encoding="utf-8")
    written.append(checklist)

    if TEMPLATE_ROOT.exists():
        for template in TEMPLATE_ROOT.glob("*"):
            if template.is_file():
                destination = target / "references" / template.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(template, destination)
                written.append(destination)
    return written


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AEOS observability artifacts.")
    parser.add_argument("--target", required=True, help="Output directory.")
    parser.add_argument("--service-name", required=True)
    parser.add_argument("--language", action="append", default=[], help="Language in scope. Can be passed more than once.")
    parser.add_argument("--backend", choices=("grafana", "dynatrace", "stdout"), default="grafana")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    languages = args.language or ["generic"]
    written = generate(Path(args.target).resolve(), args.service_name, languages, args.backend)
    for path in written:
        print(f"WROTE {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
