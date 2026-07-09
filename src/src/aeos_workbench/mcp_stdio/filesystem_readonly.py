\"\"\"MCP stdio server: filesystem readonly — list, read, exists, stat.\"\"\"
import sys, json, os, hashlib
from pathlib import Path

def handle(method, params):
    if method == "filesystem.read":
        p = Path(params.get("path", ""))
        if not p.exists() or not p.is_file():
            return {"error": "not_found"}
        content = p.read_bytes()
        return {"path": str(p), "size": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    elif method == "filesystem.list":
        p = Path(params.get("path", "."))
        if not p.exists() or not p.is_dir():
            return {"error": "not_found"}
        entries = []
        for child in p.iterdir():
            entries.append({"name": child.name, "is_dir": child.is_dir(), "size": child.stat().st_size if child.is_file() else 0})
        return {"path": str(p), "entries": entries}
    elif method == "filesystem.exists":
        return {"exists": Path(params.get("path", "")).exists()}
    elif method == "filesystem.stat":
        p = Path(params.get("path", ""))
        if not p.exists():
            return {"error": "not_found"}
        s = p.stat()
        return {"path": str(p), "size": s.st_size, "modified": s.st_mtime}
    return {"error": "unknown_method"}

if __name__ == "__main__":
    raw = sys.stdin.read()
    try:
        req = json.loads(raw)
        result = main(req.get("method"), req.get("params", {}))
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
