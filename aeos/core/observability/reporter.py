"""AEOS Observability Reporter — generates timeline, cost report, and observability dashboard."""

import json
from pathlib import Path
from datetime import datetime, UTC


class ObservabilityReporter:
    def __init__(self, target_root: str):
        self.target_root = Path(target_root)

    def generate_timeline(self, execution_id: str) -> str:
        base = self.target_root / ".aeos" / "observability" / execution_id
        log_path = base / "execution.log.jsonl"
        if not log_path.exists():
            return f"# Timeline for {execution_id}\n\nNo observability data found."

        events = []
        with log_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))

        timeline = [f"# Timeline — {execution_id}", ""]
        for ev in sorted(events, key=lambda e: e.get("timestamp", "")):
            timeline.append(f"- **{ev.get('timestamp', '?')}** | {ev.get('type', 'event')}: {json.dumps(ev.get('data', {}))}")

        return "\n".join(timeline)

    def generate_cost_report(self, execution_id: str) -> dict:
        base = self.target_root / ".aeos" / "observability" / execution_id
        metrics_path = base / "metrics.json"
        if not metrics_path.exists():
            return {"execution_id": execution_id, "status": "no_data"}
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        return {
            "execution_id": execution_id,
            "token_usage": metrics.get("token_usage", 0),
            "tool_calls": metrics.get("tool_calls", 0),
            "duration_ms": metrics.get("duration_ms", 0),
        }