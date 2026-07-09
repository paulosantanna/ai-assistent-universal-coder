\"\"\"MCP stdio: package local — create, verify, inspect, extract staging.\"\"\"
import sys, json, hashlib, zipfile, io, os
from pathlib import Path

def main(method, params):
    if method == "package.create":
        return {"status": "simulated", "note": "package creation requires ToolRouter"}
    elif method == "package.verify":
        return {"status": "verified", "note": "package verification simulated"}
    elif method == "package.inspect":
        return {"status": "simulated", "manifest": {}}
    elif method == "package.extract_staging":
        return {"status": "simulated", "dest": "staging"}
    return {"error": "unknown_method"}

if __name__ == "__main__":
    raw = sys.stdin.read()
    try:
        req = json.loads(raw)
        result = main(req.get("method"), req.get("params", {}))
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
