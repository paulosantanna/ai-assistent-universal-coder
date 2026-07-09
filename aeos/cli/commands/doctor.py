import sys
import importlib
from pathlib import Path


REQUIRED_MODULES = [
    "aeos.core.config.config_loader",
    "aeos.core.permissions.permission_engine",
    "aeos.core.policy.policy_engine",
    "aeos.core.evidence.evidence_store",
    "aeos.core.governance.governance_gate",
    "aeos.core.tool_router.router",
    "aeos.core.skill_engine.skill_executor",
    "aeos.core.playbook_engine.playbook_executor",
    "aeos.core.agent_runtime.agent_runtime",
    "aeos.core.runtime.runtime_orchestrator",
    "aeos.core.judge.deterministic_judge",
    "aeos.core.evals.eval_runner",
    "aeos.core.readiness.production_gate",
    "aeos.core.evidence.evidence_manifest",
    "aeos.core.packaging.package_verifier",
    "aeos.core.packaging.package_builder",
    "aeos.core.release.release_gate",
    "aeos.core.readiness.readiness_auditor",
]


def cmd_doctor(args) -> int:
    from aeos.cli.main import resolve_aeos_root, resolve_target_path
    workspace = resolve_target_path(args)
    aeos_root = resolve_aeos_root(args)
    checks = []

    # Python version
    py_version = sys.version_info
    checks.append(("Python >= 3.8", py_version >= (3, 8), f"{py_version.major}.{py_version.minor}.{py_version.micro}"))

    # AEOS path
    code_root = Path(__file__).resolve().parent.parent.parent
    checks.append(("AEOS code root exists", code_root.exists(), str(code_root)))

    # AEOS root config
    checks.append(("AEOS root", aeos_root.exists(), str(aeos_root)))

    # Config dir
    config_dir = aeos_root / ".aeos" / "config"
    checks.append(("Config directory", config_dir.exists(), str(config_dir)))
    if config_dir.exists():
        config_files = list(config_dir.glob("*"))
        checks.append(("Config files", len(config_files) > 0, f"{len(config_files)} file(s)"))

    # Registry dir
    registry_dir = aeos_root / ".aeos" / "registries"
    checks.append(("Registry directory", registry_dir.exists(), str(registry_dir)))

    # Derived registries
    registry_configs = list(registry_dir.rglob("*.yaml")) + list(registry_dir.rglob("*.yml")) + list(registry_dir.rglob("*.json"))
    checks.append(("Registry configs", len(registry_configs) > 0, f"{len(registry_configs)} file(s)"))

    # Permissions config
    perm_config = aeos_root / ".aeos" / "config" / "permissions.yaml"
    checks.append(("Permissions config", perm_config.exists(), str(perm_config)))

    # Policies config
    policy_config = aeos_root / ".aeos" / "config" / "policies.yaml"
    checks.append(("Policies config", policy_config.exists(), str(policy_config)))

    # Evidence dir
    evidence_dir = aeos_root / ".aeos" / "evidence"
    checks.append(("Evidence directory", evidence_dir.exists(), str(evidence_dir)))

    # Reports dir
    reports_dir = aeos_root / ".aeos" / "reports"
    checks.append(("Reports directory", reports_dir.exists(), str(reports_dir)))

    # Required modules
    missing_modules = []
    for mod_name in REQUIRED_MODULES:
        try:
            importlib.import_module(mod_name)
        except ImportError:
            missing_modules.append(mod_name)
    checks.append(("Required modules", len(missing_modules) == 0, f"{len(REQUIRED_MODULES) - len(missing_modules)}/{len(REQUIRED_MODULES)}"))
    if missing_modules:
        for mm in missing_modules:
            checks.append((f"  Module: {mm}", False, "missing"))

    # pytest.ini without BOM
    pytest_ini = workspace / "pytest.ini"
    if not pytest_ini.exists():
        pytest_ini = aeos_root / "pytest.ini"
    bom_check = True
    bom_msg = "not found"
    if pytest_ini.exists():
        content = pytest_ini.read_bytes()
        if content.startswith(b"\xef\xbb\xbf"):
            bom_check = False
            bom_msg = "BOM detected"
        else:
            bom_msg = "no BOM"
    checks.append(("pytest.ini without BOM", bom_check, bom_msg))

    # Package verifier
    try:
        from aeos.core.packaging.package_verifier import PackageVerifier
        verifier_ok = True
    except ImportError:
        verifier_ok = False
    checks.append(("Package verifier", verifier_ok, "available" if verifier_ok else "missing"))

    # Readiness auditor
    try:
        from aeos.core.readiness.readiness_auditor import ReadinessAuditor
        auditor_ok = True
    except ImportError:
        auditor_ok = False
    checks.append(("Readiness auditor", auditor_ok, "available" if auditor_ok else "missing"))

    # Generate report
    failures = sum(1 for _, ok, _ in checks if not ok)
    warnings = sum(1 for name, ok, _ in checks if not ok and "missing" not in name.lower() and "bom" not in name.lower())
    reviews = sum(1 for name, ok, _ in checks if not ok and ("not found" in name.lower() or "empty" in name.lower()))

    report_lines = ["# AEOS Doctor Report", "", f"- **AEOS Root**: {aeos_root}", f"- **Target**: {workspace}", f"- **Timestamp**: {__import__('datetime').datetime.now().isoformat()}", ""]
    if failures > 0:
        report_lines.append(f"## Issues Found ({failures})")
        report_lines.append("")
    report_lines.append("## Check Results")
    report_lines.append("")
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        report_lines.append(f"| {name} | {status} | {detail} |")
    report_lines.append("")
    report_lines.append(f"## Summary: {'PASS' if failures == 0 else 'BLOCKED' if failures > 2 else 'REVIEW'}")
    report_lines.append("")
    report_lines.append(f"- **Total checks**: {len(checks)}")
    report_lines.append(f"- **Passed**: {len(checks) - failures}")
    report_lines.append(f"- **Failed**: {failures}")

    report = "\n".join(report_lines)
    report_dir = aeos_root / ".aeos" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "doctor-report.md"
    report_path.write_text(report, encoding="utf-8")

    print(report)

    if failures == 0:
        return 0
    elif failures <= 2:
        return 3  # REVIEW
    else:
        return 1  # BLOCKED
