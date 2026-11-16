# Capability CI

Updated: 2026-11-13
Entry point: quality/README.md; .github/workflows/aeos-enterprise-ci.template.yml

- Gate source: quality/validate.py + existing skill-factory/skill-architect. Baseline and reviews are package hashes, not enterprise effectiveness scores.
- Source authority: quality/tlc-upstream.json; official current control hashes checked on every maintenance run. Unknown rule change/network error blocks publication.
- Control drift runbook: on `Unsupported TLC rule change: <path>`, diff that file from the locked commit to upstream main. Recognize the new hash in quality/tlc-upstream.json only if no local gate consumes the changed text; otherwise adapt the gate first. Verify with unit tests, a live `quality/upstream.py` dry run and `quality/validate.py --runtime`. Evidence: PR #56 (`27ceb253`) recognized CONTRIBUTING.md at upstream `e74dc8a7`.
- Automatic update explicitly chosen by user: new TLC packages and untouched auto-imports; preserve curated adaptations. Read-only candidate job, bounded artifact, separate publisher, normal master push; no runtime installation.
- MCP inventory: quality/capabilities.json. KingHost control is a custom envelope adapter with real offline self-test; other three legacy packages quarantined. No local LSP installed. Active additions require contract/protocol handshake; quarantine is not protocol PASS.
- Portability: textual SHA uses UTF-8/LF, binary SHA exact; acquired_sha256 retains historical CRLF acquisition hashes. Gate passes Windows and exact Git export before remote claim.
- Evidence: .aeos/quality/ reports locally and GitHub workflow artifacts; tests in quality/tests/test_gates.py. Local baseline441 export hash errors demonstrated why old Windows-only acceptance was insufficient.
