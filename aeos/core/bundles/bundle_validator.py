import subprocess
import os
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
    import tempfile
    import shutil
    actual_temp = tempfile.mkdtemp(prefix="aeos-bundle-")
    try:
        import os
        env = os.environ.copy()
        env["GIT_LFS_SKIP_SMUDGE"] = "1"
        res = subprocess.run(["git", "-c", "filter.lfs.smudge=", "-c", "filter.lfs.required=false", "clone", "--no-local", target_dir, actual_temp], capture_output=True, text=True, env=env)
        # Even if clone fails on checkout (e.g. LFS issues), if .git exists, we might be able to fetch.
        # But wait, we passed required=false, so it should succeed.
        if res.returncode != 0 and not (os.path.exists(actual_temp) and os.path.isdir(os.path.join(actual_temp, ".git"))):
            return False
            
        res = subprocess.run(["git", "fetch", bundle_path, f"{bundle_head}:refs/remotes/bundle/phase"], cwd=actual_temp, capture_output=True, text=True)
        if res.returncode != 0:
            return False
            
        res = subprocess.run(["git", "log", "--oneline", "--decorate", "--graph", "--all"], cwd=actual_temp, capture_output=True, text=True)
        if res.returncode != 0:
            return False
            
        res = subprocess.run(["git", "diff", f"{base_commit}..refs/remotes/bundle/phase", "--stat"], cwd=actual_temp, capture_output=True, text=True)
        if res.returncode != 0:
            return False
            
        return True
    except Exception:
        return False
    finally:
        def on_rm_error(func, path, exc_info):
            import stat
            os.chmod(path, stat.S_IWRITE)
            func(path)
        shutil.rmtree(actual_temp, onerror=on_rm_error)
