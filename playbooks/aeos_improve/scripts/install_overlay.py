#!/usr/bin/env python3
from __future__ import annotations
import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PACK_ID = "aidiabetic-urgent-improvement-v1"

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--aeos-root", required=True)
    p.add_argument("--target-root", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--uninstall", action="store_true")
    return p.parse_args()

def main() -> int:
    args = parse_args()
    pack_root = Path(__file__).resolve().parents[1]
    aeos_root = Path(args.aeos_root).resolve()
    target_root = Path(args.target_root).resolve()

    if not aeos_root.is_dir():
        print(f"ERROR: AEOS root not found: {aeos_root}", file=sys.stderr)
        return 2
    if not target_root.is_dir():
        print(f"ERROR: target root not found: {target_root}", file=sys.stderr)
        return 2
    if aeos_root == target_root:
        print("ERROR: AEOS root and target root must be separate", file=sys.stderr)
        return 2

    install_dir = aeos_root / "aeos" / "additions" / PACK_ID
    index_file = aeos_root / "aeos" / "overlays" / f"{PACK_ID}.index.yaml"
    target_marker = target_root / ".aeos" / "aidiabetic-improvement-pack.yaml"

    if args.uninstall:
        for path in [install_dir, index_file, target_marker]:
            print(f"REMOVE {path}")
            if not args.dry_run and path.exists():
                shutil.rmtree(path) if path.is_dir() else path.unlink()
        return 0

    for op, src, dst in [
        ("COPY", pack_root, install_dir),
        ("WRITE", None, index_file),
        ("WRITE", None, target_marker),
    ]:
        print(f"{op} {src or ''} -> {dst}")

    if args.dry_run:
        return 0

    backup_root = aeos_root / ".aeos-runtime" / "pack-backups" / (
        PACK_ID + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    )
    same_location = pack_root.resolve() == install_dir.resolve()
    if not same_location:
        if install_dir.exists():
            backup_root.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(install_dir, backup_root)
            shutil.rmtree(install_dir)
        install_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(pack_root, install_dir)
    else:
        print("PACK_ALREADY_IN_OVERLAY_LOCATION")

    index_file.parent.mkdir(parents=True, exist_ok=True)
    index_file.write_text(
        "overlay:\n"
        f"  id: {PACK_ID}\n"
        "  version: 1.0.0\n"
        f"  root: aeos/additions/{PACK_ID}\n"
        "  registries:\n"
        f"    skills: aeos/additions/{PACK_ID}/registries/skills.registry.overlay.yaml\n"
        f"    agents: aeos/additions/{PACK_ID}/registries/agents.registry.overlay.yaml\n"
        f"    playbooks: aeos/additions/{PACK_ID}/registries/enterprise-playbooks.registry.overlay.yaml\n"
        "  enabled: true\n",
        encoding="utf-8",
        newline="\n",
    )

    target_marker.parent.mkdir(parents=True, exist_ok=True)
    target_marker.write_text(
        "improvement_pack:\n"
        f"  id: {PACK_ID}\n"
        f"  installed_from: {str(pack_root).replace(chr(92), '/')}\n"
        f"  aeos_overlay: {str(index_file).replace(chr(92), '/')}\n"
        "  mode: controlled\n"
        "  auto_merge: false\n"
        "  auto_deploy: false\n",
        encoding="utf-8",
        newline="\n",
    )
    print("INSTALLED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
