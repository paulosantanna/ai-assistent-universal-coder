from pathlib import Path


def cmd_package_create(args) -> int:
    from aeos.cli.main import get_workspace_root, get_execution_id
    workspace = get_workspace_root(args)
    execution_id = get_execution_id(args)

    try:
        from aeos.core.packaging.package_builder import PackageBuilder
        from aeos.core.packaging.package_models import PackageBuildRequest
        builder = PackageBuilder(workspace_root=str(workspace))
        request = PackageBuildRequest(execution_id=execution_id)
        result = builder.create_package(request)
        if result.status.value == "failed":
            print(f"Package creation failed: {result.error}")
            return 2
        print(f"Package created: {result.package_path}")
        from aeos.core.packaging.package_reporter import PackageReporter
        report = PackageReporter.generate_build_report(result)
        report_dir = workspace / ".aeos" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"package-build-{execution_id}.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"Build report: {report_path}")
        return 0
    except Exception as e:
        print(f"Error creating package: {e}", file=__import__("sys").stderr)
        return 2


def cmd_package_verify(args) -> int:
    pkg_path = Path(args.path)
    if not pkg_path.exists():
        print(f"Package not found: {pkg_path}", file=__import__("sys").stderr)
        return 2

    try:
        from aeos.core.packaging.package_verifier import PackageVerifier
        result = PackageVerifier.verify(pkg_path)
        from aeos.core.packaging.package_reporter import PackageReporter
        report = PackageReporter.generate_verify_report(result)
        print(report)
        report_dir = pkg_path.parent / ".aeos" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"package-verify-{pkg_path.stem}.md"
        report_path.write_text(report, encoding="utf-8")
        if result.verified:
            print(f"\nPackage verification: PASS")
            return 0
        else:
            print(f"\nPackage verification: FAIL")
            for e in result.errors:
                print(f"  - {e}")
            return 1
    except Exception as e:
        print(f"Error verifying package: {e}", file=__import__("sys").stderr)
        return 2
