from __future__ import annotations

import argparse
import re
import urllib.request

from .profiles import PROFILES, SOURCE_POLICY, get_profile, is_allowed_url, profile_to_dict


def search_profile(profile_id: str, query: str, max_results: int = 5) -> dict:
    profile = get_profile(profile_id)
    query_l = query.lower().strip()
    ranked = []
    for source in profile.sources:
        haystack = " ".join([source.name, source.url, source.type, source.authority]).lower()
        score = sum(1 for term in query_l.split() if term in haystack)
        if score or not query_l:
            ranked.append((score, source))
    ranked.sort(key=lambda item: (-item[0], item[1].name))
    results = [source.__dict__ | {"evidence_ref": source.url} for _, source in ranked[:max_results]]
    return {
        "status": "PASS" if results else "REVIEW",
        "profile": profile_to_dict(profile),
        "query": query,
        "results": results,
        "evidence_refs": [item["url"] for item in results],
        "blocking_conditions": [] if results else ["No governed source matched the query"],
    }


def version_status(profile_id: str) -> dict:
    profile = get_profile(profile_id)
    return {
        "status": "PASS",
        "profile": profile_to_dict(profile),
        "source_policy": SOURCE_POLICY,
        "evidence_refs": [source.url for source in profile.sources],
    }


def lookup_symbol(profile_id: str, symbol: str, scope: str = "") -> dict:
    profile = get_profile(profile_id)
    query = " ".join(part for part in [symbol, scope] if part)
    result = search_profile(profile_id, query, max_results=5)
    result["symbol"] = symbol
    result["scope"] = scope
    result["lookup_strategy"] = "Search governed API/docs sources, then fetch the exact official page before claiming behavior."
    result["profile"] = profile_to_dict(profile)
    return result


def migration_delta(profile_id: str, source_version: str, target_version: str, topic: str = "") -> dict:
    active = get_profile(profile_id)
    source_profiles = [p for p in PROFILES.values() if p.language == active.language and p.version == source_version]
    target_profiles = [p for p in PROFILES.values() if p.language == active.language and p.version == target_version]
    refs = []
    for profile in [*source_profiles, *target_profiles] or [active]:
        refs.extend(source.url for source in profile.sources)
    return {
        "status": "PASS" if refs else "REVIEW",
        "language": active.language,
        "source_version": source_version,
        "target_version": target_version,
        "topic": topic,
        "migration_notes": [
            "Compare source and target API docs before proposing code changes.",
            "Use release notes and migration guides for deprecations, removals and behavior changes.",
            "Mark undocumented or implementation-specific recommendations as REVIEW.",
        ],
        "evidence_refs": refs,
        "blocking_conditions": [] if refs else ["No governed source/target profile evidence found"],
    }


def fetch_page(profile_id: str, url: str, max_bytes: int = 12000) -> dict:
    profile = get_profile(profile_id)
    if not is_allowed_url(profile, url):
        return {"status": "BLOCKED", "url": url, "blocking_conditions": ["URL outside allowed source domains"]}
    with urllib.request.urlopen(url, timeout=10) as response:
        raw = response.read(max_bytes)
    text = raw.decode("utf-8", errors="replace")
    text = re.sub(r"<script\\b.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style\\b.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\\s+", " ", text).strip()
    return {
        "status": "PASS",
        "url": url,
        "truncated": len(raw) >= max_bytes,
        "content": text[:max_bytes],
        "evidence_refs": [url],
        "blocking_conditions": [],
    }


def build_mcp(profile_id: str):
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP(f"AEOS Language Docs MCP ({profile_id})")

    @mcp.tool()
    def language_docs_search(query: str, max_results: int = 5) -> dict:
        return search_profile(profile_id, query, max_results)

    @mcp.tool()
    def language_docs_fetch(url: str, max_bytes: int = 12000) -> dict:
        return fetch_page(profile_id, url, max_bytes)

    @mcp.tool()
    def language_docs_lookup_symbol(symbol: str, scope: str = "") -> dict:
        return lookup_symbol(profile_id, symbol, scope)

    @mcp.tool()
    def language_docs_version_status() -> dict:
        return version_status(profile_id)

    @mcp.tool()
    def language_docs_migration_delta(source_version: str, target_version: str, topic: str = "") -> dict:
        return migration_delta(profile_id, source_version, target_version, topic)

    @mcp.tool()
    def language_docs_source_policy() -> dict:
        return {"status": "PASS", "source_policy": SOURCE_POLICY, "profile": profile_to_dict(get_profile(profile_id))}

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="AEOS governed language documentation MCP")
    parser.add_argument("--profile", required=True, choices=sorted(PROFILES))
    args = parser.parse_args()
    build_mcp(args.profile).run(transport="stdio")


if __name__ == "__main__":
    main()
