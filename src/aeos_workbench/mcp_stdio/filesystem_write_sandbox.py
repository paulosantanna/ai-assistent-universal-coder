"""MCP stdio: filesystem write sandbox - write to .aeos/sandbox only."""
import sys, json, hashlib
from pathlib import Path

SANDBOX_ROOT = Path(".aeos") / "sandbox"

def main(method, params):
    if method == "filesystem.write_sandbox":
        rel = params.get("path", "")
        content = params.get("content", "")
        dest = SANDBOX_ROOT / rel
        if not str(dest.resolve()).startswith(str(SANDBOX_ROOT.resolve())):
            return {"error": "path_traversal_blocked"}
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        return {"path": str(dest), "size": len(content), "sha256": hashlib.sha256(content.encode()).hexdigest()}
    elif method == "filesystem.mkdir_sandbox":
        path = params.get("path", "")
        dest = SANDBOX_ROOT / path
        if not str(dest.resolve()).startswith(str(SANDBOX_ROOT.resolve())):
            return {"error": "path_traversal_blocked"}
        dest.mkdir(parents=True, exist_ok=True)
        return {"path": str(dest)}
    return {"error": "unknown_method"}

if __name__ == "__main__":
    raw = sys.stdin.read()
    try:
        req = json.loads(raw)
        result = main(req.get("method"), req.get("params", {}))
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
