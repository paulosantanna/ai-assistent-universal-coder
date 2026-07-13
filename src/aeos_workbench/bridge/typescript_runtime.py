"""Bridge to the existing AEOS TypeScript Runtime Core (v9.1).

Allows the Workbench to delegate execution to the TypeScript runtime
for operations that are already implemented there (e.g., agent execution,
Ollama integration, quality gates).
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


RUNTIME_DIR = None


def _find_runtime():
    global RUNTIME_DIR
    if RUNTIME_DIR:
        return RUNTIME_DIR

    candidates = [
        Path.cwd() / "runtime",
        Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime",
        Path.cwd() / "AEOS_RUNTIME_MVP_v1",
    ]
    for c in candidates:
        if (c / "package.json").exists() and (c / "dist" / "cli" / "index.js").exists():
            RUNTIME_DIR = c
            return c
    return None


def runtime_available():
    return _find_runtime() is not None


def run_runtime_command(args):
    runtime_dir = _find_runtime()
    if not runtime_dir:
        return {
            "status": "error",
            "error": "AEOS TypeScript Runtime not found. Build it first: cd runtime && npm install && npm run build",
        }

    cmd = ["node", str(runtime_dir / "dist" / "cli" / "index.js")] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(runtime_dir),
            timeout=60000,
        )
        return {
            "status": "ok",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "command": " ".join(cmd),
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "Command timed out after 60s", "command": " ".join(cmd)}
    except FileNotFoundError:
        return {"status": "error", "error": "Node.js not found. Install Node.js 18+.", "command": " ".join(cmd)}
    except Exception as e:
        return {"status": "error", "error": str(e), "command": " ".join(cmd)}


def run_agent(provider, model, prompt):
    return run_runtime_command([
        "agent", "run",
        "--provider", provider,
        "--model", model,
        "--prompt", json.dumps({"text": prompt}),
    ])


def scan_project(path):
    bridge_dir = os.environ.get("AEOS_BRIDGE_DIR")
    if bridge_dir:
        p = Path(bridge_dir) / "aeos-ecosystem.json"
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return {"status": "ok", "source": "bridge-file", "data": json.load(f)}

    return run_runtime_command(["scan", "--path", str(path)])


def run_quality_gates(path):
    return run_runtime_command(["gates", "check", "--path", str(path)])


def generate_ci(provider, path):
    return run_runtime_command(["generate", "ci", "--provider", provider, "--path", str(path)])


def run_doctor():
    return run_runtime_command(["doctor"])


def status():
    return run_runtime_command(["status"])
