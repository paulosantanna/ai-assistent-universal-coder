"""Run the six pre-push backends and fail closed unless every one passes."""

from __future__ import annotations

import json
from pathlib import Path

from backends.cve_google import check as check_cves
from backends.common import BackendResult, UrllibTransport, active_exceptions, utcnow, waived
from backends.executables import check as check_executables
from backends.language import check as check_language
from backends.libraries import check as check_libraries
from backends.manifests import discover
from backends.sast import check as check_sast
from backends.security import check as check_security


HERE = Path(__file__).resolve().parent


def _status(result: BackendResult) -> str:
    blocking = [item for item in result.findings if item.get("severity") != "info"]
    if not result.fresh:
        return "blocked"
    if blocking:
        return "fail"
    return "pass"


def run(root, policy=None, transport=None, now=None, runtime=None, catalog_dir=None, exceptions_path=None) -> dict:
    root = Path(root)
    policy = policy or json.loads((HERE / "policy.json").read_text(encoding="utf-8"))
    transport = transport or UrllibTransport()
    now = now or utcnow()
    catalog_dir = Path(catalog_dir) if catalog_dir else HERE / "catalogs"
    exceptions_path = Path(exceptions_path) if exceptions_path else HERE / "exceptions.json"
    manifests = discover(root, policy["exclude_prefixes"])
    results = [
        check_cves(root, policy, transport, now, manifests),
        check_libraries(root, policy, transport, now, manifests),
        check_language(root, policy, transport, now, runtime),
        check_executables(root, policy, transport, now, manifests),
        check_sast(root, policy, transport, now, catalog_dir / "sast.json"),
        check_security(root, policy, transport, now, catalog_dir / "security.json"),
    ]
    exceptions = active_exceptions(exceptions_path, now)
    for result in results:
        result.findings = [item for item in result.findings if not waived(exceptions, item)]
        result.status = _status(result)
    statuses = {result.status for result in results}
    if "blocked" in statuses:
        status = "blocked"
    elif "fail" in statuses:
        status = "fail"
    else:
        status = "pass"
    return {
        "status": status,
        "checked_at": results[0].fetched_at,
        "root": str(root),
        "backends": [result.as_dict() for result in results],
    }


def write_report(report: dict, root: Path) -> Path:
    destination = root / ".aeos" / "prepush" / "report.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return destination
