from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


class AgentTraceStore:
    def __init__(self, target_root: str):
        self.target_root = Path(target_root)

    def write_event(self, execution_id: str, event: dict[str, Any]) -> str:
        path = self.target_root / ".aeos" / "evidence" / execution_id / "agent-trace.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        event = dict(event)
        event["execution_id"] = execution_id
        event["timestamp"] = datetime.now(timezone.utc).isoformat()
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        return str(path)

    def read_events(self, execution_id: str) -> list[dict[str, Any]]:
        path = self.target_root / ".aeos" / "evidence" / execution_id / "agent-trace.jsonl"
        if not path.exists():
            return []
        events = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events
