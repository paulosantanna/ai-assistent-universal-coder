from language_docs_mcp.profiles import PROFILES, get_profile, is_allowed_url
from language_docs_mcp.server import lookup_symbol, migration_delta, search_profile, version_status


def test_profiles_include_requested_language_docs():
    expected = {
        "docs-java-11",
        "docs-java-17",
        "docs-java-21",
        "docs-java-25",
        "docs-java-26",
        "docs-python-current",
        "docs-node-current",
        "docs-typescript-current",
        "docs-angular-current",
        "docs-javascript-current",
    }
    assert expected.issubset(PROFILES)


def test_search_returns_evidence_refs():
    result = search_profile("docs-java-21", "api", max_results=3)
    assert result["status"] == "PASS"
    assert result["evidence_refs"]


def test_version_status_is_read_only_profile_data():
    result = version_status("docs-python-current")
    assert result["profile"]["language"] == "python"
    assert result["evidence_refs"]


def test_lookup_symbol_preserves_profile_context():
    result = lookup_symbol("docs-typescript-current", "import defer")
    assert result["profile"]["language"] == "typescript"
    assert result["symbol"] == "import defer"


def test_migration_delta_compares_java_profiles():
    result = migration_delta("docs-java-26", "21", "26", "virtual threads")
    assert result["language"] == "java"
    assert result["evidence_refs"]


def test_allowed_url_uses_profile_domains():
    profile = get_profile("docs-angular-current")
    assert is_allowed_url(profile, "https://angular.dev/reference/releases")
    assert not is_allowed_url(profile, "https://example.com/reference/releases")
