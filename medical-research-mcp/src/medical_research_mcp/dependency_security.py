from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib
from typing import Any
import xml.etree.ElementTree as ET

import httpx


OSV_QUERY_BATCH = "https://api.osv.dev/v1/querybatch"
CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_API = "https://api.first.org/data/v1/epss"


def inventory_dependencies(repository: str) -> list[dict[str, Any]]:
    root = Path(repository).resolve()
    dependencies: list[dict[str, Any]] = []

    for req in root.rglob("requirements*.txt"):
        for raw in req.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            match = re.match(r"([A-Za-z0-9_.-]+)\s*(?:==|~=|>=|<=|>|<)?\s*([^;\s]+)?", line)
            if match:
                dependencies.append({
                    "ecosystem": "PyPI",
                    "name": match.group(1),
                    "version": match.group(2),
                    "source": str(req.relative_to(root)),
                })

    for pyproject in root.rglob("pyproject.toml"):
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            continue
        project = data.get("project", {})
        for item in project.get("dependencies", []):
            match = re.match(r"([A-Za-z0-9_.-]+).*?([0-9][^,;\s]*)?", item)
            if match:
                dependencies.append({
                    "ecosystem": "PyPI",
                    "name": match.group(1),
                    "version": match.group(2),
                    "source": str(pyproject.relative_to(root)),
                })

    for package_json in root.rglob("package.json"):
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for group in ("dependencies", "devDependencies", "optionalDependencies"):
            for name, version in data.get(group, {}).items():
                dependencies.append({
                    "ecosystem": "npm",
                    "name": name,
                    "version": version.lstrip("^~>=< "),
                    "source": str(package_json.relative_to(root)),
                })

    for pom in root.rglob("pom.xml"):
        try:
            tree = ET.parse(pom)
        except (OSError, ET.ParseError):
            continue
        root_element = tree.getroot()
        namespace = ""
        if root_element.tag.startswith("{"):
            namespace = root_element.tag.split("}")[0] + "}"
        for dep in root_element.findall(f".//{namespace}dependency"):
            group = dep.findtext(f"{namespace}groupId")
            artifact = dep.findtext(f"{namespace}artifactId")
            version = dep.findtext(f"{namespace}version")
            if group and artifact:
                dependencies.append({
                    "ecosystem": "Maven",
                    "name": f"{group}:{artifact}",
                    "version": version,
                    "source": str(pom.relative_to(root)),
                })

    unique: dict[tuple[str, str, str | None, str], dict[str, Any]] = {}
    for item in dependencies:
        key = (item["ecosystem"], item["name"], item.get("version"), item["source"])
        unique[key] = item
    return list(unique.values())


async def query_osv(dependencies: list[dict[str, Any]]) -> dict[str, Any]:
    queries = []
    accepted_indexes = []
    for index, dependency in enumerate(dependencies):
        version = dependency.get("version")
        if not version or any(char in version for char in "$[{("):
            continue
        queries.append({
            "package": {
                "ecosystem": dependency["ecosystem"],
                "name": dependency["name"],
            },
            "version": version,
        })
        accepted_indexes.append(index)

    if not queries:
        return {"results": [], "skipped": len(dependencies)}

    async with httpx.AsyncClient(timeout=45.0) as client:
        response = await client.post(OSV_QUERY_BATCH, json={"queries": queries})
        response.raise_for_status()
        payload = response.json()

    enriched = []
    for dependency_index, result in zip(accepted_indexes, payload.get("results", []), strict=False):
        enriched.append({
            "dependency": dependencies[dependency_index],
            "vulnerabilities": result.get("vulns", []),
        })
    return {"results": enriched, "skipped": len(dependencies) - len(queries)}


async def fetch_cisa_kev() -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=45.0, follow_redirects=True) as client:
        response = await client.get(CISA_KEV_URL)
        response.raise_for_status()
        return response.json()


async def fetch_epss(cves: list[str]) -> dict[str, Any]:
    if not cves:
        return {"data": []}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(EPSS_API, params={"cve": ",".join(cves[:100])})
        response.raise_for_status()
        return response.json()


def vulnerability_source_policy() -> dict[str, str]:
    return {
        "OSV": "ecosystem and version-aware open-source vulnerability matching",
        "GitHub Advisory Database": "GHSA and ecosystem advisories; token may be required for API workflows",
        "NVD": "CVE and CVSS enrichment; API key recommended for sustained usage",
        "CISA KEV": "evidence of known exploitation in the wild",
        "FIRST EPSS": "probability-oriented exploitation signal",
        "vendor advisories": "primary platform and product-specific remediation guidance",
        "SBOM": "inventory and reachability context; not a vulnerability source by itself",
    }
