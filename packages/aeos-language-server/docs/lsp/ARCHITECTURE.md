# AEOS Language Server — Architecture

## Overview

The AEOS Language Server (aeos-ls) provides intelligent editing support for AEOS workspace configuration files — agent definitions, skill definitions, playbooks, policies, permissions, registries, model profiles, token budgets, evidence configurations, and judge configurations.

It implements the Language Server Protocol (LSP) 3.17, delivering diagnostics, completions, hover documentation, go-to-definition, and schema validation powered by JSON Schema Draft 2020-12.

The server runs as a daemon process, communicating with editors over stdio (or optional TCP). It is built in TypeScript and designed for low latency, workspace-scale indexing, and strict security compliance.

## Architecture Principles

1. **Read-only by default** — The server never writes files. All mutation flows through explicit LSP `workspace/applyEdit` or code actions that produce edits for the client to apply.
2. **Schema-driven validation** — All AEOS artifact types are validated against published JSON Schemas. Diagnostics are derived from schema violations plus custom semantic rules.
3. **Workspace-scale indexing** — On initialization, the server indexes the entire workspace, building an in-memory graph of agents, skills, playbooks, and their relationships. Incremental updates handle file changes.
4. **Fail-closed security** — If a workspace cannot be verified as trusted, diagnostics surface warnings and certain features are disabled. Path and command policies are enforced server-side.
5. **Deterministic first, AI-augmented second** — Core features (validation, completions, navigation) are deterministic. AI-powered features (intelligent completions, diagnostics) are opt-in and layered on top.
6. **Extensibility via plugins** — Custom lint rules, schema validators, and completion providers can be registered through a plugin API.

## Component Diagram

```
+--------------------------------------------------------------------+
|                        EDITOR / CLIENT                              |
|  (VS Code, Neovim, Emacs, Helix, etc.)                             |
+--------------------------------------------------------------------+
         |  LSP (stdio/TCP)  |  JSON-RPC 2.0
         v                   v
+--------------------------------------------------------------------+
|                     AEOS LANGUAGE SERVER                            |
|                                                                     |
|  +------------------+  +------------------+  +------------------+  |
|  |  LSP Protocol    |  |  JSON-RPC        |  |  Transport       |  |
|  |  Handler         |  |  Dispatcher      |  |  Layer (stdio)   |  |
|  +--------+---------+  +--------+---------+  +--------+---------+  |
|           |                      |                      |           |
|           v                      v                      v           |
|  +------------------------------------------------------------+    |
|  |                  FEATURE CONTROLLER                         |    |
|  |  +------------+ +-----------+ +----------+ +------------+  |    |
|  |  |Diagnostics | |Completion | | Hover    | |Definition  |  |    |
|  |  |Provider    | |Provider   | |Provider  | |Provider    |  |    |
|  |  +-----+------+ +-----+-----+ +----+-----+ +-----+------+  |    |
|  +--------+--------------+-------------+-------------+---------+    |
|           |              |             |             |              |
|           v              v             v             v              |
|  +------------------------------------------------------------+    |
|  |                  DOCUMENT MODEL                             |    |
|  |  +------------+ +-----------+ +----------+ +------------+  |    |
|  |  | Agent      | | Skill     | | Playbook | | Policy     |  |    |
|  |  | Document   | | Document  | | Document | | Document   |  |    |
|  |  +------------+ +-----------+ +----------+ +------------+  |    |
|  |  +------------+ +-----------+ +----------+ +------------+  |    |
|  |  | Permission | | Registry  | | Profile  | | Budget     |  |    |
|  |  | Document   | | Document  | | Document | | Document   |  |    |
|  |  +------------+ +-----------+ +----------+ +------------+  |    |
|  |  +------------+ +-----------+                              |    |
|  |  | Evidence   | | Judge    |                              |    |
|  |  | Document   | | Document |                              |    |
|  |  +------------+ +-----------+                              |    |
|  +---------------------------+--------------------------------+    |
|                              |                                      |
|                              v                                      |
|  +------------------------------------------------------------+    |
|  |                  WORKSPACE INDEX                            |    |
|  |  +------------+ +-----------+ +----------+ +------------+  |    |
|  |  | File       | | Graph     | | Schema   | | Cache      |  |    |
|  |  | Watcher    | | Resolver  | | Registry | | Layer      |  |    |
|  |  +------------+ +-----------+ +----------+ +------------+  |    |
|  +---------------------------+--------------------------------+    |
|                              |                                      |
|                              v                                      |
|  +------------------------------------------------------------+    |
|  |                  VALIDATION ENGINE                          |    |
|  |  +------------------+ +------------------+                 |    |
|  |  | JSON Schema      | | Semantic Rules   |                 |    |
|  |  | Validator        | | Engine           |                 |    |
|  |  +------------------+ +------------------+                 |    |
|  +---------------------------+--------------------------------+    |
|                              |                                      |
|                              v                                      |
|  +------------------------------------------------------------+    |
|  |                  SECURITY LAYER                             |    |
|  |  +------------+ +-----------+ +----------+ +------------+  |    |
|  |  | Workspace  | | Path     | | Command  | | Secret     |  |    |
|  |  | Trust      | | Policy   | | Policy   | | Redaction  |  |    |
|  |  +------------+ +-----------+ +----------+ +------------+  |    |
|  +------------------------------------------------------------+    |
+--------------------------------------------------------------------+
```

## Module Dependency Graph

```
aeos-language-server/
  src/
    server.ts                    # Entry point: LSP server setup
    transport/
      stdio-transport.ts         # stdio transport layer
      tcp-transport.ts           # Optional TCP transport
    protocol/
      handler.ts                 # LSP method dispatcher
      capabilities.ts            # Server capabilities negotiation
      lifecycle.ts               # initialize, initialized, shutdown, exit
    documents/
      document-manager.ts        # Manages open documents (textDocument/didOpen, didChange, didClose)
      document.ts                # Base document model
      agent-document.ts          # Agent file parser & model
      skill-document.ts          # Skill file parser & model
      playbook-document.ts       # Playbook file parser & model
      policy-document.ts         # Policy file parser & model
      permissions-document.ts    # Permissions file parser & model
      registry-document.ts       # Registry file parser & model
      profile-document.ts        # Model profile file parser & model
      budget-document.ts         # Token budget file parser & model
      evidence-document.ts       # Evidence config file parser & model
      judge-document.ts          # Judge config file parser & model
    indexer/
      workspace-index.ts         # Full workspace index builder
      file-watcher.ts            # File system change watcher
      graph-resolver.ts          # Resolve cross-references ($id, stable_id)
      cache.ts                   # LRU cache for parsed documents
    validation/
      schema-registry.ts         # Loads and caches JSON Schemas
      schema-validator.ts        # Validates documents against schemas
      semantic-rules.ts          # Custom semantic validation rules
      diagnostics.ts             # Diagnostic generation
      codes.ts                   # Diagnostic code definitions
    features/
      completions/
        completion-provider.ts   # Base completion provider
        schema-completions.ts    # Schema-driven completions
        reference-completions.ts # $id / stable_id reference completions
        snippet-completions.ts   # Snippet completions
      hover/
        hover-provider.ts        # Hover content provider
      definition/
        definition-provider.ts   # Go-to-definition provider
      references/
        references-provider.ts   # Find references provider
      folding/
        folding-provider.ts      # Folding range provider
      symbols/
        symbols-provider.ts      # Document/workspace symbols provider
      code-actions/
        code-action-provider.ts  # Code action provider (quick fixes)
      formatting/
        formatting-provider.ts   # Document formatting provider
    security/
      workspace-trust.ts         # Workspace trust verification
      path-policy.ts             # Allowed/denied path patterns
      command-policy.ts          # Command execution policy
      secret-redaction.ts        # Secret detection and redaction
    plugins/
      plugin-manager.ts          # Plugin loading and lifecycle
      plugin-api.ts              # Public plugin API types
    config/
      server-config.ts           # Server configuration model
      config-watcher.ts          # Configuration file watcher
    utils/
      parser.ts                  # YAML/JSON parser
      schema-loader.ts           # Schema file loader
      path-utils.ts              # Path normalization utilities
      hash.ts                    # Hash utilities
      logger.ts                  # Structured logger
  schemas/
    aeos/
      agent.schema.json
      skill.schema.json
      playbook.schema.json
      policy.schema.json
      permissions.schema.json
      registry.schema.json
      model-profile.schema.json
      token-budget.schema.json
      evidence.schema.json
      judge.schema.json
  docs/
    lsp/
      ARCHITECTURE.md
      PROTOCOL_SUPPORT.md
      DIAGNOSTIC_CODES.md
      EDITOR_INTEGRATION.md
      OPENCODE_INTEGRATION.md
      SECURITY_MODEL.md
      PERFORMANCE.md
      TROUBLESHOOTING.md
```

## Data Flow

### Initialization

```
Client                    Server
  |                         |
  |-- initialize ---------->|
  |                         |-- Load workspace index
  |                         |-- Load and cache schemas
  |                         |-- Verify workspace trust
  |                         |-- Register file watchers
  |                         |-- Build initial graph
  |<-- InitializeResult ----|
  |-- initialized --------->|
  |                         |-- Start background validation
```

### Document Open / Edit / Validation

```
Client                    Server
  |                         |
  |-- didOpen/textDocument->|
  |                         |-- Parse document
  |                         |-- Update document model
  |                         |-- Run schema validation
  |                         |-- Run semantic rules
  |                         |-- Update workspace graph
  |<-- publishDiagnostics --|
  |                         |
  |-- didChange/textDoc---->|
  |                         |-- Incremental parse
  |                         |-- Re-validate changed regions
  |                         |-- Update graph references
  |<-- publishDiagnostics --|
```

### Completion Request

```
Client                    Server
  |                         |
  |-- completion ---------->|
  |                         |-- Determine context (position, trigger)
  |                         |-- Query document model
  |                         |-- Query workspace index (for references)
  |                         |-- Compute completion items
  |<-- CompletionList ------|
```

### Go-To Definition

```
Client                    Server
  |                         |
  |-- definition ---------->|
  |                         |-- Identify reference at position
  |                         |-- Resolve $id / stable_id in workspace graph
  |                         |-- Compute target location
  |<-- Location / Link ------|
```

## Extension Points

The AEOS Language Server supports extension through a plugin API:

| Extension Point | Interface | Description |
|---|---|---|
| **Schema Validator** | `ISchemaValidatorPlugin` | Add custom schema validation logic |
| **Semantic Rule** | `ISemanticRulePlugin` | Register custom semantic diagnostic rules |
| **Completion Provider** | `ICompletionProviderPlugin` | Add custom completion items |
| **Code Action Provider** | `ICodeActionProviderPlugin` | Register quick-fix code actions |
| **Hover Provider** | `IHoverProviderPlugin` | Add custom hover content |
| **Diagnostic Provider** | `IDiagnosticProviderPlugin` | Register custom diagnostic sources |

Plugins are loaded from the workspace `.aeos/plugins/` directory or configured in `aeos.config.json`.

## Security Model Overview

The security layer enforces:

1. **Workspace Trust** — On initialization, the server checks for workspace trust markers (`.aeos/` directory, `aeos.config.yaml`, `aeos.config.json`). Untrusted workspaces get degraded functionality.
2. **Path Policy** — All file paths are normalized and checked against allow/deny patterns. Path traversal attacks are blocked.
3. **Command Policy** — Any command execution requests are validated against an allowlist. Shell injection patterns are detected and blocked.
4. **Secret Redaction** — Secrets are detected and redacted from diagnostics, hover text, and logs. Plaintext secrets in configuration files trigger warnings.
5. **Read-Only by Default** — The server never initiates write operations. All edits are sent as `workspace/applyEdit` for client-side execution.
6. **Sandbox Execution** — If code execution is requested (e.g., for custom validators), it runs in a sandboxed environment with restricted capabilities.

See [SECURITY_MODEL.md](./SECURITY_MODEL.md) for full details.
