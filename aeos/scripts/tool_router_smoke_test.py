from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from aeos.core.tool_router.router import ToolRouter, register_adapter
from aeos.core.tool_router.tool_models import ToolRequest
from aeos.core.tool_router.adapters.filesystem_readonly_adapter import FilesystemReadonlyAdapter
from aeos.core.tool_router.adapters.filesystem_sandbox_write_adapter import FilesystemSandboxWriteAdapter
from aeos.core.tool_router.adapters.package_local_adapter import PackageLocalAdapter
from aeos.core.tool_router.adapters.test_runner_mock_adapter import TestRunnerMockAdapter
from aeos.core.evidence.evidence_store import EvidenceStore


EXECUTION_ID = "smoke-tool-router-001"
results: list[tuple[str, bool, str]] = []
errors: list[str] = []


def check(name: str, condition: bool, detail: str = ""):
    if condition:
        print(f"  [PASS] {name}")
    else:
        msg = f"  [FAIL] {name}"
        if detail:
            msg += f" - {detail}"
        print(msg)
        errors.append(name)
    results.append((name, condition, detail))


def main() -> int:
    print("=" * 60)
    print("AEOS Tool Router Smoke Test")
    print("=" * 60)

    register_adapter("filesystem-readonly", FilesystemReadonlyAdapter)
    register_adapter("filesystem-write-sandbox", FilesystemSandboxWriteAdapter)
    register_adapter("package-local", PackageLocalAdapter)
    register_adapter("test-runner-controlled", TestRunnerMockAdapter)

    evidence = EvidenceStore()
    router = ToolRouter(workspace_root=".", evidence_store=evidence)
    router.initialize()

    router.register_adapter_instance("filesystem-readonly", FilesystemReadonlyAdapter())
    router.register_adapter_instance("filesystem-write-sandbox", FilesystemSandboxWriteAdapter())
    router.register_adapter_instance("package-local", PackageLocalAdapter())
    router.register_adapter_instance("test-runner-controlled", TestRunnerMockAdapter())

    print("\n[1] Tool inexistente => BLOCKED")
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="tester", role="tester",
        tool_id="nonexistent-tool", action="filesystem.read",
        capability="READ_FILES", resource="aeos/README.md",
    )
    result = router.route(req)
    check("unknown tool blocked", result.status == "BLOCKED", f"got {result.status}: {result.error}")

    print("\n[2] Actor sem capability => BLOCKED")
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="tester", role="tester",
        tool_id="filesystem-readonly", action="filesystem.read",
        capability="NONEXISTENT_CAP", resource="aeos/README.md",
    )
    result = router.route(req)
    check("no capability blocked", result.status == "BLOCKED", f"got {result.status}")

    print("\n[3] Policy denied => BLOCKED")
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="coder", role="coder",
        tool_id="filesystem-write-sandbox", action="filesystem.write",
        capability="WRITE_SANDBOX_FILES", resource="outside.txt",
    )
    result = router.route(req)
    check("write outside sandbox blocked", result.status == "BLOCKED", f"got {result.status}: {result.error}")

    print("\n[4] filesystem-readonly stat_file permitido")
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="architect", role="architect",
        tool_id="filesystem-readonly", action="filesystem.exists",
        capability="READ_FILES", resource="aeos/config",
    )
    result = router.route(req)
    check("stat_file allowed", result.status == "PASS", f"got {result.status}: {result.error}")
    if result.status == "PASS":
        check("file exists", result.output.get("exists") is True, f"got {result.output}")

    print("\n[5] read_text_file bloqueia acima do limite")
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="architect", role="architect",
        tool_id="filesystem-readonly", action="filesystem.read",
        capability="READ_FILES", resource="aeos/config/aeos.config.yaml",
    )
    tiny_adapter = FilesystemReadonlyAdapter(max_file_bytes=10)
    router.register_adapter_instance("filesystem-readonly", tiny_adapter)
    result = router.route(req)
    check("oversize file blocked", result.status == "PASS" and "exceeds size limit" in result.output.get("error", ""),
          f"got output={result.output}")

    print("\n[6] write_sandbox permite dentro de sandbox")
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="coder", role="coder",
        tool_id="filesystem-write-sandbox", action="filesystem.write_sandbox",
        capability="WRITE_SANDBOX_FILES", resource="test_smoke.txt",
        input={"content": "smoke test content"},
    )
    result = router.route(req)
    check("sandbox write allowed", result.status == "PASS", f"got {result.status}: {result.error}")

    print("\n[7] write_sandbox bloqueia fora de sandbox")
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="coder", role="coder",
        tool_id="filesystem-write-sandbox", action="filesystem.write_sandbox",
        capability="WRITE_SANDBOX_FILES", resource="..\\outside.txt",
        input={"content": "should be blocked"},
    )
    sandbox_adapter = FilesystemSandboxWriteAdapter(sandbox_base=".aeos/sandbox")
    router.register_adapter_instance("filesystem-write-sandbox", sandbox_adapter)
    result = router.route(req)
    check("outside sandbox blocked", result.status == "PASS" and "outside sandbox" in (result.output.get("error", "") or "").lower(),
          f"got output={result.output}")

    print("\n[8] package verify bloqueia path traversal")
    import zipfile, io
    traversal_zip = io.BytesIO()
    with zipfile.ZipFile(traversal_zip, "w") as zf:
        zf.writestr("../../etc/passwd", "pwned")
    traversal_zip.seek(0)
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="judge", role="judge",
        tool_id="package-local", action="package.verify",
        capability="PACKAGE_VERIFY", resource="",
        input={"content": list(traversal_zip.read())},
    )
    result = router.route(req)
    check("path traversal blocked", result.status == "PASS" and "traversal" in str(result.output.get("error", "") or result.output.get("errors", [])).lower(),
          f"got output={result.output}")

    print("\n[9] package verify bloqueia absolute path")
    abs_zip = io.BytesIO()
    with zipfile.ZipFile(abs_zip, "w") as zf:
        zf.writestr("/absolute/file.txt", "data")
    abs_zip.seek(0)
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="judge", role="judge",
        tool_id="package-local", action="package.verify",
        capability="PACKAGE_VERIFY", resource="",
        input={"content": list(abs_zip.read())},
    )
    result = router.route(req)
    check("absolute path blocked", result.status == "PASS" and "absolute" in str(result.output.get("error", "") or result.output.get("errors", [])).lower(),
          f"got output={result.output}")

    print("\n[10] package verify bloqueia .git")
    git_zip = io.BytesIO()
    with zipfile.ZipFile(git_zip, "w") as zf:
        zf.writestr(".git/config", "dummy")
    git_zip.seek(0)
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="judge", role="judge",
        tool_id="package-local", action="package.verify",
        capability="PACKAGE_VERIFY", resource="",
        input={"content": list(git_zip.read())},
    )
    result = router.route(req)
    check(".git blocked", result.status == "PASS" and ".git" in str(result.output.get("error", "") or result.output.get("errors", [])),
          f"got output={result.output}")

    print("\n[11] test-runner retorna disabled/simulado")
    req = ToolRequest(
        execution_id=EXECUTION_ID, actor="tester", role="tester",
        tool_id="test-runner-controlled", action="test.detect",
        capability="RUN_TESTS", resource="",
    )
    result = router.route(req)
    check("test runner mock", result.status == "PASS" and "disabled" in str(result.output.get("note", "")).lower(),
          f"got output={result.output}")

    print("\n[12] MCP Registry Resolver smoke")
    from aeos.core.mcp_runtime.mcp_registry_resolver import MCPRegistryResolver
    resolver = MCPRegistryResolver()
    report = resolver.load()
    check("mcps validated", report.mcps_validated > 0, f"got {report.mcps_validated}")
    check("risk report generated", bool(resolver.generate_risk_report(EXECUTION_ID, report)),
          "risk report path is empty")

    print("\n[13] generate tool-router-report")
    report_path = router.generate_report()
    check("report generated", bool(report_path), f"got {report_path}")

    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r[1])
    total = len(results)
    failed = total - passed
    print(f"Results: {passed}/{total} passed, {failed} failed")
    if failed == 0:
        print("\n  STATUS: PASS")
    else:
        print(f"\n  STATUS: FAIL ({failed} errors)")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
