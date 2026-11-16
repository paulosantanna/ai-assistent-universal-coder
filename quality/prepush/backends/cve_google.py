"""Google OSV advisory gate. A stale export or a failed query blocks the push."""

from __future__ import annotations

from datetime import timedelta

from backends.common import TransportError, finding, finish, parse_http_date
from backends.manifests import discover


BACKEND = "cve_google"


def _queries(packages: list[dict]) -> list[dict]:
    seen, queries = set(), []
    for item in packages:
        if not item.get("version"):
            continue
        key = (item["ecosystem"], item["name"].lower(), item["version"])
        if key in seen:
            continue
        seen.add(key)
        queries.append({
            "version": item["version"],
            "package": {"name": item["name"], "ecosystem": item["ecosystem"]},
        })
    return queries


def check(root, policy, transport, now, manifests=None):
    manifests = manifests if manifests is not None else discover(root, policy["exclude_prefixes"])
    packages = list(manifests["direct"]) + list(manifests["locked"])
    ecosystems = sorted({item["ecosystem"] for item in packages if item.get("version")} or {"PyPI"})
    exports = []
    fresh = True
    findings = []
    queries = []
    vulnerabilities = 0
    try:
        for ecosystem in ecosystems:
            url = policy["osv_exports"][ecosystem]
            response = transport.request("HEAD", url, timeout=30)
            modified = parse_http_date(response.header("last-modified"))
            exports.append({"ecosystem": ecosystem, "status": response.status, "last_modified": response.header("last-modified")})
            if response.status != 200 or modified is None:
                fresh = False
                findings.append(finding(BACKEND, "cve-export-unreachable", f"export OSV {ecosystem} sem data confiavel", subject=ecosystem))
            elif now - modified > timedelta(hours=policy["cve_export_max_age_hours"]):
                fresh = False
                findings.append(finding(
                    BACKEND,
                    "cve-export-stale",
                    f"export OSV {ecosystem} de {modified.date()} passou de {policy['cve_export_max_age_hours']}h",
                    subject=ecosystem,
                ))
        queries = _queries(packages)
        for start in range(0, len(queries), 100):
            chunk = queries[start:start + 100]
            response = transport.request("POST", policy["osv_query"], {"queries": chunk}, timeout=60)
            if response.status != 200:
                fresh = False
                findings.append(finding(BACKEND, "cve-query-failed", f"OSV respondeu HTTP {response.status}", subject="osv.dev"))
                break
            results = response.json().get("results")
            if not isinstance(results, list) or len(results) != len(chunk):
                fresh = False
                findings.append(finding(BACKEND, "cve-response-incomplete", "resposta OSV incompleta", subject="osv.dev"))
                break
            for query, result in zip(chunk, results):
                for vuln in result.get("vulns") or []:
                    if vuln.get("withdrawn"):
                        continue
                    vulnerabilities += 1
                    aliases = [item for item in vuln.get("aliases") or [] if item.startswith("CVE-")]
                    identifier = aliases[0] if aliases else vuln.get("id", "OSV")
                    name = query["package"]["name"]
                    findings.append(finding(
                        BACKEND,
                        "cve-found",
                        f"{identifier} em {name}=={query['version']}",
                        subject=f"{query['package']['ecosystem']}:{name}@{query['version']}",
                    ))
    except (TransportError, ValueError, KeyError) as exc:
        fresh = False
        findings.append(finding(BACKEND, "cve-refresh-failed", f"nao foi possivel atualizar a OSV: {exc}", subject="osv.dev"))
    version = ",".join(item.get("last_modified") or "?" for item in exports) or "unavailable"
    return finish(BACKEND, policy["osv_query"], version, now, findings, {
        "exports": exports,
        "query_count": len(queries),
        "vulnerabilities": vulnerabilities,
    }, fresh)
