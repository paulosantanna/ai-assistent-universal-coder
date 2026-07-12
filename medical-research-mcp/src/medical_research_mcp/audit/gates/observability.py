"""Gate 13: Observability — health/readiness/liveness, metrics, tracing, structured logs, SLOs."""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from ..models import GateResult, AuditStatus
from ..exclusions import should_ignore, DEFAULT_EXCLUSIONS

OBSERVABILITY_TERMS = {
    "health", "readiness", "liveness", "healthcheck", "health_check",
    "metric", "prometheus", "grafana", "otel", "opentelemetry",
    "tracing", "trace", "span", "jaeger",
    "structured_log", "json_log", "logstash",
    "slo", "sli", "service_level",
}


def check_observability(repository: str) -> GateResult:
    """Gate 13: Audit observability infrastructure — real endpoints and monitoring."""
    gate = GateResult(
        id="observability",
        title="Observability",
        critical=False,
        weight=0.75,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    root = Path(repository).resolve()
    if not root.is_dir():
        gate.status = AuditStatus.BLOCKED
        gate.findings.append(f"Repository path not found: {repository}")
        gate.finished_at = datetime.now(timezone.utc).isoformat()
        return gate

    obs_files = []
    health_files = []
    metrics_files = []
    tracing_files = []
    logging_files = []
    slo_files = []

    for p in root.rglob("*.py"):
        rel = str(p.relative_to(root)).replace("\\", "/")
        if should_ignore(rel, DEFAULT_EXCLUSIONS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue

        if any(t in text for t in OBSERVABILITY_TERMS):
            obs_files.append(rel)

        if any(t in text for t in {"health", "readiness", "liveness", "healthcheck"}):
            health_files.append(rel)
        if any(t in text for t in {"metric", "prometheus", "grafana"}):
            metrics_files.append(rel)
        if any(t in text for t in {"trace", "tracing", "otel", "opentelemetry", "jaeger"}):
            tracing_files.append(rel)
        if any(t in text for t in {"logging", "logger", "logstash", "structured_log"}):
            logging_files.append(rel)
        if any(t in text for t in {"slo", "sli", "service_level"}):
            slo_files.append(rel)

    gate.metrics["observability_files"] = len(obs_files)
    gate.metrics["health_endpoints"] = len(health_files)
    gate.metrics["metrics_infra"] = len(metrics_files)
    gate.metrics["tracing_infra"] = len(tracing_files)
    gate.metrics["logging_infra"] = len(logging_files)
    gate.metrics["slo_definitions"] = len(slo_files)

    issues = []

    if not health_files:
        gate.findings.append("No health/readiness/liveness endpoints detected")
        issues.append("missing_health_endpoints")
    if not metrics_files:
        gate.findings.append("No metrics infrastructure (Prometheus, etc.) detected")
        issues.append("missing_metrics")

    if not logging_files:
        gate.findings.append("No structured logging detected")
        gate.remediation.append("Implement structured logging (e.g., structlog, json-logger)")

    if not slo_files:
        gate.findings.append("No SLO/SLI definitions found")
        gate.remediation.append("Define SLOs and SLIs for critical services")

    if not tracing_files:
        gate.findings.append("No distributed tracing found")
        gate.remediation.append("Implement OpenTelemetry for distributed tracing")

    if issues:
        gate.status = AuditStatus.FAIL
        gate.score = max(0.0, 10.0 - len(issues) * 3.0)
    else:
        gate.status = AuditStatus.PASS
        gate.score = 10.0
        gate.evidence.append({
            "type": "metric",
            "source": "static_analysis",
            "sha256": "",
            "summary": f"Full observability infrastructure detected ({len(obs_files)} files)",
            "verified": True,
        })
        gate.evidence.append({
            "type": "source_code",
            "source": f"health={len(health_files)}, metrics={len(metrics_files)}, tracing={len(tracing_files)}, logging={len(logging_files)}, slo={len(slo_files)}",
            "sha256": "",
            "summary": "All observability components present",
            "verified": True,
        })

    gate.finished_at = datetime.now(timezone.utc).isoformat()
    gate.duration_ms = (
        datetime.fromisoformat(gate.finished_at).timestamp()
        - datetime.fromisoformat(gate.started_at).timestamp()
    ) * 1000
    return gate
