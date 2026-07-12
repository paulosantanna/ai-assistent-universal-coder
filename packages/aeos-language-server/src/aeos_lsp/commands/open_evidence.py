from __future__ import annotations

import glob
import logging
import os
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def open_evidence(server: Any, args: dict[str, Any]) -> dict[str, Any]:
    artifact_id = args.get("artifact_id", "")
    if not artifact_id:
        return {"error": "Missing 'artifact_id' argument"}

    logger.info("Opening evidence for artifact: %s", artifact_id)

    try:
        workspace = getattr(server, "workspace_manager", None)
        aeos_root = None
        if workspace is not None:
            aeos_root = getattr(workspace, "aeos_root", None)
            if aeos_root is None and hasattr(workspace, "workspace_folders"):
                for folder in workspace.workspace_folders:
                    candidate = Path(folder.path) / ".aeos"
                    if candidate.is_dir():
                        aeos_root = candidate
                        break

        evidence_dir = None
        if aeos_root is not None:
            evidence_dir = Path(aeos_root) / "evidence"
        else:
            cwd = Path.cwd()
            candidates = list(cwd.rglob(".aeos/evidence"))
            if not candidates:
                candidates = list(cwd.glob("**/.aeos/evidence"))
            if candidates:
                evidence_dir = candidates[0]

        if evidence_dir is None or not evidence_dir.is_dir():
            return {
                "artifact_id": artifact_id,
                "found": False,
                "message": "No evidence directory found. Run an AEOS execution first.",
            }

        matching_files: list[dict[str, Any]] = []
        for pattern in ("*.jsonl", "*.json", "*.log", "*.yaml", "*.md"):
            for f in evidence_dir.rglob(pattern):
                if artifact_id in f.stem or artifact_id in f.name:
                    try:
                        stat = f.stat()
                        matching_files.append({
                            "path": str(f.absolute()),
                            "name": f.name,
                            "size_bytes": stat.st_size,
                            "modified": stat.st_mtime,
                        })
                    except OSError:
                        pass

        if not matching_files:
            execution_dirs = [d for d in evidence_dir.iterdir() if d.is_dir()] if evidence_dir.is_dir() else []
            for exec_dir in execution_dirs:
                for f in exec_dir.rglob("*"):
                    if f.is_file() and artifact_id in f.stem:
                        try:
                            stat = f.stat()
                            matching_files.append({
                                "path": str(f.absolute()),
                                "name": f.name,
                                "size_bytes": stat.st_size,
                                "modified": stat.st_mtime,
                            })
                        except OSError:
                            pass

        if not matching_files:
            semantic_model = getattr(server, "semantic_model", None)
            symbol = None
            if semantic_model is not None:
                symbol = semantic_model.get_symbol_by_id(artifact_id)
            if symbol is not None:
                matching_files.append({
                    "path": getattr(symbol, "source_uri", ""),
                    "name": getattr(symbol, "name", artifact_id),
                    "size_bytes": 0,
                    "modified": 0,
                    "note": "Symbol source file (no evidence logs found)",
                })

        return {
            "artifact_id": artifact_id,
            "found": len(matching_files) > 0,
            "evidence_count": len(matching_files),
            "evidence_dir": str(evidence_dir) if evidence_dir else None,
            "files": matching_files,
        }
    except Exception as exc:
        logger.exception("Failed to open evidence for %s", artifact_id)
        return {"error": str(exc), "artifact_id": artifact_id}
