"""Declared and running language versions must be the current supported release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date

from backends.common import TransportError, finding, finish, is_older, iter_files, read_text, version_key


BACKEND = "language"
PYTHON_VERSION = re.compile(r"python-version:\s*['\"]?(\d+(?:\.\d+){0,2})")
NODE_VERSION = re.compile(r"node-version:\s*['\"]?(\d+(?:\.\d+){0,2})")
REQUIRES_PYTHON = re.compile(r"requires-python\s*=\s*['\"]([^'\"]+)['\"]")
COMPARATOR = re.compile(r"(>=|<=|==|>|<)\s*(\d+(?:\.\d+){0,2})")


def detect_runtime() -> dict:
    runtime = {"python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", "node": None}
    try:
        proc = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return runtime
    if proc.returncode == 0:
        runtime["node"] = proc.stdout.strip().lstrip("v")
    return runtime


def _declarations(root, prefixes: list[str]) -> list[dict]:
    found = []
    for path in iter_files(root, prefixes, {".yml", ".yaml", ".toml", ".json"}):
        text = read_text(path)
        if text is None:
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix in {".yml", ".yaml"}:
            for match in PYTHON_VERSION.finditer(text):
                found.append({"product": "python", "value": match.group(1), "path": rel})
            for match in NODE_VERSION.finditer(text):
                found.append({"product": "node", "value": match.group(1), "path": rel})
        elif path.name == "pyproject.toml":
            match = REQUIRES_PYTHON.search(text)
            if match:
                spec = match.group(1)
                found.append({"product": "python", "value": spec, "path": rel, "range": any(op in spec for op in "><=!~")})
        elif path.name == "package.json":
            try:
                engines = json.loads(text).get("engines") or {}
            except json.JSONDecodeError:
                engines = {}
            if isinstance(engines.get("node"), str):
                spec = engines["node"]
                found.append({"product": "node", "value": spec, "path": rel, "range": any(op in spec for op in "><=!~")})
    return found


def _cycles(feed: list, today: date) -> list[dict]:
    rows = []
    for item in feed:
        cycle = str(item.get("cycle"))
        if not re.fullmatch(r"\d+(?:\.\d+)*", cycle):
            continue
        release = item.get("releaseDate")
        if release and date.fromisoformat(release) > today:
            continue
        eol = item.get("eol")
        ended = eol is True or (isinstance(eol, str) and eol not in {"false", ""} and date.fromisoformat(eol) <= today)
        rows.append({"cycle": cycle, "latest": str(item.get("latest") or cycle), "eol": ended})
    rows.sort(key=lambda row: [int(part) for part in row["cycle"].split(".") if part.isdigit()])
    return rows


def _range_problem(spec: str, current: dict, cycles: list[dict]) -> str | None:
    parts = [match.groups() for match in COMPARATOR.finditer(spec)]
    if not parts:
        return f"restricao nao comparavel {spec}"
    lower = next((number for op, number in parts if op in {">=", ">", "=="}), None)
    if lower is None:
        return f"sem piso em {spec}"
    floor = _cycle_of(lower, cycles)
    if floor is None or floor["eol"] or floor["cycle"] != current["cycle"]:
        return f"{spec} nao exige o ciclo atual {current['cycle']}"
    current_key = version_key(current["cycle"])
    for op, number in parts:
        bound = version_key(number)
        allowed = (
            (op == ">=" and current_key >= bound)
            or (op == ">" and current_key > bound)
            or (op == "==" and current_key == bound)
            or (op == "<=" and current_key <= bound)
            or (op == "<" and current_key < bound)
        )
        if not allowed:
            return f"{spec} exclui o ciclo atual {current['cycle']}"
    return None


def _cycle_of(value: str, cycles: list[dict]) -> dict | None:
    matches = [row for row in cycles if value == row["cycle"] or value.startswith(row["cycle"] + ".")]
    if not matches:
        return None
    return max(matches, key=lambda row: len(row["cycle"]))


def check(root, policy, transport, now, runtime=None):
    runtime = detect_runtime() if runtime is None else runtime
    declarations = _declarations(root, policy["exclude_prefixes"])
    for product, value in runtime.items():
        if value:
            declarations.append({"product": product, "value": value, "path": f"runtime:{product}"})
    findings, feeds, fresh = [], {}, True
    products = sorted({item["product"] for item in declarations})
    try:
        for product in products:
            response = transport.request("GET", policy["endoflife"].format(product=product), timeout=30)
            if response.status != 200:
                fresh = False
                findings.append(finding(BACKEND, "language-feed-unreachable", f"endoflife {product} HTTP {response.status}", subject=product))
                continue
            payload = response.json()
            if isinstance(payload, dict):
                payload = payload.get("result", {}).get("releases") or payload.get("releases") or []
            cycles = _cycles(payload, now.date())
            supported = [row for row in cycles if not row["eol"]]
            if not supported:
                fresh = False
                findings.append(finding(BACKEND, "language-feed-empty", f"endoflife {product} sem ciclo suportado", subject=product))
                continue
            current = supported[-1]
            feeds[product] = {"current": current["cycle"], "latest": current["latest"]}
            for item in declarations:
                if item["product"] != product:
                    continue
                if item.get("range"):
                    problem = _range_problem(item["value"], current, cycles)
                    if problem:
                        findings.append(finding(BACKEND, "language-outdated", f"{product} {problem}", item["path"], product))
                    continue
                row = _cycle_of(item["value"], cycles)
                if row is None or row["eol"] or row["cycle"] != current["cycle"]:
                    findings.append(finding(
                        BACKEND,
                        "language-outdated",
                        f"{product} {item['value']} nao e o ciclo atual {current['cycle']} ({current['latest']})",
                        item["path"],
                        product,
                    ))
                elif item["value"] != row["cycle"] and is_older(item["value"], row["latest"]):
                    findings.append(finding(
                        BACKEND,
                        "language-patch-outdated",
                        f"{product} {item['value']} esta atras do patch {row['latest']}",
                        item["path"],
                        product,
                    ))
    except (TransportError, ValueError, KeyError) as exc:
        fresh = False
        findings.append(finding(BACKEND, "language-refresh-failed", f"nao foi possivel atualizar o ciclo de vida: {exc}", subject="endoflife.date"))
    return finish(BACKEND, policy["endoflife"], ",".join(f"{key}:{value['latest']}" for key, value in feeds.items()), now, findings, {"feeds": feeds}, fresh)
