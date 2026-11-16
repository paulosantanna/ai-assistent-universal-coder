"""Static security gate: secrets and workflow trust. It does not attack a running system."""

from __future__ import annotations

import re

from backends.common import TransportError, finding, finish, iter_files, load_json, read_text


BACKEND = "security"
ACTION = re.compile(r"uses:\s*(\S+)")
SHA = re.compile(r"^[0-9a-f]{40}$")


def _action_pin(value: str, rel: str, findings: list):
    token = value.split("#", 1)[0].strip().strip("\"'")
    if token.startswith("./") or token.startswith("docker://"):
        return
    if "@" not in token:
        findings.append(finding(BACKEND, "action-unpinned", f"{rel} usa {token} sem revisao fixa", rel, token))
        return
    revision = token.rsplit("@", 1)[1]
    if not SHA.fullmatch(revision):
        findings.append(finding(BACKEND, "action-unpinned", f"{rel} usa {token}; a revisao precisa ser o commit completo", rel, token))


def check(root, policy, transport, now, catalog_path=None):
    catalog_path = catalog_path or root
    path = catalog_path if getattr(catalog_path, "name", "") == "security.json" else catalog_path / "catalogs" / "security.json"
    catalog = load_json(path)
    findings = []
    fresh = True
    observed = ""
    try:
        response = transport.request("GET", catalog["upstream"], timeout=30)
        if response.status != 200:
            fresh = False
            findings.append(finding(BACKEND, "security-upstream-unreachable", f"gitleaks HTTP {response.status}", subject="gitleaks"))
        else:
            observed = response.json().get("tag_name") or ""
            if not observed:
                fresh = False
                findings.append(finding(BACKEND, "security-upstream-undated", "gitleaks nao informou a versao", subject="gitleaks"))
            elif observed != catalog.get("aligned_upstream"):
                findings.append(finding(
                    BACKEND,
                    "security-catalog-behind-upstream",
                    f"regras de segredo revisadas em {catalog.get('aligned_upstream')} e o gitleaks atual e {observed}",
                    "quality/prepush/catalogs/security.json",
                    "gitleaks",
                ))
    except (TransportError, ValueError, KeyError) as exc:
        fresh = False
        findings.append(finding(BACKEND, "security-refresh-failed", f"nao foi possivel atualizar a seguranca: {exc}", subject="gitleaks"))
    secret = re.compile(catalog["secret_pattern"].encode("utf-8"))
    names = set(catalog.get("credential_names") or [])
    for file_path in iter_files(root, policy["exclude_prefixes"]):
        rel = file_path.relative_to(root).as_posix()
        if file_path.name in names:
            findings.append(finding(BACKEND, "credential-artifact", f"{rel} e um arquivo de credencial", rel, file_path.name))
        if file_path.suffix.lower() in {".yml", ".yaml"} and ".github/workflows/" in rel:
            text = read_text(file_path) or ""
            if "pull_request_target" in text:
                findings.append(finding(BACKEND, "workflow-pull-request-target", f"{rel} usa pull_request_target", rel, rel))
            if re.search(r"permissions:\s*write-all", text):
                findings.append(finding(BACKEND, "workflow-write-all", f"{rel} concede write-all", rel, rel))
            for match in ACTION.finditer(text):
                _action_pin(match.group(1), rel, findings)
        try:
            if file_path.stat().st_size > 1_000_000:
                continue
            data = file_path.read_bytes()
        except OSError:
            continue
        if secret.search(data):
            findings.append(finding(BACKEND, "possible-secret", f"{rel} contem um padrao de segredo", rel, file_path.name))
    return finish(BACKEND, catalog.get("upstream", ""), observed or catalog.get("aligned_upstream", ""), now, findings, {
        "catalog_version": catalog.get("version"),
        "aligned_upstream": catalog.get("aligned_upstream"),
        "observed_upstream": observed,
        "mode": "static-security",
    }, fresh)
