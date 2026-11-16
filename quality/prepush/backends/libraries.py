"""Direct libraries must resolve to the current registry release."""

from __future__ import annotations

from urllib.parse import quote

from backends.common import TransportError, finding, finish, is_older
from backends.manifests import discover


BACKEND = "libraries"


def _latest(transport, policy, item) -> str:
    template = policy["registries"][item["ecosystem"]]
    name = item["name"]
    if item["ecosystem"] == "npm":
        name = quote(name, safe="@")
    elif item["ecosystem"] == "Go":
        name = quote(name, safe="")
    response = transport.request("GET", template.format(name=name), timeout=30)
    if response.status != 200:
        raise TransportError(f"HTTP {response.status} para {item['name']}")
    payload = response.json()
    if item["ecosystem"] == "PyPI":
        version = payload["info"]["version"]
    elif item["ecosystem"] == "npm":
        version = payload["version"]
    elif item["ecosystem"] == "crates.io":
        version = payload["crate"].get("max_stable_version") or payload["crate"]["newest_version"]
    else:
        version = payload["Version"]
    if not version:
        raise TransportError(f"registro sem versao para {item['name']}")
    return str(version)


def check(root, policy, transport, now, manifests=None):
    manifests = manifests if manifests is not None else discover(root, policy["exclude_prefixes"])
    findings = []
    checked = []
    fresh = True
    try:
        for item in manifests["direct"]:
            subject = f"{item['ecosystem']}:{item['name']}"
            if item.get("index") == "nondefault":
                findings.append(finding(
                    BACKEND,
                    "library-nondefault-index",
                    f"{item['name']} nao usa o registro publico; a versao atual nao foi provada",
                    item["path"],
                    subject,
                ))
                continue
            if not item.get("pinned") or not item.get("version"):
                findings.append(finding(
                    BACKEND,
                    "library-unpinned",
                    f"{item['name']} sem versao exata ({item.get('constraint') or 'sem restricao'})",
                    item["path"],
                    subject,
                ))
                continue
            if item["ecosystem"] not in policy["registries"]:
                fresh = False
                findings.append(finding(BACKEND, "library-registry-unknown", f"sem registro para {item['ecosystem']}", item["path"], subject))
                continue
            try:
                latest = _latest(transport, policy, item)
            except TransportError as exc:
                if str(exc).startswith("HTTP"):
                    findings.append(finding(BACKEND, "library-unknown", f"{item['name']} nao encontrado no registro ({exc})", item["path"], subject))
                    continue
                fresh = False
                findings.append(finding(BACKEND, "library-refresh-failed", f"nao foi possivel atualizar o registro: {exc}", item["path"], subject))
                break
            checked.append({"name": item["name"], "version": item["version"], "latest": latest, "path": item["path"]})
            if is_older(item["version"], latest):
                findings.append(finding(
                    BACKEND,
                    "library-outdated",
                    f"{item['name']} {item['version']} esta atras de {latest}",
                    item["path"],
                    subject,
                ))
    except (ValueError, KeyError) as exc:
        fresh = False
        findings.append(finding(BACKEND, "library-refresh-failed", f"nao foi possivel atualizar o registro: {exc}", subject="registry"))
    return finish(BACKEND, "registries", str(len(checked)), now, findings, {"checked": checked}, fresh)
