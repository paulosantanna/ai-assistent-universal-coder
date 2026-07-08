"""Ecosystem Map Generator - produces ecosystem-map.md."""

from datetime import datetime, timezone


class EcosystemMapGenerator:
    def __init__(self, scan_result, stacks):
        self.scan = scan_result
        self.stacks = stacks

    def generate(self):
        scan = self.scan
        stacks = self.stacks

        lines = []

        # Header
        lines.append("# AEOS Ecosystem Map\n")
        lines.append(f"**Generated:** {scan.get('scan_timestamp', datetime.now(timezone.utc).isoformat())}")
        lines.append(f"**Project:** {scan.get('project_name', 'unknown')}")
        lines.append(f"**Scanner ID:** {scan.get('scan_id', 'unknown')}")
        lines.append(f"**Version:** 1.0.0\n")

        # Project Overview
        lines.append("## Project Overview\n")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Total Files | {scan.get('total_files', 0)} |")
        lines.append(f"| Total Dirs | {scan.get('total_dirs', 0)} |")
        lines.append(f"| Total Lines | {scan.get('total_lines', 0):,} |")
        lines.append(f"| Languages | {len(scan.get('languages', {}))} |")
        lines.append(f"| Stacks Detected | {len(stacks)} |\n")

        # Languages
        lines.append("## Languages\n")
        lines.append("| Language | Files | Lines |")
        lines.append("|----------|-------|-------|")
        for lang, info in sorted(scan.get("languages", {}).items()):
            lines.append(f"| {lang.capitalize()} | {info['files']} | {info['lines']:,} |")
        lines.append("")

        # Stacks
        lines.append("## Detected Stacks\n")
        for stack in stacks:
            confidence_pct = int(stack["confidence"] * 100)
            lines.append(f"### {stack['name']} (Confidence: {confidence_pct}%)")
            lines.append(f"- **ID:** `{stack['id']}`")
            lines.append(f"- **Frameworks:** {', '.join(stack['frameworks'])}")
            lines.append(f"- **Build Tools:** {', '.join(stack['build_tools']) if stack['build_tools'] else 'N/A'}")
            lines.append(f"- **Evidence:**")
            for ev in stack.get("evidence", []):
                lines.append(f"  - {ev}")
            if stack.get("missing"):
                lines.append(f"- **Missing Indicators:**")
                for m in stack["missing"]:
                    lines.append(f"  - {m}")
            lines.append("")

        # File Categories
        lines.append("## File Categories\n")
        lines.append("| Category | Count |")
        lines.append("|----------|-------|")
        for cat, count in sorted(scan.get("file_categories", {}).items()):
            lines.append(f"| {cat} | {count} |")
        lines.append("")

        # Top-Level Structure
        lines.append("## Top-Level Structure\n")
        lines.append("```")
        project_root = scan.get("project_root", ".")
        lines.append(f"{scan.get('project_name', 'project')}/")
        for f in scan.get("files", []):
            parts = f["path"].split("/")
            if len(parts) <= 2:
                prefix = "├── " if f != scan["files"][-1] else "└── "
                lines.append(f"{prefix}{f['path']}")
        lines.append("```\n")

        # Evidence Summary
        lines.append("## Evidence Collected\n")
        lines.append(f"| ID | Type | Claim |")
        lines.append(f"|----|------|-------|")
        for ev in scan.get("evidence", []):
            claim = ev["claim"][:80] + "..." if len(ev["claim"]) > 80 else ev["claim"]
            lines.append(f"| {ev['evidence_id']} | {ev['type']} | {claim} |")
        lines.append("")

        lines.append("---\n")
        lines.append(f"*AEOS Ecosystem Map v1.0.0 — Scan ID: {scan.get('scan_id', 'unknown')}*")

        return "\n".join(lines)
