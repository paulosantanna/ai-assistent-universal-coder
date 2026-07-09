\"\"\"MCP stdio: test runner controlled — detect, run allowlisted.\"\"\"
import sys, json, subprocess
from pathlib import Path

ALLOWLISTED_COMMANDS = {
    "pytest": ["pytest", "-x", "--tb=short"],
    "jest": ["npx", "jest", "--bail"],
}

def main(method, params):
    if method == "test.detect":
        target = Path(params.get("target", "."))
        if (target / "pyproject.toml").exists() or (target / "setup.py").exists():
            return {"framework": "pytest"}
        if (target / "package.json").exists():
            return {"framework": "jest"}
        return {"framework": "unknown"}
    elif method == "test.run_allowlisted":
        framework = params.get("framework", "unknown")
        cmd = ALLOWLISTED_COMMANDS.get(framework)
        if not cmd:
            return {"error": "framework_not_allowlisted"}
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=params.get("cwd"), timeout=300)
            return {"stdout": r.stdout[:10000], "stderr": r.stderr[:1000], "returncode": r.returncode}
        except subprocess.TimeoutExpired:
            return {"error": "timeout"}
        except Exception as e:
            return {"error": str(e)}
    return {"error": "unknown_method"}

if __name__ == "__main__":
    raw = sys.stdin.read()
    try:
        req = json.loads(raw)
        result = main(req.get("method"), req.get("params", {}))
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
