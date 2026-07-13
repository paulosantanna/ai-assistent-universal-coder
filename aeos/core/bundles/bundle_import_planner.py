import os
from pathlib import Path

def generate_import_plan(target_dir: str, bundle_path: str, remote_branch: str, base_commit: str) -> str:
    script = f"""$Target = "{target_dir}"
$Bundle = "{bundle_path}"
$RemoteBranch = "{remote_branch}"

cd $Target

git status
git bundle verify $Bundle
git fetch $Bundle "$RemoteBranch:refs/remotes/aeos-bundle/$RemoteBranch"

git log --oneline --decorate --graph "HEAD..refs/remotes/aeos-bundle/$RemoteBranch"
git diff HEAD "refs/remotes/aeos-bundle/$RemoteBranch" --stat
git diff HEAD "refs/remotes/aeos-bundle/$RemoteBranch"

Write-Host "Please review the diff. To import:"
Write-Host "git merge --no-ff refs/remotes/aeos-bundle/$RemoteBranch"
Write-Host "OR cherry-pick specific commits."
"""
    return script

def generate_rollback_plan(remote_branch: str, base_commit: str) -> str:
    script = f"""# Rollback plan for {remote_branch}
# Run BEFORE merge:
git branch backup/pre-{remote_branch}

# If merged locally but not pushed:
git reset --hard backup/pre-{remote_branch}

# If pushed or cannot reset:
# git revert -m 1 <merge-commit-hash>
"""
    return script
