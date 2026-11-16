"""Static rules plus a live check that the rule review matches current semgrep-rules."""

from __future__ import annotations

import re

from backends.common import TransportError, finding, finish, iter_files, load_json, read_text


BACKEND = "sast"


def check(root, policy, transport, now, catalog_path=None):
    catalog_path = catalog_path or root
    path = catalog_path if catalog_path.name == "sast.json" else catalog_path / "catalogs" / "sast.json"
    if not path.exists():
        path = catalog_path
    catalog = load_json(path)
    findings = []
    fresh = True
    observed = ""
    try:
        response = transport.request("GET", catalog["upstream"], timeout=30)
        if response.status != 200:
            fresh = False
            findings.append(finding(BACKEND, "sast-upstream-unreachable", f"semgrep-rules HTTP {response.status}", subject="semgrep-rules"))
        else:
            payload = response.json()
            observed = payload.get("sha") or ""
            if not observed:
                fresh = False
                findings.append(finding(BACKEND, "sast-upstream-undated", "semgrep-rules nao informou o commit", subject="semgrep-rules"))
            elif observed != catalog.get("aligned_upstream"):
                findings.append(finding(
                    BACKEND,
                    "sast-catalog-behind-upstream",
                    f"regras SAST revisadas em {catalog.get('aligned_upstream', '')[:12]} e o upstream esta em {observed[:12]}",
                    "quality/prepush/catalogs/sast.json",
                    "semgrep-rules",
                ))
    except (TransportError, ValueError, KeyError) as exc:
        fresh = False
        findings.append(finding(BACKEND, "sast-refresh-failed", f"nao foi possivel atualizar o SAST: {exc}", subject="semgrep-rules"))
    extensions = {ext for rule in catalog.get("rules") or [] for ext in rule.get("extensions") or []}
    compiled = []
    for rule in catalog.get("rules") or []:
        compiled.append((rule, re.compile(rule["pattern"])))
    hits = 0
    for file_path in iter_files(root, policy["exclude_prefixes"], extensions):
        text = read_text(file_path)
        if text is None:
            continue
        rel = file_path.relative_to(root).as_posix()
        for rule, pattern in compiled:
            if file_path.suffix.lower() not in set(rule.get("extensions") or []):
                continue
            for number, line in enumerate(text.splitlines(), 1):
                if not pattern.search(line):
                    continue
                if any(token in line for token in rule.get("unless") or []):
                    continue
                hits += 1
                findings.append(finding(
                    BACKEND,
                    rule["id"],
                    f"{rel}:{number} {rule['message']}",
                    rel,
                    rule["id"],
                ))
                if hits >= 200:
                    break
            if hits >= 200:
                break
        if hits >= 200:
            break
    return finish(BACKEND, catalog.get("upstream", ""), observed or catalog.get("aligned_upstream", ""), now, findings, {
        "catalog_version": catalog.get("version"),
        "aligned_upstream": catalog.get("aligned_upstream"),
        "observed_upstream": observed,
        "hits": hits,
    }, fresh)
