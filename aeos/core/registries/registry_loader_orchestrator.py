from __future__ import annotations

import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from aeos.core.config.config_loader import ConfigLoader
from aeos.core.registries.cross_registry_dependency_validator import CrossRegistryDependencyValidator
from aeos.core.registries.overlay_index_loader import OverlayRegistryIndexLoader
from aeos.core.registries.overlay_registry_merger import OverlayRegistryMerger
from aeos.core.registries.registry_conflict_detector import RegistryConflictDetector
from aeos.core.registries.registry_fragment_loader import RegistryFragmentLoader
from aeos.core.registries.registry_models import (
    ConsolidatedRegistry,
    FragmentCategory,
    MergeManifest,
)
from aeos.core.registries.registry_orphan_detector import RegistryOrphanDetector
from aeos.core.registries.registry_reporter import RegistryReporter
from aeos.core.registries.schema_validator import SchemaValidator


def run_phase2(workspace_root: str = ".") -> dict:
    root = Path(workspace_root).resolve()
    results = {
        "status": "PASS",
        "blocks": [],
        "fragments_loaded": [],
        "conflicts_detected": [],
        "orphans_detected": [],
        "cross_validation": {},
        "output_files": [],
        "errors": [],
    }

    try:
        print("=" * 60)
        print("AEOS Phase 2 — Registry Loader & Consolidation")
        print("=" * 60)

        print("\n[1/8] Loading config...")
        config_loader = ConfigLoader(str(root))
        config = config_loader.load("aeos/config/aeos.config.yaml")
        print(f"  Config loaded: {config.name} v{config.version}")
        for finding in config_loader.findings:
            if finding.severity.value == "error":
                results["blocks"].append(finding.detail)
                results["errors"].append(finding.detail)
                print(f"  [ERROR] {finding.detail}")

        print("\n[2/8] Loading overlay index...")
        overlay_loader = OverlayRegistryIndexLoader(str(root))
        fragment_paths = overlay_loader.load(
            config.registries.overlay_index
            if config.registries.overlay_index
            else "aeos/registries/overlay.registry.index.yaml"
        )
        print(f"  Found {len(fragment_paths)} fragments in overlay index")

        print("\n[3/8] Loading registry fragments...")
        fragment_loader = RegistryFragmentLoader(str(root))
        fragments = fragment_loader.load_fragments(fragment_paths)
        loaded = [f for f in fragments if f.metadata.loaded]
        failed = [f for f in fragments if not f.metadata.loaded]
        print(f"  Loaded: {len(loaded)}, Failed: {len(failed)}")
        for f in failed:
            print(f"  [FAIL] {Path(f.metadata.path).name}: {f.metadata.parse_error}")

        print("\n[4/8] Detecting conflicts...")
        conflict_detector = RegistryConflictDetector()
        conflicts = conflict_detector.detect(fragments)
        print(f"  Conflicts: {len(conflicts)}, Deduplications: {len(conflict_detector.deduplications)}")
        for c in conflicts:
            print(f"  [CONFLICT] {c.entry_id}: {Path(c.source_a_path).name} vs {Path(c.source_b_path).name}")
            results["conflicts_detected"].append(c.entry_id)

        print("\n[5/8] Merging registries...")
        merger = OverlayRegistryMerger()
        registry = merger.merge(fragments)
        print(f"  Agents: {len(registry.agents)}")
        print(f"  SubAgents: {len(registry.subagents)}")
        print(f"  Skills: {len(registry.skills)}")
        print(f"  Playbooks: {len(registry.playbooks)}")
        print(f"  MCPs: {len(registry.mcps)}")
        print(f"  LCPs: {len(registry.lcps)}")
        print(f"  Blueprints: {len(registry.blueprints)}")
        print(f"  Profiles: {len(registry.profiles)}")

        print("\n[6/8] Validating schema & cross-dependencies...")
        schema_validator = SchemaValidator(str(root))
        schema_validator.load_capabilities()
        schema_result = schema_validator.validate(registry)
        print(f"  Schema valid: {schema_result.valid}")
        if schema_result.errors:
            for e in schema_result.errors:
                print(f"  [ERROR] {e}")
        if schema_result.warnings:
            for w in schema_result.warnings:
                print(f"  [WARN] {w}")

        cross_validator = CrossRegistryDependencyValidator(str(root))
        cross_result = cross_validator.validate(registry)
        print(f"  Cross-dependency errors: {len(cross_result.errors())}")
        for e in cross_result.errors():
            print(f"  [ERROR] [{e.check}] {e.detail}")
            results["cross_validation"][e.check] = e.detail

        print("\n[7/8] Detecting orphans...")
        orphan_detector = RegistryOrphanDetector()
        orphans = orphan_detector.detect(registry)
        sev_counts = orphan_detector.count_by_severity()
        print(f"  Critical: {sev_counts['critical']}, High: {sev_counts['high']}, Medium: {sev_counts['medium']}, Low: {sev_counts['low']}")
        for o in orphans:
            print(f"  {o.severity.value.upper()}: {o.orphan_id} ({o.referenced_by})")
            results["orphans_detected"].append({
                "id": o.orphan_id,
                "type": o.orphan_type,
                "severity": o.severity.value,
            })

        print("\n[8/8] Generating outputs...")
        reporter = RegistryReporter()

        consolidated_files = reporter.write_consolidated_registries(registry)
        for f in consolidated_files:
            print(f"  [OK] Generated: {f}")
            results["output_files"].append(f)

        manifest = MergeManifest(
            generated_at=datetime.now(timezone.utc).isoformat(),
            fragments_loaded=len(loaded),
            fragments_failed=len(failed),
            total_entries_by_type={
                "agents": len(registry.agents),
                "subagents": len(registry.subagents),
                "skills": len(registry.skills),
                "playbooks": len(registry.playbooks),
                "mcps": len(registry.mcps),
                "lcps": len(registry.lcps),
                "blueprints": len(registry.blueprints),
                "profiles": len(registry.profiles),
            },
            deduplications=conflict_detector.deduplications,
            conflicts_resolved=0,
            source_fragments=[f.metadata.path for f in fragments],
        )
        mf = reporter.write_merge_manifest(manifest)
        print(f"  [OK] Generated: {mf}")
        results["output_files"].append(mf)

        lf = reporter.write_loaded_fragments(fragments)
        print(f"  [OK] Generated: {lf}")
        results["output_files"].append(lf)

        cf = reporter.write_conflicts(conflicts)
        print(f"  [OK] Generated: {cf}")
        results["output_files"].append(cf)

        of = reporter.write_orphans(orphans)
        print(f"  [OK] Generated: {of}")
        results["output_files"].append(of)

        dv = reporter.write_cross_dependency_validation(cross_result)
        print(f"  [OK] Generated: {dv}")
        results["output_files"].append(dv)

        report_file = reporter.write_consistency_report(
            fragments, registry, schema_result, cross_result, conflicts, orphans, manifest
        )
        print(f"  [OK] Generated: {report_file}")
        results["output_files"].append(report_file)

        print("\n" + "=" * 60)
        has_critical_orphans = orphan_detector.has_critical_orphans()
        has_cross_errors = cross_result.has_errors()

        if has_critical_orphans:
            results["status"] = "BLOCKED"
            results["blocks"].append("Critical orphans found")
            print("  STATUS: BLOCKED (critical orphans)")
        elif has_cross_errors:
            results["status"] = "BLOCKED"
            results["blocks"].append("Cross-dependency errors found")
            print("  STATUS: BLOCKED (cross-dependency errors)")
        else:
            print("  STATUS: PASS")
        print("=" * 60)

    except Exception as e:
        results["status"] = "BLOCKED"
        results["blocks"].append(str(e))
        results["errors"].append(traceback.format_exc())
        print(f"\n  ERROR: {e}")
        traceback.print_exc()

    return results


if __name__ == "__main__":
    result = run_phase2()
    if result["status"] != "PASS":
        sys.exit(1)
