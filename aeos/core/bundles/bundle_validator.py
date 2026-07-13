import subprocess
from typing import List

def verify_bundle(bundle_path: str, target_dir: str = None) -> bool:
    res = subprocess.run(["git", "bundle", "verify", bundle_path], cwd=target_dir, capture_output=True, text=True)
    return res.returncode == 0

def list_bundle_heads(bundle_path: str, target_dir: str = None) -> List[str]:
    res = subprocess.run(["git", "bundle", "list-heads", bundle_path], cwd=target_dir, capture_output=True, text=True)
    if res.returncode != 0:
        return []
    return res.stdout.strip().splitlines()

def test_import_in_temp(target_dir: str, bundle_path: str, bundle_head: str, base_commit: str, temp_dir: str) -> bool:
    try:
        res = subprocess.run(["git", "clone", "--no-local", target_dir, temp_dir], capture_output=True, text=True)
        if res.returncode != 0:
            return False
            
        res = subprocess.run(["git", "fetch", bundle_path, f"{bundle_head}:refs/remotes/bundle/phase"], cwd=temp_dir, capture_output=True, text=True)
        if res.returncode != 0:
            return False
            
        res = subprocess.run(["git", "log", "--oneline", "--decorate", "--graph", "--all"], cwd=temp_dir, capture_output=True, text=True)
        if res.returncode != 0:
            return False
            
        res = subprocess.run(["git", "diff", f"{base_commit}..refs/remotes/bundle/phase", "--stat"], cwd=temp_dir, capture_output=True, text=True)
        if res.returncode != 0:
            return False
            
        return True
    except Exception:
        return False
