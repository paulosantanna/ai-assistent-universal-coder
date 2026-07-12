# AEOS Language Server

Production-grade Language Server Protocol implementation for the AEOS ecosystem.

Provides semantic intelligence about agents, sub-agents, skills, playbooks, policies, permissions, tools, commands, registries, quality gates, evidence, models, token budgets, and configuration of the AEOS engineering environment.

## Features

- **Semantic Model** — Full symbol table, cross-file reference resolution, dependency and inheritance graphs
- **Diagnostics** — 55+ diagnostic rules (AEOS0001–AEOS0055) covering syntax, schema, references, security, and architecture
- **Navigation** — Go to definition, find references, document/workspace symbols, call/type hierarchy
- **Completions** — Context-aware completions for IDs, schemas, expressions, variables, paths, and snippets
- **Refactoring** — Safe rename with prepareRename, code actions for common fixes
- **Indexing** — Persistent SQLite-based incremental index with content-hash caching
- **Security** — Read-only by default, workspace trust, path policy, secret redaction, no eval/exec
- **Multi-root** — Full multi-root workspace support
- **Profiles** — Editor, Agent, and CI diagnostic profiles

## Installation

```bash
pip install aeos-lsp
```

Or from source:

```bash
cd packages/aeos-language-server
pip install -e .
```

## Usage

```bash
# Start LSP server via stdio (default)
aeos-lsp --stdio

# Start via TCP for debugging
aeos-lsp --tcp --host 127.0.0.1 --port 2087

# Validate a workspace
aeos-lsp validate /path/to/workspace

# Index a workspace
aeos-lsp index /path/to/workspace

# Run diagnostics
aeos-lsp diagnostics /path/to/workspace --format json

# System health check
aeos-lsp doctor

# Show capabilities
aeos-lsp capabilities

# Show version
aeos-lsp version
```

## VS Code Extension

The VS Code extension is in `extensions/vscode-aeos/`.

```bash
cd extensions/vscode-aeos
npm install
npm run compile
```

## Architecture

See `docs/lsp/ARCHITECTURE.md` for detailed architecture documentation.

## Protocol Support

LSP 3.17 baseline with all major language features. See `docs/lsp/PROTOCOL_SUPPORT.md`.

## Diagnostic Codes

55+ stable diagnostic codes (AEOS0001–AEOS0055). See `docs/lsp/DIAGNOSTIC_CODES.md`.

## Security Model

Read-only by default with workspace trust, path canonicalization, and secret redaction. See `docs/lsp/SECURITY_MODEL.md`.

## License

MIT
