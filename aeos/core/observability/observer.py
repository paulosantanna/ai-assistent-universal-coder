import json
from pathlib import Path
from dataclasses import asdict
from datetime import datetime, UTC

class AEOSObserver:
    def __init__(self, target_root: str, execution_id: str):
        self.base = Path(target_root) / ".aeos" / "observability" / execution_id
        self.base.mkdir(parents=True, exist_ok=True)
        self.execution_id = execution_id

    def log_event(self, event: dict):
        event = dict(event)
        event["execution_id"] = self.execution_id
        event["timestamp"] = datetime.now(UTC).isoformat()
        with (self.base / "execution.log.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def write_metric(self, metrics: dict):
        (self.base / "metrics.json").write_text(
            json.dumps(metrics, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def write_trace_span(self, span):
        with (self.base / "trace.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(span), ensure_ascii=False) + "\n")
