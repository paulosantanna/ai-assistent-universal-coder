# AEOS Language Server — LSP Protocol Support

## LSP Version Baseline

The AEOS Language Server targets **LSP 3.17** as its baseline protocol version. Selected features from the upcoming **3.18** draft are implemented as experimental extensions.

| LSP Version | Support | Notes |
|---|---|---|
| 3.16 | Full | Baseline minimum |
| 3.17 | Full | Primary target |
| 3.18 (draft) | Partial | Experimental features (opt-in) |

## Server Capabilities

On `initialize`, the server advertises the following capabilities:

```json
{
  "textDocumentSync": {
    "openClose": true,
    "change": 2,
    "save": { "includeText": true }
  },
  "completionProvider": {
    "triggerCharacters": [".", "/", "\"", "'", "$", "@"],
    "completionItem": {
      "labelDetailsSupport": true,
      "resolveProvider": true
    }
  },
  "hoverProvider": true,
  "definitionProvider": true,
  "referencesProvider": true,
  "documentHighlightProvider": true,
  "documentSymbolProvider": true,
  "workspaceSymbolProvider": true,
  "codeActionProvider": {
    "codeActionKinds": [
      "quickfix",
      "refactor",
      "source.organizeImports"
    ],
    "resolveProvider": true
  },
  "foldingRangeProvider": true,
  "formattingProvider": true,
  "rangeFormattingProvider": true,
  "renameProvider": {
    "prepareProvider": true
  },
  "documentLinkProvider": {
    "resolveProvider": true
  },
  "workspace": {
    "workspaceFolders": {
      "supported": true,
      "changeNotifications": true
    },
    "didChangeConfiguration": {
      "dynamicRegistration": true
    }
  },
  "diagnosticProvider": {
    "interFileDependencies": true,
    "workspaceDiagnostics": true
  },
  "experimental": {
    "aeosSchemaValidation": true,
    "aeosGraphVisualization": true,
    "aeosEvidenceViewer": true,
    "aeosJudgeReport": true,
    "inlineValues": true,
    "typeHierarchy": true,
    "linkedEditingRange": true
  }
}
```

Text document sync uses **Incremental** mode (change = 2) for efficient updates.

## Supported Methods

### Lifecycle Methods

| Method | Direction | Support |
|---|---|---|
| `initialize` | Client → Server | Full |
| `initialized` | Client → Server | Full |
| `shutdown` | Client → Server | Full |
| `exit` | Client → Server | Full |
| `$/cancelRequest` | Bidirectional | Full |
| `$/progress` | Bidirectional | Full |

### Text Document Methods

| Method | Direction | Support |
|---|---|---|
| `textDocument/didOpen` | Client → Server | Full |
| `textDocument/didChange` | Client → Server | Full (incremental) |
| `textDocument/willSave` | Client → Server | Full |
| `textDocument/willSaveWaitUntil` | Client → Server | Full |
| `textDocument/didSave` | Client → Server | Full |
| `textDocument/didClose` | Client → Server | Full |

### Language Features

| Method | Direction | Support | Notes |
|---|---|---|---|
| `textDocument/completion` | Client → Server | Full | Schema-driven + reference completions |
| `completionItem/resolve` | Client → Server | Full | Resolves documentation and detail |
| `textDocument/hover` | Client → Server | Full | Schema docs, type info, reference info |
| `textDocument/definition` | Client → Server | Full | Links to artifact definitions |
| `textDocument/declaration` | Client → Server | Full | |
| `textDocument/implementation` | Client → Server | Full | |
| `textDocument/typeDefinition` | Client → Server | Full | |
| `textDocument/references` | Client → Server | Full | Cross-workspace references |
| `textDocument/documentHighlight` | Client → Server | Full | |
| `textDocument/documentSymbol` | Client → Server | Full | |
| `workspace/symbol` | Client → Server | Full | |
| `textDocument/codeAction` | Client → Server | Full | Quick fixes for diagnostics |
| `codeAction/resolve` | Client → Server | Full | |
| `textDocument/codeLens` | Client → Server | Full | Evidence status, schema links |
| `codeLens/resolve` | Client → Server | Full | |
| `textDocument/foldingRange` | Client → Server | Full | YAML/JSON structure folding |
| `textDocument/formatting` | Client → Server | Full | YAML/JSON formatting |
| `textDocument/rangeFormatting` | Client → Server | Full | |
| `textDocument/onTypeFormatting` | Client → Server | Partial | |
| `textDocument/rename` | Client → Server | Full | Rename $id references across workspace |
| `prepareRename` | Client → Server | Full | |
| `textDocument/documentLink` | Client → Server | Full | Schema $id links |
| `documentLink/resolve` | Client → Server | Full | |
| `textDocument/documentColor` | Client → Server | No | |
| `textDocument/colorPresentation` | Client → Server | No | |
| `textDocument/semanticTokens` | Client → Server | Full | Full semantic token support |
| `textDocument/moniker` | Client → Server | Full | |
| `textDocument/inlayHint` | Client → Server | Full | Type hints, parameter names |
| `inlayHint/resolve` | Client → Server | Full | |
| `textDocument/inlineValue` | Client → Server | Experimental | |
| `textDocument/diagnostic` | Client → Server | Full | Pull-based diagnostics (3.17+) |

### Workspace Methods

| Method | Direction | Support | Notes |
|---|---|---|---|
| `workspace/didChangeWorkspaceFolders` | Client → Server | Full | |
| `workspace/didChangeConfiguration` | Client → Server | Full | |
| `workspace/didChangeWatchedFiles` | Client → Server | Full | |
| `workspace/semanticTokens/refresh` | Server → Client | Full | |
| `workspace/codeLens/refresh` | Server → Client | Full | |
| `workspace/inlayHint/refresh` | Server → Client | Full | |
| `workspace/inlineValue/refresh` | Server → Client | Experimental | |
| `workspace/diagnostic/refresh` | Server → Client | Full | |
| `workspace/executeCommand` | Client → Server | Full | Custom AEOS commands |
| `workspace/applyEdit` | Server → Client | Full | Apply edits from code actions |

### Window Methods

| Method | Direction | Support |
|---|---|---|
| `window/showMessage` | Server → Client | Full |
| `window/showMessageRequest` | Server → Client | Full |
| `window/logMessage` | Server → Client | Full |
| `window/workDoneProgress/create` | Server → Client | Full |
| `window/workDoneProgress/cancel` | Client → Server | Full |
| `telemetry/event` | Server → Client | Full (opt-in) |

### Experimental Methods

These methods are prefixed with `aeos/` and require explicit opt-in via client settings:

| Method | Direction | Support | Description |
|---|---|---|---|
| `aeos/validateSchema` | Client → Server | Experimental | Validate an AEOS file against its schema |
| `aeos/resolveGraph` | Client → Server | Experimental | Resolve the artifact dependency graph |
| `aeos/getEvidenceReport` | Client → Server | Experimental | Get evidence report for an execution |
| `aeos/getJudgeReport` | Client → Server | Experimental | Get judge evaluation report |
| `aeos/generateSnippet` | Client → Server | Experimental | Generate an AEOS artifact snippet |
| `aeos/diagnosticContext` | Client → Server | Experimental | Get rich context for a diagnostic |

## Capabilities Negotiation

The server uses the following negotiation strategy:

1. **Client sends `initialize`** with its capabilities.
2. **Server computes intersection** of client capabilities and server capabilities.
3. **Server responds** with final `ServerCapabilities`, omitting features the client cannot support.
4. **Dynamic registration** is used for features that need runtime configuration.

For experimental features, the client must set `"aeos.experimental.enabled": true` in its initialization options.

## Experimental Features (3.18 Draft)

The following 3.18 draft features are implemented experimentally:

| Feature | Status | Notes |
|---|---|---|
| `textDocument/inlineValue` | Stable | Evaluated inline values for diagnostic references |
| `textDocument/typeHierarchy` | Beta | Type hierarchy for schema type references |
| `textDocument/linkedEditingRange` | Beta | Linked editing for schema $ref targets |
| `workspace/diagnostic` (pull) | Stable | Pull-based diagnostics with doc versioning |
| Diagnostic `data` field | Stable | Rich diagnostic data for code actions |

## Limitations

1. **No multi-root workspace support** — The server operates on a single root workspace. Multi-root is planned.
2. **No remote file system support** — All files must be local. Remote file systems (SSH, WSL) are not supported.
3. **No LSP extension negotiation** — Experimental features require explicit client-side opt-in.
4. **No streaming responses** — All methods use request/response. Streaming is not implemented.
5. **No notebook support** — Notebook cell types are not supported.
6. **Formatting limited to YAML/JSON** — Only `.yaml`, `.yml`, and `.json` files are formatted.
7. **Maximum file size** — Files larger than 10 MB are not indexed.
8. **Maximum workspace size** — Workspaces with more than 10,000 files trigger a warning.

## Extensions

### `workspace/executeCommand` Commands

The server registers the following custom commands:

| Command | Description |
|---|---|
| `aeos.applySchemaFix` | Apply auto-fix for a schema validation error |
| `aeos.organizeAgentSkills` | Sort and organize agent skill references |
| `aeos.generatePlaybookDocs` | Generate documentation for a playbook |
| `aeos.validateAllSchemas` | Validate all AEOS files in the workspace |
| `aeos.exportDependencyGraph` | Export the artifact dependency graph as DOT |
| `aeos.runJudge` | Run judge evaluation on current execution evidence |

### LSP Extensions

The server extends LSP with custom parameters in existing methods:

**`textDocument/completion`** — The completion list includes items with a custom `data` field containing:
- `aeos.schemaPath`: Path to the schema that generated this completion
- `aeos.artifactType`: Type of AEOS artifact
- `aeos.referenceTarget`: If this is a reference, the target `$id`

**`textDocument/publishDiagnostics`** — Each diagnostic includes a `data` field with:
- `aeos.code`: The diagnostic code (see DIAGNOSTIC_CODES.md)
- `aeos.schemaPath`: Schema path that generated this diagnostic
- `aeos.ruleId`: The semantic rule ID (if from a semantic rule)
- `aeos.fixable`: Whether an auto-fix is available
