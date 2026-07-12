# Changelog

## 1.0.0 (2026-07-11)

### Initial Release

- LSP 3.17 baseline with full lifecycle, text sync, and cancellation support
- 26 language features: completion, hover, definition, declaration, implementation, references, document highlight, document symbols, workspace symbols, prepare rename, rename, code actions, code lens, semantic tokens, folding, selection range, formatting, range formatting, document links, inlay hints, signature help, call hierarchy, type hierarchy
- 55+ diagnostic rules (AEOS0001–AEOS0055) covering all AEOS artifact types
- Persistent SQLite-based incremental index with content-hash caching
- Multi-root workspace support
- Read-only security model with workspace trust, path policy, command policy, secret redaction
- Editor/Agent/CI diagnostic profiles for token economy
- VS Code extension with TextMate grammars, snippets, and full command integration
- JSON Schemas for all AEOS artifact types (agent, skill, playbook, policy, permissions, registry, model profile, token budget, evidence, judge)
- CLI modes: stdio, TCP, validate, index, diagnostics, doctor, capabilities, version
- OpenCode integration configuration
- Comprehensive test suite: unit, integration, protocol, feature, performance, golden, security
- Support for Markdown (with front matter), YAML, JSON/JSONC, TOML, and AEOS expression documents
- Formal grammar for AEOS expressions with recursive descent parser
- Cross-platform: Windows, Linux, macOS
