"""Ecosystem JSON export - produces aeos-ecosystem.json for cross-tool compatibility.

This file enables the TypeScript runtime and other tools
to consume scan results without re-parsing markdown.
"""

import json
from datetime import datetime, timezone


def export_ecosystem_json(scan_result, stacks, output_path):
    eco = {
        "_aeos": {
            "type": "ecosystem-export",
            "version": "1.0.0",
            "generated": datetime.now(timezone.utc).isoformat(),
            "scanner_id": scan_result.get("scan_id", ""),
        },
        "project": {
            "name": scan_result.get("project_name", ""),
            "root": scan_result.get("project_root", ""),
            "total_files": scan_result.get("total_files", 0),
            "total_dirs": scan_result.get("total_dirs", 0),
            "total_lines": scan_result.get("total_lines", 0),
        },
        "languages": {},
        "stacks": [],
        "dependencies": [],
        "architecture": {
            "patterns": [],
            "api_types": [],
        },
        "risks": [],
        "docker": {
            "has_dockerfile": False,
            "has_compose": False,
        },
    }

    for lang, info in scan_result.get("languages", {}).items():
        eco["languages"][lang] = {
            "files": info["files"],
            "lines": info["lines"],
        }

    for stack in stacks:
        s = {
            "id": stack["id"],
            "name": stack["name"],
            "confidence": stack["confidence"],
            "frameworks": stack["frameworks"],
            "build_tools": stack["build_tools"],
        }
        eco["stacks"].append(s)

    for f in scan_result.get("files", []):
        if f.get("type") == "dockerfile":
            eco["docker"]["has_dockerfile"] = True
        if "docker-compose" in f.get("type", ""):
            eco["docker"]["has_compose"] = True

    output_path = output_path / "aeos-ecosystem.json" if output_path else Path.cwd() / "aeos-ecosystem.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(eco, f, indent=2, ensure_ascii=False)

    return eco
