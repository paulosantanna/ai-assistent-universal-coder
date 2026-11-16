"""Shared types for the pre-push gate. Network failures become blocked results, never a pass."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path


class TransportError(Exception):
    pass


@dataclass
class Response:
    status: int
    headers: dict
    body: bytes

    def json(self):
        return json.loads(self.body.decode("utf-8"))

    def header(self, name: str) -> str | None:
        return self.headers.get(name.lower())


class UrllibTransport:
    def request(self, method, url, body=None, headers=None, timeout=30):
        hdrs = {"User-Agent": "codenavi-prepush", "Accept": "application/json"}
        if headers:
            hdrs.update(headers)
        data = None
        if body is not None:
            data = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
            hdrs.setdefault("Content-Type", "application/json")
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as res:
                return Response(res.status, {k.lower(): v for k, v in res.headers.items()}, res.read())
        except urllib.error.HTTPError as exc:
            return Response(exc.code, {k.lower(): v for k, v in (exc.headers or {}).items()}, exc.read())
        except urllib.error.URLError as exc:
            raise TransportError(str(exc.reason)) from exc


def utcnow():
    return datetime.now(timezone.utc)


def parse_http_date(value: str | None):
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_iso(value: str):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def version_key(value: str):
    text = value.strip().lstrip("v").split("+", 1)[0]
    number, _, pre = text.partition("-")
    parts = []
    for piece in number.split("."):
        if piece.isdigit():
            parts.append(int(piece))
        else:
            break
    while len(parts) < 3:
        parts.append(0)
    return (tuple(parts), 0 if not pre else -1, pre.lower())


def is_older(left: str, right: str) -> bool:
    return version_key(left) < version_key(right)


def excluded(path: Path, root: Path, prefixes: list[str]) -> bool:
    rel = path.relative_to(root).as_posix()
    if not rel.endswith("/"):
        rel_dir = rel + "/"
    else:
        rel_dir = rel
    return any(rel == prefix.rstrip("/") or rel_dir.startswith(prefix) or rel.startswith(prefix) for prefix in prefixes)


def iter_files(root: Path, prefixes: list[str], suffixes: set[str] | None = None):
    skip_names = {
        ".git", "node_modules", "target", "dist", "__pycache__", ".tools", ".aeos", ".work",
        ".venv", "venv", ".state", "site-packages", ".ruff_cache", ".mypy_cache", ".pytest_cache",
    }
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        if excluded(current, root, prefixes) and current != root:
            dirnames[:] = []
            continue
        dirnames[:] = [name for name in dirnames if name not in skip_names and not excluded(current / name, root, prefixes)]
        for name in filenames:
            path = current / name
            if suffixes is not None and path.suffix.lower() not in suffixes:
                continue
            if path.is_symlink():
                continue
            yield path


def read_text(path: Path, limit: int = 1_000_000) -> str | None:
    try:
        if path.stat().st_size > limit:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def finding(backend: str, code: str, message: str, path: str = "", subject: str = "", severity: str = "high") -> dict:
    return {
        "backend": backend,
        "code": code,
        "severity": severity,
        "path": path,
        "subject": subject or path,
        "message": message,
    }


def active_exceptions(path: Path, now: datetime) -> list[dict]:
    if not path.exists():
        return []
    items = load_json(path).get("exceptions") or []
    active = []
    for item in items:
        expires = item.get("expires")
        reason = item.get("reason")
        if not expires or not reason:
            continue
        try:
            deadline = parse_iso(expires)
        except ValueError:
            continue
        if deadline > now:
            active.append(item)
    return active


def waived(exceptions: list[dict], item: dict) -> bool:
    for rule in exceptions:
        if rule.get("backend") not in (item["backend"], "*"):
            continue
        if rule.get("code") not in (item["code"], "*"):
            continue
        subject = rule.get("subject")
        if subject and subject not in (item.get("subject"), item.get("path")):
            continue
        return True
    return False


@dataclass
class BackendResult:
    id: str
    status: str
    source: str
    source_version: str
    fetched_at: str
    fresh: bool
    findings: list = field(default_factory=list)
    evidence: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "status": self.status,
            "source": self.source,
            "source_version": self.source_version,
            "fetched_at": self.fetched_at,
            "fresh": self.fresh,
            "findings": self.findings,
            "evidence": self.evidence,
        }


def finish(backend: str, source: str, source_version: str, fetched_at: datetime, findings: list, evidence: dict, fresh: bool) -> BackendResult:
    blocking = [item for item in findings if item.get("severity") != "info"]
    if not fresh:
        status = "blocked"
    elif blocking:
        status = "fail"
    else:
        status = "pass"
    return BackendResult(backend, status, source, source_version, iso(fetched_at), fresh, findings, evidence)
