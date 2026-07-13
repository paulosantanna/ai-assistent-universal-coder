import os
import sys
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

def cmd_bundle_create(args) -> int:
    from aeos.core.bundles import (
        check_working_tree_clean, get_commits, get_base_commit,
        get_head_commit, get_changed_files, create_bundle_file, get_current_branch,
        verify_bundle, list_bundle_heads, test_import_in_temp,
        save_manifest, generate_report, generate_patch,
        generate_import_plan, generate_rollback_plan,
        check_forbidden_files, run_secret_scan, BundleManifest
    )
    
    aeos_root = Path(args.aeos_root).resolve() if getattr(args, "aeos_root", None) else Path.cwd().resolve()
    target_dir = Path(args.target).resolve()
    
    if not (target_dir / ".git").exists():
        print("Target is not a git repository.")
        return 1
        
    current_branch = get_current_branch(str(target_dir))
    if current_branch != args.branch:
        print(f"Target is on branch {current_branch}, expected {args.branch}")
        return 1
        
    if not check_working_tree_clean(str(target_dir)):
        print("Working tree is not clean.")
        return 1
        
    if current_branch in ["main", "master"] and not getattr(args, "force_main", False):
        print("Cannot bundle directly from main or master branch.")
        return 1
        
    # Get base commit relative to main/master (assuming main is the base)
    try:
        base_commit = get_base_commit(str(target_dir), "main", current_branch)
    except Exception:
        base_commit = get_base_commit(str(target_dir), "master", current_branch)
        
    head_commit = get_head_commit(str(target_dir))
    commits = get_commits(str(target_dir), base_commit, head_commit)
    
    if not commits:
        print("No commits found in the branch.")
        return 1
        
    added, modified, deleted = get_changed_files(str(target_dir), base_commit, head_commit)
    all_changed = added + modified + deleted
    
    forbidden = check_forbidden_files(all_changed)
    if forbidden:
        print("Forbidden files detected in branch changes:")
        for f in forbidden:
            print(f" - {f}")
        return 1
        
    secret_pass, secret_out = run_secret_scan(str(target_dir), head_commit, base_commit)
    if not secret_pass:
        print(f"Secret scan failed: {secret_out}")
        return 1
        
    bundle_dir = aeos_root / ".aeos" / "bundles" / f"phase-{args.phase}"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    
    bundle_prefix = f"aeos-phase-{args.phase}-{args.name}"
    bundle_path = bundle_dir / f"{bundle_prefix}.bundle"
    
    create_bundle_file(str(target_dir), str(bundle_path), base_commit, current_branch)
    
    if not verify_bundle(str(bundle_path), str(target_dir)):
        print("Bundle verification failed.")
        return 1
        
    heads = list_bundle_heads(str(bundle_path), str(target_dir))
    
    with open(bundle_path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
    
    sha256_path = bundle_dir / f"{bundle_prefix}.bundle.sha256"
    sha256_path.write_text(sha256, encoding="utf-8")
    
    temp_dir = bundle_dir / f"temp-{args.name}"
    if test_import_in_temp(str(target_dir), str(bundle_path), current_branch, base_commit, str(temp_dir)):
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
    else:
        print("Import test in temporary clone failed.")
        return 1
        
    manifest = BundleManifest(
        bundle_id=bundle_prefix,
        phase=args.phase,
        name=args.name,
        execution_id=args.execution_id,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_repository=str(target_dir),
        source_branch=current_branch,
        base_commit=base_commit,
        head_commit=head_commit,
        commit_count=len(commits),
        commits=commits,
        files_added=added,
        files_modified=modified,
        files_deleted=deleted
    )
    manifest.security.secret_scan = "PASS"
    manifest.security.status = "PASS"
    manifest.bundle.filename = bundle_path.name
    manifest.bundle.sha256 = sha256
    manifest.bundle.size_bytes = bundle_path.stat().st_size
    manifest.bundle.verified = True
    manifest.bundle.heads = heads
    
    manifest_path = bundle_dir / f"{bundle_prefix}.manifest.json"
    save_manifest(manifest, str(manifest_path))
    
    patch_path = bundle_dir / f"{bundle_prefix}.patch"
    generate_patch(str(target_dir), base_commit, head_commit, str(patch_path))
    
    report_path = bundle_dir / f"{bundle_prefix}.report.md"
    generate_report(manifest, str(report_path))
    
    import_plan = generate_import_plan(str(target_dir), str(bundle_path), current_branch, base_commit)
    import_path = bundle_dir / f"{bundle_prefix}-import.ps1"
    import_path.write_text(import_plan, encoding="utf-8")
    
    rollback_plan = generate_rollback_plan(current_branch, base_commit)
    rollback_path = bundle_dir / f"{bundle_prefix}-rollback.ps1"
    rollback_path.write_text(rollback_plan, encoding="utf-8")
    
    print(f"Bundle successfully created: {bundle_path}")
    print(f"SHA256: {sha256}")
    print(f"Manifest: {manifest_path}")
    return 0

def cmd_bundle_verify(args) -> int:
    from aeos.core.bundles import verify_bundle, list_bundle_heads
    path = Path(args.path)
    if not path.exists():
        print(f"Bundle not found: {path}")
        return 1
    if verify_bundle(str(path)):
        print("Bundle is valid.")
        heads = list_bundle_heads(str(path))
        print("Heads:", heads)
        return 0
    print("Bundle is invalid.")
    return 1

def cmd_bundle_inspect(args) -> int:
    from aeos.core.bundles import load_manifest
    path = Path(args.manifest)
    if not path.exists():
        print(f"Manifest not found: {path}")
        return 1
    m = load_manifest(str(path))
    print(json.dumps(m.model_dump(), indent=2))
    return 0

def cmd_bundle_import_plan(args) -> int:
    pass

def cmd_bundle_list(args) -> int:
    pass
