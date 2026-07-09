import json
from pathlib import Path
from datetime import datetime, UTC

class AgentTraceStore:
    def __init__(self, target_root: str):
        self.target_root = Path(target_root)

    def write_event(self, execution_id: str, event: dict):
        path = self.target_root / ".aeos" / "evidence" / execution_id / "agent-trace.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        event = dict(event)
        event["execution_id"] = execution_id
        event["timestamp"] = datetime.now(UTC).isoformat()
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
        return str(path)
