"""Read direct dependencies and lockfiles. Versions that are not exact stay unpinned."""

from __future__ import annotations

import json
import re
from pathlib import Path

from backends.common import iter_files, read_text


REQ_NAME = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)\s*(.*)$")
EXACT = re.compile(r"^==\s*([0-9][0-9A-Za-z._+-]*)$")


def _requirement(spec: str):
    spec = spec.split(";", 1)[0].strip().strip(",").strip("\"'")
    spec = re.sub(r"\[[^\]]*\]", "", spec).strip()
    match = REQ_NAME.match(spec)
    if not match:
        return None
    name, operator = match.group(1), match.group(2).strip()
    exact = EXACT.fullmatch(operator)
    version = exact.group(1) if exact else None
    return {"name": name, "version": version, "pinned": version is not None, "constraint": operator}


def _join_continuations(text: str) -> list[str]:
    lines, current = [], ""
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.endswith("\\"):
            current += stripped[:-1].strip() + " "
            continue
        current += stripped
        if current:
            lines.append(current.strip())
        current = ""
    if current.strip():
        lines.append(current.strip())
    return lines


def _requirements(path: Path, ecosystem: str = "PyPI") -> list[dict]:
    text = read_text(path)
    if text is None:
        return []
    found = []
    for line in _join_continuations(text):
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        item = _requirement(line.split("--hash", 1)[0].strip())
        if item:
            item.update({"ecosystem": ecosystem, "path": "", "index": "default"})
            found.append(item)
    return found


def _pyproject(text: str) -> tuple[list[dict], set[str]]:
    deps, sources, section, in_array = [], set(), "", False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("[") and line.endswith("]"):
            section = line.strip("[]")
            in_array = False
            continue
        if section == "tool.uv.sources" and "=" in line:
            sources.add(line.split("=", 1)[0].strip().strip("\"'"))
            continue
        if section in {"project", "project.optional-dependencies"} and line.endswith("["):
            in_array = "dependencies" in line or section == "project.optional-dependencies"
            continue
        if in_array and line.startswith("]"):
            in_array = False
            continue
        if not in_array:
            continue
        quoted = line.strip(",").strip()
        if quoted[:1] in {"'", '"'}:
            quoted = quoted[1:-1] if quoted[-1:] in {"'", '"'} else quoted[1:]
        item = _requirement(quoted)
        if item:
            item.update({"ecosystem": "PyPI", "path": "", "index": "default"})
            deps.append(item)
    return deps, sources


def _package_json(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    found = []
    exact_version = re.compile(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z._]+)?")
    for field in ("dependencies", "devDependencies"):
        for name, spec in (data.get(field) or {}).items():
            pinned = isinstance(spec, str) and exact_version.fullmatch(spec) is not None
            found.append({
                "ecosystem": "npm",
                "name": name,
                "version": spec if pinned else None,
                "pinned": pinned,
                "constraint": str(spec),
                "path": "",
                "index": "default",
            })
    return found


def _cargo(text: str) -> list[dict]:
    deps, section = [], ""
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("[") and line.endswith("]"):
            section = line.strip("[]")
            continue
        if section not in {"dependencies", "dev-dependencies"} or "=" not in line or line.startswith("#"):
            continue
        name, value = (part.strip() for part in line.split("=", 1))
        version = None
        if value.startswith("\""):
            version = value.strip("\",")
        else:
            match = re.search(r'version\s*=\s*"([^"]+)"', value)
            if match:
                version = match.group(1)
        pinned = bool(version) and "*" not in version and not version[:1] in {"^", "~", ">", "<"}
        deps.append({
            "ecosystem": "crates.io",
            "name": name,
            "version": version if pinned else None,
            "pinned": pinned,
            "constraint": version or value,
            "path": "",
            "index": "default",
        })
    return deps


def _lock_versions(root: Path, prefixes: list[str]) -> dict[tuple[str, str], str]:
    found = {}
    for path in iter_files(root, prefixes, {".lock", ".json", ".sum"}):
        if path.name.startswith("requirements") and path.suffix == ".lock":
            for item in _requirements(path):
                if item["version"]:
                    found[("PyPI", item["name"].lower().replace("_", "-"))] = item["version"]
        elif path.name == "package-lock.json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for key, meta in (data.get("packages") or {}).items():
                if key.startswith("node_modules/") and isinstance(meta, dict) and meta.get("version"):
                    # Use the FINAL node_modules segment. Nested keys like
                    # node_modules/express/node_modules/content-type must resolve to
                    # content-type, not overwrite express with content-type's version.
                    name = key.rsplit("node_modules/", 1)[-1]
                    if name.startswith("@"):
                        parts = name.split("/")
                        name = "/".join(parts[:2]) if len(parts) >= 2 else name
                    else:
                        name = name.split("/", 1)[0]
                    found[("npm", name)] = meta["version"]
        elif path.name == "Cargo.lock":
            name = version = None
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.strip() == "[[package]]":
                    if name and version:
                        found[("crates.io", name)] = version
                    name = version = None
                elif line.startswith("name = "):
                    name = line.split("=", 1)[1].strip().strip('"')
                elif line.startswith("version = "):
                    version = line.split("=", 1)[1].strip().strip('"')
            if name and version:
                found[("crates.io", name)] = version
        elif path.name == "go.sum":
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                parts = line.split()
                if len(parts) < 2 or parts[0].endswith("/go.mod"):
                    continue
                found[("Go", parts[0])] = parts[1].split("/", 1)[0]
    return found


def discover(root: Path, prefixes: list[str]) -> dict:
    direct, locks = [], _lock_versions(root, prefixes)
    for path in iter_files(root, prefixes):
        rel = path.relative_to(root).as_posix()
        items, sources = [], set()
        if path.name in {"requirements.txt", "requirements-dev.txt"} or (
            path.name.startswith("requirements") and path.suffix == ".txt"
        ):
            items = _requirements(path)
        elif path.name == "pyproject.toml":
            text = read_text(path) or ""
            items, sources = _pyproject(text)
        elif path.name == "package.json":
            items = _package_json(path)
        elif path.name == "Cargo.toml":
            items = _cargo(read_text(path) or "")
        for item in items:
            item["path"] = rel
            if item["name"] in sources:
                item["index"] = "nondefault"
            key = (item["ecosystem"], item["name"].lower().replace("_", "-") if item["ecosystem"] == "PyPI" else item["name"])
            if not item["pinned"] and key in locks:
                item["version"] = locks[key]
                item["pinned"] = True
                item["resolved_by"] = "lock"
            else:
                item["resolved_by"] = "manifest"
            direct.append(item)
    locked = []
    for (ecosystem, name), version in sorted(locks.items()):
        locked.append({"ecosystem": ecosystem, "name": name, "version": version, "pinned": True, "path": "lock"})
    return {"direct": direct, "locked": locked}
