from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class DocumentationSource:
    name: str
    url: str
    authority: str
    type: str


@dataclass(frozen=True)
class DocumentationProfile:
    id: str
    language: str
    version: str
    status: str
    domains: tuple[str, ...]
    sources: tuple[DocumentationSource, ...]
    resolved_version: str | None = None


SOURCE_POLICY = {
    "prefer": ["official documentation", "official API docs", "language specifications", "official release notes"],
    "require": ["source URL", "version label", "authority label", "retrieval timestamp at runtime"],
    "forbid": ["uncited language claims", "community-only breaking-change advice", "long copyrighted excerpts"],
}


PROFILES: dict[str, DocumentationProfile] = {
    "docs-java-11": DocumentationProfile(
        id="docs-java-11",
        language="java",
        version="11",
        status="legacy-lts",
        domains=("docs.oracle.com", "www.oracle.com", "openjdk.org", "jdk.java.net"),
        sources=(
            DocumentationSource("Oracle JDK 11 Documentation", "https://docs.oracle.com/en/java/javase/11/", "official", "documentation"),
            DocumentationSource("Java SE 11 API", "https://docs.oracle.com/en/java/javase/11/docs/api/index.html", "official", "api"),
            DocumentationSource("OpenJDK 11 Project", "https://openjdk.org/projects/jdk/11/", "official", "release"),
        ),
    ),
    "docs-java-17": DocumentationProfile(
        id="docs-java-17",
        language="java",
        version="17",
        status="lts",
        domains=("docs.oracle.com", "www.oracle.com", "openjdk.org", "jdk.java.net"),
        sources=(
            DocumentationSource("Oracle JDK 17 Documentation", "https://docs.oracle.com/en/java/javase/17/", "official", "documentation"),
            DocumentationSource("Java SE 17 API", "https://docs.oracle.com/en/java/javase/17/docs/api/index.html", "official", "api"),
            DocumentationSource("OpenJDK 17 Project", "https://openjdk.org/projects/jdk/17/", "official", "release"),
        ),
    ),
    "docs-java-21": DocumentationProfile(
        id="docs-java-21",
        language="java",
        version="21",
        status="previous-lts",
        domains=("docs.oracle.com", "www.oracle.com", "openjdk.org", "jdk.java.net"),
        sources=(
            DocumentationSource("Oracle JDK 21 Documentation", "https://docs.oracle.com/en/java/javase/21/", "official", "documentation"),
            DocumentationSource("Java SE 21 API", "https://docs.oracle.com/en/java/javase/21/docs/api/index.html", "official", "api"),
            DocumentationSource("OpenJDK 21 Project", "https://openjdk.org/projects/jdk/21/", "official", "release"),
        ),
    ),
    "docs-java-25": DocumentationProfile(
        id="docs-java-25",
        language="java",
        version="25",
        status="current-lts",
        domains=("docs.oracle.com", "www.oracle.com", "openjdk.org", "jdk.java.net"),
        sources=(
            DocumentationSource("Oracle JDK 25 Documentation", "https://docs.oracle.com/en/java/javase/25/", "official", "documentation"),
            DocumentationSource("Java SE 25 API", "https://docs.oracle.com/en/java/javase/25/docs/api/index.html", "official", "api"),
            DocumentationSource("OpenJDK 25 Builds", "https://jdk.java.net/25/", "official", "release"),
        ),
    ),
    "docs-java-26": DocumentationProfile(
        id="docs-java-26",
        language="java",
        version="26",
        status="current-feature-release",
        domains=("docs.oracle.com", "www.oracle.com", "openjdk.org", "jdk.java.net"),
        sources=(
            DocumentationSource("Oracle JDK 26 Documentation", "https://docs.oracle.com/en/java/javase/26/", "official", "documentation"),
            DocumentationSource("OpenJDK JDK 26 GA", "https://jdk.java.net/26/", "official", "release"),
            DocumentationSource("OpenJDK 26 Project", "https://openjdk.org/projects/jdk/26/", "official", "release"),
        ),
    ),
    "docs-python-current": DocumentationProfile(
        id="docs-python-current",
        language="python",
        version="current",
        resolved_version="3.14",
        status="current-stable",
        domains=("docs.python.org", "www.python.org", "pypi.org", "packaging.python.org"),
        sources=(
            DocumentationSource("Python Current Documentation", "https://docs.python.org/3/", "official", "documentation"),
            DocumentationSource("Python Versioned Documentation", "https://www.python.org/doc/versions/", "official", "release"),
            DocumentationSource("Python Packaging User Guide", "https://packaging.python.org/", "official", "packaging"),
        ),
    ),
    "docs-node-current": DocumentationProfile(
        id="docs-node-current",
        language="node",
        version="current",
        resolved_version="26",
        status="current",
        domains=("nodejs.org", "github.com", "api.github.com"),
        sources=(
            DocumentationSource("Node.js Documentation", "https://nodejs.org/api/", "official", "api"),
            DocumentationSource("Node.js Releases", "https://nodejs.org/en/about/previous-releases", "official", "release-policy"),
            DocumentationSource("Node.js Release Blog", "https://nodejs.org/en/blog/release", "official", "release"),
        ),
    ),
    "docs-typescript-current": DocumentationProfile(
        id="docs-typescript-current",
        language="typescript",
        version="current",
        resolved_version="5.9",
        status="current-stable",
        domains=("www.typescriptlang.org", "devblogs.microsoft.com", "github.com", "api.github.com"),
        sources=(
            DocumentationSource("TypeScript Documentation", "https://www.typescriptlang.org/docs/", "official", "documentation"),
            DocumentationSource("TypeScript 5.9 Release Notes", "https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-9.html", "official", "release"),
            DocumentationSource("TypeScript Releases", "https://github.com/microsoft/TypeScript/releases", "official", "release"),
        ),
    ),
    "docs-angular-current": DocumentationProfile(
        id="docs-angular-current",
        language="angular",
        version="current",
        resolved_version="22",
        status="current-stable",
        domains=("angular.dev", "next.angular.dev", "github.com", "api.github.com"),
        sources=(
            DocumentationSource("Angular Documentation", "https://angular.dev/", "official", "documentation"),
            DocumentationSource("Angular Versioning and Releases", "https://angular.dev/reference/releases", "official", "release-policy"),
            DocumentationSource("Angular Releases", "https://github.com/angular/angular/releases", "official", "release"),
        ),
    ),
    "docs-javascript-current": DocumentationProfile(
        id="docs-javascript-current",
        language="javascript",
        version="current",
        resolved_version="ECMAScript current draft",
        status="living-standard-plus-current-snapshot",
        domains=("tc39.es", "ecma-international.org", "developer.mozilla.org", "github.com"),
        sources=(
            DocumentationSource("TC39 ECMA-262 Living Specification", "https://tc39.es/ecma262/", "official", "specification"),
            DocumentationSource("ECMA-262 Standard", "https://ecma-international.org/publications-and-standards/standards/ecma-262/", "official", "specification"),
            DocumentationSource("MDN JavaScript Reference", "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "official-practical", "documentation"),
        ),
    ),
}


def profile_to_dict(profile: DocumentationProfile) -> dict:
    return {
        "id": profile.id,
        "language": profile.language,
        "version": profile.version,
        "resolved_version": profile.resolved_version,
        "status": profile.status,
        "domains": list(profile.domains),
        "sources": [source.__dict__ for source in profile.sources],
    }


def get_profile(profile_id: str) -> DocumentationProfile:
    if profile_id not in PROFILES:
        raise KeyError(f"Unknown documentation profile: {profile_id}")
    return PROFILES[profile_id]


def is_allowed_url(profile: DocumentationProfile, url: str) -> bool:
    host = urlparse(url).hostname or ""
    return any(host == domain or host.endswith("." + domain) for domain in profile.domains)
