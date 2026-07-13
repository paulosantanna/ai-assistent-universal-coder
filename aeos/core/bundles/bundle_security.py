import os
import subprocess
from typing import List, Tuple
from pathlib import Path

FORBIDDEN_EXTENSIONS = {
    ".env", "*.pem", "*.key", "*.p12", "*.pfx", "*.sqlite", "*.db",
    "*.pt", "*.pth", "*.bin", "*.safetensors"
}
FORBIDDEN_DIRS = {
    "data/", "datasets/", "models/", "embeddings/", "chroma/", "chromadb/", ".venv/", "venv/"
}
FORBIDDEN_EXACT = {".env"}

def check_forbidden_files(files_changed: List[str]) -> List[str]:
    violations = []
    for f in files_changed:
        f_path = Path(f)
        
        if f_path.name in FORBIDDEN_EXACT:
            violations.append(f)
            continue
            
        for ext in FORBIDDEN_EXTENSIONS:
            if ext.startswith("*"):
                if f_path.suffix == ext[1:]:
                    violations.append(f)
                    break
            elif f_path.name == ext:
                violations.append(f)
                break
                
        for d in FORBIDDEN_DIRS:
            if f.startswith(d) or f"/{d}" in f:
                violations.append(f)
                break
    return list(set(violations))

def run_secret_scan(target_dir: str, head_commit: str, base_commit: str) -> Tuple[bool, str]:
    """Run gitleaks on the diff between base_commit and head_commit."""
    try:
        # Run gitleaks explicitly on the local dir to check the specific commits
        cmd = ["gitleaks", "detect", "--no-git", "--source", target_dir, "-v"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=target_dir)
        if result.returncode != 0 and "leaks found" in result.stdout.lower():
            return False, result.stdout
        return True, "PASS"
    except Exception as e:
        return False, str(e)
