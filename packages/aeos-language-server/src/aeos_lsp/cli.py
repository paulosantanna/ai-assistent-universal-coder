from __future__ import annotations

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

from aeos_lsp.capabilities import build_server_capabilities
from aeos_lsp.configuration import LSPClientConfig
from aeos_lsp.constants import (
    EXIT_SUCCESS,
    EXIT_DIAGNOSTICS_ERROR,
    EXIT_INTERNAL_ERROR,
    EXIT_INVALID_CONFIG,
    EXIT_OPERATION_BLOCKED,
    EXIT_TIMEOUT,
    SERVER_NAME,
    SERVER_VERSION,
)

logger = logging.getLogger(__name__)


def _create_lightweight_server(config: LSPClientConfig | None = None) -> Any:
    from aeos_lsp.server import AEOSLanguageServer
    cfg = config or LSPClientConfig()
    return AEOSLanguageServer(config=cfg)


def _validate_workspace_path(path: str) -> Path:
    p = Path(path).resolve()
    if not p.exists():
        print(f"Error: path does not exist: {path}", file=sys.stderr)
        sys.exit(EXIT_INVALID_CONFIG)
    if not p.is_dir():
        print(f"Error: path is not a directory: {path}", file=sys.stderr)
        sys.exit(EXIT_INVALID_CONFIG)
    return p


def cli_validate(workspace_path: str) -> int:
    p = _validate_workspace_path(workspace_path)
    print(f"Validating workspace: {p}", file=sys.stderr)

    try:
        server = _create_lightweight_server()
        server.workspace_manager.add_folder(
            server.workspace_manager.__class__.__module__  # placeholder
        )

        from aeos_lsp.workspace import WorkspaceFolderInfo
        from aeos_lsp.index import WorkspaceIndexer, SqliteStore
        from aeos_lsp.parsing import ParserDispatcher

        parser = ParserDispatcher()
        indexer = WorkspaceIndexer(
            workspace_manager=server.workspace_manager,
            semantic_model=server.semantic_model,
            store=SqliteStore(workspace_root=p),
        )

        aeos_files = _collect_aeos_files(p)
        if not aeos_files:
            print("No AEOS documents found in workspace", file=sys.stderr)
            return EXIT_SUCCESS

        errors = 0
        warnings = 0
        for file_path in aeos_files:
            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
                result = parser.parse(file_path.as_uri(), text)
                if result.errors:
                    for err in result.errors:
                        severity = getattr(err, "severity", "error")
                        msg = getattr(err, "message", str(err))
                        loc = getattr(err, "location", "")
                        print(f"  {severity}: {file_path} {loc} - {msg}")
                        if severity == "error":
                            errors += 1
                        else:
                            warnings += 1
                elif result.ast is not None:
                    server.semantic_model.update_for_document(
                        file_path.as_uri(), result,
                    )
            except Exception as e:
                print(f"  error: {file_path} - {e}", file=sys.stderr)
                errors += 1

        print(f"Validation complete: {errors} errors, {warnings} warnings", file=sys.stderr)
        return EXIT_DIAGNOSTICS_ERROR if errors > 0 else EXIT_SUCCESS

    except Exception as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        logger.exception("Validation failed")
        return EXIT_INTERNAL_ERROR


def cli_index(workspace_path: str) -> int:
    p = _validate_workspace_path(workspace_path)
    print(f"Indexing workspace: {p}", file=sys.stderr)

    try:
        from aeos_lsp.index import WorkspaceIndexer, SqliteStore
        from pathlib import Path

        server = _create_lightweight_server()
        store = SqliteStore(workspace_root=p)
        indexer = WorkspaceIndexer(
            workspace_manager=server.workspace_manager,
            semantic_model=server.semantic_model,
            store=store,
        )

        start = time.monotonic()
        result = indexer.index_workspace()
        elapsed = time.monotonic() - start

        indexed = sum(1 for s in result.values() if s.status.value == "indexed")
        failed = sum(1 for s in result.values() if s.status.value == "failed")
        skipped = sum(1 for s in result.values() if s.status.value == "skipped")
        total = len(result)

        print(f"Indexed {indexed}/{total} documents ({failed} failed, {skipped} skipped) in {elapsed:.2f}s", file=sys.stderr)
        return EXIT_DIAGNOSTICS_ERROR if failed > 0 else EXIT_SUCCESS

    except Exception as e:
        print(f"Indexing failed: {e}", file=sys.stderr)
        logger.exception("Indexing failed")
        return EXIT_INTERNAL_ERROR


def cli_diagnostics(workspace_path: str, output_format: str = "editor") -> int:
    p = _validate_workspace_path(workspace_path)
    print(f"Running diagnostics: {p}", file=sys.stderr)

    try:
        from aeos_lsp.diagnostics import DiagnosticsEngine, DiagnosticRuleRegistry, DiagnosticPublisher
        from aeos_lsp.output import DiagnosticFormatter

        server = _create_lightweight_server()
        registry = DiagnosticRuleRegistry()
        registry.register_defaults()
        engine = DiagnosticsEngine(registry=registry)
        formatter = DiagnosticFormatter(profile=output_format)

        formatter._profile = output_format

        aeos_files = _collect_aeos_files(p)
        all_diagnostics: dict[str, list] = {}
        total_errors = 0

        for file_path in aeos_files:
            try:
                import lsprotocol.types as lsp_types
                text = file_path.read_text(encoding="utf-8", errors="replace")
                uri = file_path.as_uri()

                from aeos_lsp.parsing import ParserDispatcher
                parser = ParserDispatcher()
                parse_result = parser.parse(uri, text)
                if parse_result is not None:
                    server.semantic_model.update_for_document(uri, parse_result)

                result = engine.run_document_diagnostics(
                    uri, text, server.semantic_model, server._config,
                )
                docs = result.diagnostics.get(uri, [])
                if docs:
                    all_diagnostics[uri] = docs
                    total_errors += sum(
                        1 for d in docs if getattr(d, "severity", None) == lsp_types.DiagnosticSeverity.Error
                    )
            except Exception as e:
                logger.warning("Failed to analyze %s: %s", file_path, e)

        if output_format == "json":
            output = _diagnostics_to_json(all_diagnostics)
            print(output)
        elif output_format == "sarif":
            output = _diagnostics_to_sarif(all_diagnostics)
            print(output)
        else:
            for uri, diags in all_diagnostics.items():
                formatted = formatter.format(diags, uri)
                if formatted:
                    print(formatted)
                    print()

        print(f"Total: {len(all_diagnostics)} files with diagnostics, {total_errors} errors", file=sys.stderr)
        return EXIT_DIAGNOSTICS_ERROR if total_errors > 0 else EXIT_SUCCESS

    except Exception as e:
        print(f"Diagnostics failed: {e}", file=sys.stderr)
        logger.exception("Diagnostics failed")
        return EXIT_INTERNAL_ERROR


def _diagnostics_to_json(all_diagnostics: dict[str, list]) -> str:
    output: dict[str, list[dict[str, Any]]] = {}
    for uri, diags in all_diagnostics.items():
        entry_list: list[dict[str, Any]] = []
        for d in diags:
            entry_list.append({
                "uri": uri,
                "range": {
                    "start": {"line": d.range.start.line, "character": d.range.start.character},
                    "end": {"line": d.range.end.line, "character": d.range.end.character},
                },
                "severity": str(d.severity) if d.severity else "unknown",
                "code": d.code,
                "source": d.source,
                "message": d.message,
            })
        output[uri] = entry_list
    return json.dumps(output, indent=2, ensure_ascii=False)


def _diagnostics_to_sarif(all_diagnostics: dict[str, list]) -> str:
    results: list[dict[str, Any]] = []
    for uri, diags in all_diagnostics.items():
        for d in diags:
            level = "none"
            if d.severity and d.severity.value <= 1:
                level = "error"
            elif d.severity and d.severity.value == 2:
                level = "warning"
            elif d.severity and d.severity.value >= 3:
                level = "note"
            results.append({
                "ruleId": str(d.code or "unknown"),
                "level": level,
                "message": {"text": d.message},
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": uri},
                        "region": {
                            "startLine": d.range.start.line + 1,
                            "startColumn": d.range.start.character + 1,
                            "endLine": d.range.end.line + 1,
                            "endColumn": d.range.end.character + 1,
                        },
                    },
                }],
            })
    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION,
                    "informationUri": "https://aeos.ai",
                },
            },
            "results": results,
        }],
    }
    return json.dumps(sarif, indent=2, ensure_ascii=False)


def cli_doctor() -> int:
    print(f"AEOS Language Server v{SERVER_VERSION}")
    print()

    checks: list[tuple[str, bool, str]] = []

    try:
        import pygls
        checks.append(("pygls", True, getattr(pygls, "__version__", "2.1.1")))
    except ImportError:
        checks.append(("pygls", False, "not installed"))

    try:
        import lsprotocol
        checks.append(("lsprotocol", True, getattr(lsprotocol, "__version__", "unknown")))
    except ImportError:
        checks.append(("lsprotocol", False, "not installed"))

    try:
        import yaml
        checks.append(("PyYAML", True, getattr(yaml, "__version__", "unknown")))
    except ImportError:
        checks.append(("PyYAML", False, "not installed"))

    try:
        import pydantic
        checks.append(("pydantic", True, pydantic.__version__))
    except ImportError:
        checks.append(("pydantic", False, "not installed"))

    try:
        import tomli
        checks.append(("tomli", True, tomli.__version__))
    except ImportError:
        checks.append(("tomli", False, "not installed"))

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    checks.append(("Python", True, python_version))
    checks.append(("Platform", True, sys.platform))

    print("Dependency check:")
    for name, ok, detail in checks:
        status = "[OK]" if ok else "[FAIL]"
        print(f"  {status} {name}: {detail}")

    print()
    config_ok = _check_config_integrity()
    paths_ok = _check_path_integrity()

    all_ok = all(ok for _, ok, _ in checks) and config_ok and paths_ok
    print()
    if all_ok:
        print("Doctor: All checks passed")
    else:
        print("Doctor: Some checks failed", file=sys.stderr)

    return EXIT_SUCCESS if all_ok else EXIT_INTERNAL_ERROR


def _check_config_integrity() -> bool:
    try:
        from aeos_lsp.configuration import LSPClientConfig
        cfg = LSPClientConfig()
        _ = cfg.to_dict()
        print("  [OK] Configuration model")
        return True
    except Exception as e:
        print(f"  [FAIL] Configuration model: {e}", file=sys.stderr)
        return False


def _check_path_integrity() -> bool:
    ok = True
    expected_dirs = [
        "aeos_lsp/commands",
        "aeos_lsp/diagnostics",
        "aeos_lsp/features",
        "aeos_lsp/index",
        "aeos_lsp/output",
        "aeos_lsp/parsing",
        "aeos_lsp/protocol",
        "aeos_lsp/runtime",
        "aeos_lsp/schemas",
        "aeos_lsp/security",
        "aeos_lsp/semantic",
        "aeos_lsp/telemetry",
        "aeos_lsp/workspace",
    ]
    try:
        import aeos_lsp
        base = Path(aeos_lsp.__file__).parent
        for dirname in expected_dirs:
            d = base / dirname.replace("aeos_lsp/", "")
            if d.is_dir():
                print(f"  [OK] {dirname}")
            else:
                print(f"  [FAIL] {dirname}: not found", file=sys.stderr)
                ok = False
    except Exception as e:
        print(f"  [FAIL] Path check: {e}", file=sys.stderr)
        ok = False
    return ok


def cli_capabilities() -> int:
    try:
        config = LSPClientConfig()
        caps = build_server_capabilities(config)
        caps_dict = _serialize_capabilities(caps)
        print(json.dumps(caps_dict, indent=2, default=str))
        return EXIT_SUCCESS
    except Exception as e:
        print(f"Failed to generate capabilities: {e}", file=sys.stderr)
        logger.exception("Capabilities generation failed")
        return EXIT_INTERNAL_ERROR


def _serialize_capabilities(caps: Any) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for attr_name in dir(caps):
        if attr_name.startswith("_"):
            continue
        value = getattr(caps, attr_name, None)
        if value is None:
            continue
        result[attr_name] = _serialize_value(value)
    return result


def _serialize_value(value: Any) -> Any:
    if hasattr(value, "__dict__"):
        return {k: _serialize_value(v) for k, v in value.__dict__.items() if not k.startswith("_")}
    if isinstance(value, list):
        return [_serialize_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialize_value(v) for k, v in value.items() if not k.startswith("_")}
    if hasattr(value, "value"):
        return value.value
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def cli_version() -> int:
    print(f"{SERVER_NAME} v{SERVER_VERSION}")
    return EXIT_SUCCESS


def _collect_aeos_files(root: Path) -> list[Path]:
    from aeos_lsp.constants import AEOS_DOCUMENT_PATTERNS, DEFAULT_EXCLUSIONS

    files: list[Path] = []
    excluded_dirs = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", "build", "dist", ".aeos"}

    for pattern in AEOS_DOCUMENT_PATTERNS:
        if "*" in pattern:
            found = list(root.rglob(pattern))
        else:
            found = [root / pattern] if (root / pattern).is_file() else []

        for f in found:
            try:
                rel = f.relative_to(root)
                parts = rel.parts
                if any(p in excluded_dirs for p in parts):
                    continue
                if f not in files:
                    files.append(f)
            except ValueError:
                continue

    files.sort(key=lambda p: p.as_posix())
    logger.debug("Collected %d AEOS files from %s", len(files), root)
    return files
