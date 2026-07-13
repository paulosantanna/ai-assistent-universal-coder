import os
import subprocess
from pathlib import Path
from typing import List, Tuple
from datetime import datetime

def run_git(cmd: List[str], cwd: str) -> str:
    res = subprocess.run(["git"] + cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Git command failed: git {' '.join(cmd)}\n{res.stderr}")
    return res.stdout.strip()

def get_current_branch(target_dir: str) -> str:
    return run_git(["branch", "--show-current"], target_dir)

def check_working_tree_clean(target_dir: str) -> bool:
    stdout = run_git(["status", "--porcelain", "--untracked-files=no"], target_dir)
    return len(stdout) == 0

def get_commits(target_dir: str, base_branch: str, current_branch: str) -> List[str]:
    stdout = run_git(["log", f"{base_branch}..{current_branch}", "--format=%H"], target_dir)
    return stdout.splitlines() if stdout else []

def get_base_commit(target_dir: str, base_branch: str, current_branch: str) -> str:
    return run_git(["merge-base", base_branch, current_branch], target_dir)

def get_head_commit(target_dir: str) -> str:
    return run_git(["rev-parse", "HEAD"], target_dir)

def get_changed_files(target_dir: str, base_commit: str, head_commit: str) -> Tuple[List[str], List[str], List[str]]:
    stdout = run_git(["diff", "--name-status", f"{base_commit}..{head_commit}"], target_dir)
    added, modified, deleted = [], [], []
    for line in stdout.splitlines():
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]
        file_path = parts[1]
        if status.startswith("A"):
            added.append(file_path)
        elif status.startswith("D"):
            deleted.append(file_path)
        else:
            modified.append(file_path)
    return added, modified, deleted

def create_bundle_file(target_dir: str, bundle_out: str, base_branch: str, current_branch: str) -> None:
    # Use branch name directly so git bundle verify shows the branch correctly
    run_git(["bundle", "create", bundle_out, f"{base_branch}..{current_branch}"], target_dir)
