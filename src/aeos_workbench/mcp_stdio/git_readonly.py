"""MCP stdio: git readonly - status, diff, log, branch_current."""
import sys, json, subprocess

def _run(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=30)
        return {"stdout": r.stdout[:5000], "stderr": r.stderr[:500], "returncode": r.returncode}
    except Exception as e:
        return {"error": str(e)}

def main(method, params):
    cwd = params.get("cwd", None)
    if method == "git.status":
        return _run(["git", "status", "--short"], cwd)
    elif method == "git.diff":
        return _run(["git", "diff", "--stat"], cwd)
    elif method == "git.log":
        n = params.get("n", 10)
        return _run(["git", "log", f"-{n}", "--oneline"], cwd)
    elif method == "git.branch_current":
        return _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd)
    return {"error": "unknown_method"}

if __name__ == "__main__":
    raw = sys.stdin.read()
    try:
        req = json.loads(raw)
        result = main(req.get("method"), req.get("params", {}))
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
