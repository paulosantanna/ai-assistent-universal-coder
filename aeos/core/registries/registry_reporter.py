from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from aeos.core.registries.registry_models import (
    ConflictRecord,
    ConsolidatedRegistry,
    CrossDependencyResult,
    FragmentMetadata,
    LoadedFragment,
    MergeManifest,
    OrphanRecord,
    SchemaValidationResult,
    ValidationSeverity,
)


class RegistryReporter:
    def __init__(
        self,
        derived_dir: str = ".aeos/derived/registries",
        reports_dir: str = ".aeos/reports",
        evidence_dir: str = ".aeos/evidence/registry-loader",
    ):
        self.derived_dir = Path(derived_dir)
        self.reports_dir = Path(reports_dir)
        self.evidence_dir = Path(evidence_dir)

        self.derived_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def write_consolidated_registries(self, registry: ConsolidatedRegistry) -> list[str]:
        output_files = []

        agents_data = {"agents": [v.to_dict() for v in registry.agents.values()]}
        ap = self.derived_dir / "agents.consolidated.yaml"
        with open(ap, "w", encoding="utf-8") as f:
            yaml.safe_dump(agents_data, f, default_flow_style=False, sort_keys=False)
        output_files.append(str(ap))

        skills_data = {"skills": [v.to_dict() for v in registry.skills.values()]}
        sp = self.derived_dir / "skills.consolidated.yaml"
        with open(sp, "w", encoding="utf-8") as f:
            yaml.safe_dump(skills_data, f, default_flow_style=False, sort_keys=False)
        output_files.append(str(sp))

        playbooks_data = {"playbooks": [v.to_dict() for v in registry.playbooks.values()]}
        pp = self.derived_dir / "playbooks.consolidated.yaml"
        with open(pp, "w", encoding="utf-8") as f:
            yaml.safe_dump(playbooks_data, f, default_flow_style=False, sort_keys=False)
        output_files.append(str(pp))

        mcps_data = {"mcps": [v.to_dict() for v in registry.mcps.values()]}
        mp = self.derived_dir / "mcps.consolidated.yaml"
        with open(mp, "w", encoding="utf-8") as f:
            yaml.safe_dump(mcps_data, f, default_flow_style=False, sort_keys=False)
        output_files.append(str(mp))

        lcps_data = {"lcps": [v.to_dict() for v in registry.lcps.values()]}
        lp = self.derived_dir / "lcps.consolidated.yaml"
        with open(lp, "w", encoding="utf-8") as f:
            yaml.safe_dump(lcps_data, f, default_flow_style=False, sort_keys=False)
        output_files.append(str(lp))

        return output_files

    def write_merge_manifest(self, manifest: MergeManifest) -> str:
        data = {
            "generated_at": manifest.generated_at,
            "fragments_loaded": manifest.fragments_loaded,
            "fragments_failed": manifest.fragments_failed,
            "total_entries_by_type": manifest.total_entries_by_type,
            "deduplications": manifest.deduplications,
            "conflicts_resolved": manifest.conflicts_resolved,
            "source_fragments": manifest.source_fragments,
        }
        fp = self.derived_dir / "registry-merge-manifest.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return str(fp)

    def write_loaded_fragments(self, fragments: list[LoadedFragment]) -> str:
        data = []
        for frag in fragments:
            data.append({
                "path": frag.metadata.path,
                "registry_type": frag.metadata.registry_type.value,
                "category": frag.metadata.category.value,
                "version_label": frag.metadata.version_label,
                "loaded": frag.metadata.loaded,
                "parse_error": frag.metadata.parse_error,
                "entry_count": frag.metadata.entry_count,
            })
        fp = self.evidence_dir / "loaded-fragments.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return str(fp)

    def write_conflicts(self, conflicts: list[ConflictRecord]) -> str:
        data = []
        for c in conflicts:
            data.append({
                "entry_id": c.entry_id,
                "registry_type": c.registry_type.value,
                "source_a_path": c.source_a_path,
                "source_b_path": c.source_b_path,
                "existing_path": c.existing_path,
                "conflicting_path": c.conflicting_path,
                "description": c.description,
            })
        fp = self.evidence_dir / "conflicts.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return str(fp)

    def write_orphans(self, orphans: list[OrphanRecord]) -> str:
        data = []
        for o in orphans:
            data.append({
                "orphan_id": o.orphan_id,
                "orphan_type": o.orphan_type,
                "referenced_by": o.referenced_by,
                "reference_field": o.reference_field,
                "severity": o.severity.value,
                "description": o.description,
            })
        fp = self.evidence_dir / "orphans.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return str(fp)

    def write_cross_dependency_validation(self, result: CrossDependencyResult) -> str:
        data = {
            "agent_skills": self._findings_to_dict(result.agent_skills),
            "playbook_agents": self._findings_to_dict(result.playbook_agents),
            "playbook_skills": self._findings_to_dict(result.playbook_skills),
            "playbook_lcps": self._findings_to_dict(result.playbook_lcps),
            "playbook_mcps": self._findings_to_dict(result.playbook_mcps),
            "skill_capabilities": self._findings_to_dict(result.skill_capabilities),
            "mcp_capabilities": self._findings_to_dict(result.mcp_capabilities),
            "file_paths": self._findings_to_dict(result.file_paths),
            "config_paths": self._findings_to_dict(result.config_paths),
        }
        fp = self.evidence_dir / "cross-dependency-validation.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return str(fp)

    def _findings_to_dict(self, findings: list) -> list[dict]:
        return [
            {
                "check": f.check,
                "status": f.status,
                "severity": f.severity.value,
                "detail": f.detail,
            }
            for f in findings
        ]

    def write_consistency_report(
        self,
        fragments: list[LoadedFragment],
        registry: ConsolidatedRegistry,
        schema_result: SchemaValidationResult,
        cross_result: CrossDependencyResult,
        conflicts: list[ConflictRecord],
        orphans: list[OrphanRecord],
        manifest: MergeManifest,
    ) -> str:
        lines = []
        lines.append("# AEOS Registry Consistency Report")
        lines.append("")
        lines.append(f"**Generated at:** {datetime.now(timezone.utc).isoformat()}")
        lines.append(f"**AEOS Version:** {manifest.generated_at}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 1. Fragment Loading Summary")
        lines.append("")
        lines.append(f"- Fragments found in overlay index: {len(fragments)}")
        lines.append(f"- Fragments loaded successfully: {manifest.fragments_loaded}")
        lines.append(f"- Fragments failed to load: {manifest.fragments_failed}")
        lines.append("")
        for frag in fragments:
            status = "OK" if frag.metadata.loaded else "FAILED"
            icon = "✓" if frag.metadata.loaded else "✗"
            lines.append(f"  - {icon} `{Path(frag.metadata.path).name}` [{frag.metadata.category.value}] → {status}")
            if frag.metadata.parse_error:
                lines.append(f"    - Error: {frag.metadata.parse_error}")
        lines.append("")

        lines.append("## 2. Consolidated Registry Overview")
        lines.append("")
        lines.append("| Registry Type | Entry Count |")
        lines.append("|---|---|")
        for rtype, count in sorted(manifest.total_entries_by_type.items()):
            lines.append(f"| {rtype} | {count} |")
        lines.append("")

        lines.append("## 3. Schema Validation")
        lines.append("")
        if schema_result.errors:
            lines.append("### Errors")
            for e in schema_result.errors:
                lines.append(f"  - ✗ {e}")
        if schema_result.warnings:
            lines.append("### Warnings")
            for w in schema_result.warnings:
                lines.append(f"  - ⚠ {w}")
        if schema_result.unknown_capabilities:
            lines.append("### Unknown Capabilities")
            for cap in sorted(schema_result.unknown_capabilities):
                lines.append(f"  - ⚠ {cap}")
        if not schema_result.errors and not schema_result.warnings:
            lines.append("- ✓ No schema issues found")
        lines.append("")

        lines.append("## 4. Conflicts")
        lines.append("")
        if conflicts:
            for c in conflicts:
                lines.append(f"  - ✗ `{c.entry_id}` ({c.registry_type.value}): path conflict between `{Path(c.source_a_path).name}` and `{Path(c.source_b_path).name}`")
                lines.append(f"    - Existing: `{c.existing_path}`")
                lines.append(f"    - Conflicting: `{c.conflicting_path}`")
        else:
            lines.append("- ✓ No conflicts detected")
        lines.append("")

        lines.append("## 5. Orphans")
        lines.append("")
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_orphans = sorted(orphans, key=lambda o: severity_order.get(o.severity.value, 99))
        if sorted_orphans:
            for o in sorted_orphans:
                icon = {"critical": "🚫", "high": "⚠", "medium": "⚡", "low": "ℹ"}
                lines.append(f"  - {icon.get(o.severity.value, '•')} `{o.orphan_id}` [{o.severity.value}] referenced by {o.referenced_by} ({o.reference_field})")
                lines.append(f"    - {o.description}")
            lines.append("")
            lines.append("### Orphan Counts by Severity")
            severity_counts = {}
            for o in sorted_orphans:
                severity_counts[o.severity.value] = severity_counts.get(o.severity.value, 0) + 1
            for sev in ["critical", "high", "medium", "low"]:
                if sev in severity_counts:
                    lines.append(f"  - {sev}: {severity_counts[sev]}")
        else:
            lines.append("- ✓ No orphans detected")
        lines.append("")

        lines.append("## 6. Cross-Dependency Validation")
        lines.append("")
        all_findings = cross_result.all_findings()
        errors = [f for f in all_findings if f.severity == ValidationSeverity.ERROR]
        warnings = [f for f in all_findings if f.severity == ValidationSeverity.WARNING]
        if errors:
            lines.append(f"### Errors ({len(errors)})")
            for e in errors:
                lines.append(f"  - ✗ [{e.check}] {e.detail}")
        if warnings:
            lines.append(f"### Warnings ({len(warnings)})")
            for w in warnings:
                lines.append(f"  - ⚠ [{w.check}] {w.detail}")
        if not errors and not warnings:
            lines.append("- ✓ No cross-dependency issues found")
        lines.append("")

        lines.append("## 7. Enterprise Registry Inclusion")
        lines.append("")
        enterprise_sources = [f for f in fragments if f.metadata.category.value == "enterprise"]
        if enterprise_sources:
            for es in enterprise_sources:
                lines.append(f"  - ✓ `{Path(es.metadata.path).name}` loaded ({es.metadata.entry_count} entries)")
        else:
            lines.append("  - ⚠ No enterprise registries found")
        lines.append("")

        lines.append("## 8. Overlay Index Usage")
        lines.append("")
        lines.append(f"- Overlay index was used to discover {len(fragments)} fragment(s)")
        lines.append("")

        lines.append("## 9. Deduplications")
        lines.append("")
        if manifest.deduplications:
            for d in manifest.deduplications:
                lines.append(f"  - ℹ `{d['entry_id']}` ({d['registry_type']}): {d['count']} occurrences, path `{d['path']}`")
        else:
            lines.append("- ✓ No deduplications needed")
        lines.append("")

        lines.append("## 10. Final Verdict")
        lines.append("")
        has_critical_orphans = any(o.severity.value == "critical" for o in orphans)
        has_cross_errors = cross_result.has_errors()
        has_conflicts = len(conflicts) > 0

        if has_critical_orphans or has_cross_errors:
            status = "**BLOCKED** 🚫"
            reasons = []
            if has_critical_orphans:
                reasons.append("Critical orphans found")
            if has_cross_errors:
                reasons.append(f"Cross-dependency errors: {len(cross_result.errors())}")
            if has_conflicts:
                reasons.append(f"Conflicts: {len(conflicts)}")
            lines.append(f"Status: {status}")
            for r in reasons:
                lines.append(f"- {r}")
        else:
            lines.append("Status: **PASS** ✓")
        lines.append("")

        lines.append("---")
        lines.append("*Report generated by AEOS Registry Loader Phase 2*")

        content = "\n".join(lines)
        fp = self.reports_dir / "registry-consistency-report.md"
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        return str(fp)
