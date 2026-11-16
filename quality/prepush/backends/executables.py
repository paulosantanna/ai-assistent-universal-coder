"""Committed application executables must name a creator and a current file version."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from backends.common import finding, finish, iter_files
from backends.pe import parse_pe


BACKEND = "executables"


def check(root, policy, transport, now, manifests=None):
    del transport, manifests
    findings = []
    inspected = []
    max_age = timedelta(days=policy["executable_max_age_days"])
    for path in iter_files(root, policy["exclude_prefixes"], {".exe"}):
        rel = path.relative_to(root).as_posix()
        try:
            info = parse_pe(path.read_bytes())
        except (OSError, ValueError) as exc:
            findings.append(finding(BACKEND, "exe-unreadable", f"{rel} nao pode ser lido como PE: {exc}", rel, rel))
            continue
        strings = info["strings"]
        created = datetime.fromtimestamp(info["timestamp"], timezone.utc) if info["timestamp"] else None
        inspected.append({
            "path": rel,
            "creator": strings.get("CompanyName", ""),
            "file_version": strings.get("FileVersion", ""),
            "product": strings.get("ProductName", ""),
            "built_at": created.strftime("%Y-%m-%dT%H:%M:%SZ") if created else "",
        })
        if not strings.get("CompanyName"):
            findings.append(finding(BACKEND, "exe-creator-missing", f"{rel} nao informa CompanyName", rel, rel))
        if not strings.get("FileVersion"):
            findings.append(finding(BACKEND, "exe-version-missing", f"{rel} nao informa FileVersion", rel, rel))
        if created is None:
            findings.append(finding(BACKEND, "exe-timestamp-missing", f"{rel} nao tem data de compilacao", rel, rel))
        elif created > now + timedelta(days=1):
            findings.append(finding(BACKEND, "exe-timestamp-invalid", f"{rel} tem data de compilacao no futuro", rel, rel))
        elif now - created > max_age:
            findings.append(finding(
                BACKEND,
                "exe-stale",
                f"{rel} compilado em {created.date()} passou de {policy['executable_max_age_days']} dias",
                rel,
                rel,
            ))
    return finish(
        BACKEND,
        "pe-version-resource",
        str(len(inspected)),
        now,
        findings,
        {"executables": inspected, "applicable": bool(inspected)},
        True,
    )
