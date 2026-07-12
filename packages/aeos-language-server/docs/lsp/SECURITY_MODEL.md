# AEOS Language Server — Security Model

## Overview

The AEOS Language Server implements a defense-in-depth security model aligned with the AEOS platform's security requirements. All features are designed around the principle of least privilege, with fail-closed defaults.

## Security Principles

1. **Fail Closed** — When in doubt, deny access. All security checks default to denying unless explicitly allowed.
2. **Read-Only by Default** — The language server never initiates file writes, command execution, or network requests. All mutating operations go through LSP mechanisms that require client consent.
3. **Defense in Depth** — Multiple security layers ensure that a bypass in one layer is caught by another.
4. **Explicit Trust** — Workspaces must be explicitly trusted before full features are enabled.
5. **Secrets Never Logged** — Secrets are detected and redacted from all server output (diagnostics, logs, hover text).
6. **Auditability** — All security-relevant decisions are logged for audit.

## Workspace Trust

### Trust Markers

A workspace is considered trusted if it contains any of the following markers at its root:

- `.aeos/` directory
- `aeos.config.yaml` file
- `aeos.config.json` file

### Trust Levels

| Level | Trust Marker | Features Enabled |
|---|---|---|
| **Full** | `.aeos/` directory with security configuration | All features including code actions, formatting, experimental features |
| **Standard** | `aeos.config.yaml` or `aeos.config.json` | Validation, completions, hover, definition. Code actions limited to safe operations |
| **Minimal** | No trust marker | Schema validation only. No completions, no cross-file references, no code actions. Warning diagnostic displayed |

### Trust Verification Process

1. On `initialize`, the server scans the workspace root for trust markers
2. If no trust marker is found, the server enters **Minimal** trust mode
3. A diagnostic (AEOS0031) is published indicating the untrusted state
4. The server watches for trust marker creation; if detected, it upgrades trust level and re-indexes
5. Users can explicitly trust a workspace by creating the `.aeos/` directory

### Configuration

```jsonc
{
  "aeos": {
    "security": {
      "workspaceTrust": {
        "enabled": true,          // Enable trust verification
        "required": true,         // Require trust for all features
        "allowedLevels": [        // Allowed trust levels (default: all)
          "full",
          "standard"
        ]
      }
    }
  }
}
```

## Path Policy

### Purpose

Prevent path traversal attacks and restrict file access to the workspace scope.

### Rules

1. **All paths are normalized** — Path separators are normalized to OS-native form, `..` segments are resolved, and symlinks are resolved
2. **Paths must be within the workspace root** — Any path that resolves outside the workspace root is blocked
3. **Blocked patterns** — Paths matching blocked glob patterns are denied
4. **Allowed patterns** — Only paths matching allowed glob patterns are permitted (if configured)

### Default Blocked Paths

```
**/node_modules/**
**/.git/**
**/.svn/**
**/.hg/**
**/CVS/**
**/.DS_Store
**/Thumbs.db
*.exe
*.dll
*.so
*.dylib
*.bin
```

### Configuration

```jsonc
{
  "aeos": {
    "security": {
      "pathPolicy": {
        "enabled": true,
        "blockedPatterns": [
          "**/node_modules/**",
          "**/.git/**",
          "**/secrets/**"
        ],
        "allowedPatterns": [
          "**/*.yaml",
          "**/*.yml",
          "**/*.json"
        ]
      }
    }
  }
}
```

### Path Traversal Detection

The server detects and blocks:
- Directory traversal using `../` or `..\`
- Absolute paths that escape the workspace root
- Symbolic links that point outside the workspace
- UNC paths (Windows)
- Device paths (e.g., `\\.\COM1`)
- Alternative data streams (NTFS ADS)

## Command Policy

### Purpose

Prevent arbitrary command execution and shell injection attacks.

### Rules

1. **All command execution must go through LSP** — The server does not directly execute commands. Commands are sent as workspace edits for the client to execute
2. **Command allowlist** — Only explicitly allowed commands may be executed
3. **Shell injection detection** — Command arguments are scanned for shell metacharacters
4. **No shell execution** — Commands are executed directly, not through a shell

### Default Allowed Commands

```
aeos.applySchemaFix
aeos.organizeAgentSkills
aeos.generatePlaybookDocs
aeos.validateAllSchemas
aeos.exportDependencyGraph
aeos.runJudge
```

### Configuration

```jsonc
{
  "aeos": {
    "security": {
      "commandPolicy": {
        "enabled": true,
        "allowedCommands": [
          "aeos.applySchemaFix",
          "aeos.validateAllSchemas"
        ],
        "blockShellInjection": true
      }
    }
  }
}
```

## Secret Redaction

### Purpose

Prevent accidental exposure of secrets in server output (diagnostics, logs, hover text, completion details).

### Detection Patterns

The server detects the following types of secrets by default:

- API keys (`sk-...`, `pk-...`, etc.)
- AWS access keys (`AKIA...`)
- GitHub tokens (`ghp_...`, `gho_...`, `ghu_...`, etc.)
- Private keys (`-----BEGIN ... PRIVATE KEY-----`)
- JWT tokens
- Connection strings
- Password fields
- Token fields
- Secret fields
- Credential fields

### Redaction Behavior

1. **In diagnostics** — Secret values are replaced with `[REDACTED]`
2. **In logs** — Secret values are replaced with `[REDACTED]`
3. **In hover text** — Secret values are replaced with `[REDACTED]`
4. **In completion details** — Secret values are replaced with `[REDACTED]`
5. **In telemetry** — Secret values are stripped entirely

### Warnings

When a plaintext secret is detected in a configuration file, a warning diagnostic (AEOS0034) is published with the message: `Potential secret detected in field '{field}'. Secrets should not be stored in plaintext in configuration files.`

### Configuration

```jsonc
{
  "aeos": {
    "security": {
      "secretRedaction": {
        "enabled": true,
        "customPatterns": [
          "myapp_secret_.*"
        ],
        "excludedFields": [
          "description",
          "name",
          "author"
        ],
        "redactionString": "[REDACTED]"
      }
    }
  }
}
```

## Read-Only by Default

### Principle

The AEOS Language Server operates in a read-only mode. It never directly:
- Writes files to disk
- Executes shell commands
- Makes network requests
- Modifies the workspace

### Mutating Operations

When a mutating operation is required (e.g., auto-fix from a code action), the server uses LSP's `workspace/applyEdit` request, which sends the edit to the client. The client (editor) decides whether to apply the edit.

### Mutating Operations Flow

```
  Server                              Client
    |                                    |
    |-- workspace/applyEdit ------------>|  Client receives edit
    |                                    |-- Client validates edit
    |                                    |-- Client may show confirmation
    |                                    |-- Client applies edit to buffer
    |<-- applyEdit result ---------------|  Returns success/failure
```

### Allowed Mutating Operations

| Operation | LSP Method | User Confirmation |
|---|---|---|
| Auto-fix schema error | `workspace/applyEdit` | Optional (configurable) |
| Organize agent skills | `workspace/applyEdit` | Optional |
| Rename artifact | `textDocument/rename` | Yes |
| Format document | `textDocument/formatting` | No (can be undone) |

## Sandbox Execution

### Purpose

Custom validators and plugins may require code execution. This is done in a sandboxed environment.

### Sandbox Properties

1. **No file system access** — Sandboxed code cannot read or write files
2. **No network access** — Sandboxed code cannot make network requests
3. **Resource limits** — CPU time and memory are limited
4. **Timeout** — Sandboxed execution is terminated after a configurable timeout
5. **No process spawning** — Sandboxed code cannot spawn child processes
6. **No native modules** — Only pure JavaScript/TypeScript code is allowed

### Configuration

```jsonc
{
  "aeos": {
    "security": {
      "sandbox": {
        "enabled": true,
        "timeoutMs": 5000,
        "maxMemoryMB": 64,
        "maxCpuTimeMs": 2000
      }
    }
  }
}
```

### Sandbox Backend

The sandbox uses:
- **Node.js**: `vm` module with `contextified` sandbox, no `require`, no `process`, no `fs`
- **Deno**: `--allow-none` permissions flag (if using Deno runtime)
- **WebAssembly**: Wasmtime or similar Wasm runtime (planned)

## Network Security

### Purpose

Prevent data exfiltration and unauthorized network access.

### Rules

1. **No outgoing network requests** — The server does not initiate network connections
2. **Schema loading** — Schemas are loaded from local files only. Remote `$ref` resolution is disabled by default
3. **Telemetry** — If enabled, telemetry data is sent over HTTPS with strict TLS verification

### Configuration

```jsonc
{
  "aeos": {
    "security": {
      "network": {
        "allowRemoteSchemas": false,   // Block remote $ref resolution
        "telemetry": {
          "enabled": false,            // Telemetry opt-in
          "endpoint": ""
        },
        "proxy": {
          "enabled": false             // No proxy by default
        }
      }
    }
  }
}
```

## Security Event Logging

All security-relevant events are logged with the following information:

```typescript
interface SecurityEvent {
  timestamp: string;           // ISO 8601
  eventType: string;           // e.g., "path_blocked", "secret_redacted"
  severity: string;            // "info", "warning", "error", "critical"
  details: string;             // Human-readable description
  source: string;              // Component that generated the event
  /** No sensitive data is included in security events */
}
```

### Security Events

| Event Type | Severity | Description |
|---|---|---|
| `trust_check` | info | Workspace trust level determined |
| `trust_upgraded` | info | Workspace trust level upgraded |
| `trust_downgraded` | warning | Workspace trust level downgraded |
| `path_blocked` | warning | Path access denied by path policy |
| `path_traversal_detected` | error | Path traversal attack detected and blocked |
| `command_blocked` | warning | Command execution denied by command policy |
| `injection_detected` | error | Shell injection attempt detected and blocked |
| `secret_redacted` | info | Secret value redacted from output |
| `secret_plaintext` | warning | Plaintext secret detected in configuration |
| `sandbox_timeout` | warning | Sandboxed execution timed out |
| `sandbox_violation` | error | Sandbox violation detected |
| `network_blocked` | info | Network request blocked |

## Security Checklist

- [ ] Workspace trust is verified on startup
- [ ] All paths are normalized and validated
- [ ] Path traversal attacks are blocked
- [ ] Command execution is restricted to an allowlist
- [ ] Shell injection is detected and blocked
- [ ] Secrets are detected and redacted from all output
- [ ] Plaintext secrets in config files trigger warnings
- [ ] Server is read-only; edits go through LSP
- [ ] Plugin execution is sandboxed
- [ ] Network requests are blocked by default
- [ ] All security events are logged
- [ ] Telemetry is opt-in only
