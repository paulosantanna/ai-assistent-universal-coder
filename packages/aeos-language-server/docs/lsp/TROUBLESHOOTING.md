# AEOS Language Server — Troubleshooting Guide

## Common Issues

### Language Server Not Starting

**Symptoms:**
- No diagnostics, completions, or hover in AEOS files
- Status indicator shows "AEOS Language Server: Stopped" or "Not Connected"
- Editor shows a warning about the language server

**Possible Causes:**

| Cause | Check | Fix |
|---|---|---|
| Server binary not found | Verify installation: `which aeos-language-server` | Install the server: `npm install -g aeos-language-server` |
| Node.js version too old | Check Node version: `node --version` | Upgrade to Node.js 18+ (20 recommended) |
| Wrong server path | Check `aeos.server.path` setting | Update to correct path |
| Port conflict | Check if another server is using the same port | Use `--stdio` transport instead of TCP |
| Permission denied | Check file permissions on the server binary | `chmod +x` on Linux/Mac |
| Missing dependencies | Check for error logs | Run `npm install` in the server directory |

**Diagnostic Steps:**

1. Check the editor's LSP output panel/log
2. Start the server manually:
   ```bash
   aeos-language-server --stdio
   ```
3. Check the server log file:
   ```bash
   cat .aeos/logs/lsp.log
   ```
4. Verify the workspace contains AEOS files

### No Diagnostics

**Symptoms:**
- Files open without error markers or squiggly lines
- No validation feedback on save

**Possible Causes:**

| Cause | Check | Fix |
|---|---|---|
| AEOS disabled | Check `aeos.enable` setting | Set to `true` |
| Wrong file extension | File must be `.yaml`, `.yml`, or `.json` | Rename file or update settings |
| Schema not found | Check `schemas/aeos/` directory exists | Reinstall the server |
| File not recognized as AEOS | File must start with an AEOS artifact structure | Add proper AEOS fields |
| Diagnostics debounce too high | Check `diagnostics.delayMs` | Reduce to 500ms or lower |
| Workspace not trusted | Check for trust warning diagnostic (AEOS0031) | Create `.aeos/` directory |
| File too large | File exceeds 10 MB | Split into smaller files |

**Diagnostic Steps:**

1. Open the file and wait 2-3 seconds
2. Trigger manual validation: use the "AEOS: Validate All Schemas" command
3. Check the LSP log for validation errors
4. Try creating a minimal AEOS file:
   ```yaml
   $id: test-agent
   name: Test
   version: 1.0.0
   capabilities: ["test"]
   ```

### Completions Not Working

**Symptoms:**
- No auto-complete suggestions in AEOS files
- Trigger characters (`.`, `/`, `"`, etc.) don't invoke completions

**Possible Causes:**

| Cause | Check | Fix |
|---|---|---|
| Completions disabled | Check `completions.enabled` setting | Set to `true` |
| Wrong language mode | File must be recognized as YAML or JSON | Check editor language mode |
| Cursor not at completion point | Completions work at property values and references | Move cursor to a valid position |
| Plugin conflict | Another LSP plugin may be intercepting completions | Disable other YAML/JSON servers |
| Feature disabled by profile | Check current profile settings | Switch to balanced or thorough profile |

**Diagnostic Steps:**

1. Type `$id: ` in an AEOS file and check for completions
2. Type `"` after a reference field and check for `$id` completions
3. Check the LSP log for completion-related errors
4. Verify `triggerCharacters` includes `.`, `/`, `"`, `'`, `$`, `@`

### Hover Not Working

**Symptoms:**
- No tooltip/popup when hovering over AEOS fields
- No documentation shown on hover

**Possible Causes:**

| Cause | Check | Fix |
|---|---|---|
| Hover disabled | Check `hover.enabled` setting | Set to `true` |
| Hover mode set to minimal | Check `hover.showSchema` setting | Set to `true` |
| File not recognized | File must be a valid AEOS document | Create valid AEOS content |

**Diagnostic Steps:**

1. Hover over a property name (e.g., `version`, `capabilities`)
2. Hover over a reference value (e.g., a skill `$id`)
3. Check the LSP log for hover-related errors

### Go-To-Definition Not Working

**Symptoms:**
- Ctrl+click or equivalent does not navigate
- "No definition found" message

**Possible Causes:**

| Cause | Check | Fix |
|---|---|---|
| Definition disabled | Check `definition.enabled` setting | Set to `true` |
| Reference points to non-existent artifact | Check workspace for the target `$id` | Create the referenced artifact |
| Cross-file resolution failed | Workspace index may not have resolved | Run "AEOS: Validate All Schemas" |
| File not indexed | File may be excluded by `excludePatterns` | Check performance settings |

**Diagnostic Steps:**

1. Place cursor on a `$id` reference and trigger definition
2. Verify the target artifact exists in the workspace
3. Check the LSP log for resolution errors

### Slow Performance

**Symptoms:**
- Lag when typing in large files
- Delayed diagnostics
- Editor freezes during indexing

**Possible Causes:**

| Cause | Check | Fix |
|---|---|---|
| Very large file | Check file size | Split file or increase `largeFileSizeMB` |
| Too many workspace files | Check file count | Exclude non-AEOS directories |
| Full index running | Check if server just started | Wait for indexing to complete |
| Plugin overhead | Check loaded plugins | Disable unused plugins |
| Memory pressure | Check system memory usage | Reduce cache sizes, switch to fast profile |

**Solutions:**

1. Switch to the **fast** profile:
   ```jsonc
   { "aeos": { "profiles": { "default": "fast" } } }
   ```
2. Increase diagnostic debounce:
   ```jsonc
   { "aeos": { "diagnostics": { "delayMs": 1500 } } }
   ```
3. Exclude non-AEOS directories:
   ```jsonc
   {
     "aeos": {
       "performance": {
         "indexing": {
           "excludePatterns": ["node_modules", ".git", "dist", "build"]
         }
       }
     }
   }
   ```
4. Reduce max indexed files:
   ```jsonc
   { "aeos": { "performance": { "maxFiles": 5000 } } }
   ```
5. Disable semantic validation:
   ```jsonc
   {
     "aeos": {
       "schemas": { "autoValidate": true },
       "diagnostics": { "verbose": false }
     }
   }
   ```

### High Memory Usage

**Symptoms:**
- System becomes slow after editing AEOS files for a while
- Memory usage in process monitor shows > 500 MB

**Solutions:**

1. Reduce LRU cache size:
   ```jsonc
   {
     "aeos": {
       "performance": {
         "cache": {
           "fileContent": { "maxSizeMB": 10 },
           "documentModel": { "maxSizeMB": 10 }
         }
       }
     }
   }
   ```
2. Switch to fast profile
3. Limit indexed files:
   ```jsonc
   { "aeos": { "performance": { "maxFiles": 2000 } } }
   ```
4. Restart the language server periodically

### Workspace Trust Warning

**Symptoms:**
- Warning diagnostic: "Workspace is not trusted"
- Some features are disabled

**Solutions:**

1. Create the `.aeos/` directory:
   ```bash
   mkdir -p .aeos
   ```
2. Create an `aeos.config.yaml` file
3. Or disable trust checks (not recommended):
   ```jsonc
   {
     "aeos": {
       "security": {
         "workspaceTrust": { "enabled": false }
       }
     }
   }
   ```

### Secret Detection False Positives

**Symptoms:**
- Warning diagnostic: "Potential secret detected" on non-secret values

**Solutions:**

1. Add the field to `excludedFields`:
   ```jsonc
   {
     "aeos": {
       "security": {
         "secretRedaction": {
           "excludedFields": ["description", "example", "template"]
         }
       }
     }
   }
   ```
2. Disable secret detection for the workspace (not recommended)

### Plugin Not Loading

**Symptoms:**
- Error diagnostic: "Plugin failed to load"
- Plugin features not available

**Solutions:**

1. Check the plugin is in the correct directory (`.aeos/plugins/`)
2. Ensure the plugin is compatible with the server version
3. Check for missing dependencies
4. Review the log file for detailed error information

## Logging

### Log Levels

| Level | Description | Use Case |
|---|---|---|
| `error` | Errors that prevent operation | Production |
| `warn` | Warnings that should be reviewed | Production |
| `info` | Normal operational messages | Development |
| `debug` | Detailed debugging information | Troubleshooting |
| `trace` | Very detailed tracing | Advanced debugging |

### Configuring Logging

```jsonc
{
  "aeos": {
    "logging": {
      "level": "debug",
      "file": ".aeos/logs/lsp.log",
      "maxSizeMB": 10,
      "maxFiles": 5,
      "format": "json"  // "json" or "text"
    }
  }
}
```

### Viewing Logs

**From the editor:**
- VS Code: View → Output → Select "AEOS Language Server"
- Neovim: `:LspLog`
- Emacs: `M-x eglot-events-buffer`

**From the command line:**
```bash
# Tail the log file
tail -f .aeos/logs/lsp.log

# View last 100 lines
tail -100 .aeos/logs/lsp.log

# Search for errors
grep "ERROR" .aeos/logs/lsp.log

# Search for specific diagnostic code
grep "AEOS0012" .aeos/logs/lsp.log
```

### Log Format (JSON)

```json
{
  "timestamp": "2025-07-11T14:30:00.123Z",
  "level": "ERROR",
  "component": "validator",
  "message": "Schema validation failed",
  "details": {
    "file": "agents/data-processor.yaml",
    "schema": "agent.schema.json",
    "errors": [
      {
        "path": "/version",
        "message": "Value 'abc' does not match pattern '^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)(-[a-zA-Z0-9.]+)?$'"
      }
    ]
  },
  "execution_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Log Format (Text)

```
[2025-07-11T14:30:00.123Z] [ERROR] [validator] Schema validation failed for 'agents/data-processor.yaml': version 'abc' does not match semver pattern
[2025-07-11T14:30:01.456Z] [WARN] [validator] AEOS0012: Reference 'skill/text-analyzer' in 'agents/data-processor.yaml' does not resolve
```

## Diagnostic Codes Reference

For a complete catalog of all diagnostic codes (AEOS0001–AEOS0055), see [DIAGNOSTIC_CODES.md](./DIAGNOSTIC_CODES.md).

### Quick Reference

| Code | Severity | Summary |
|---|---|---|
| AEOS0001 | Error | Schema validation failed |
| AEOS0002 | Error | Missing required property |
| AEOS0003 | Error | Invalid property type |
| AEOS0004 | Error | Value pattern mismatch |
| AEOS0005 | Error | Value not in enum |
| AEOS0006 | Error | Value out of range |
| AEOS0007 | Error | Array too short |
| AEOS0008 | Warning | Duplicate array items |
| AEOS0009 | Error | Additional property not allowed |
| AEOS0010 | Error | Invalid $ref target |
| AEOS0011 | Error | Duplicate $id in workspace |
| AEOS0012 | Error | Unresolved reference |
| AEOS0013 | Error | Circular dependency |
| AEOS0014 | Warning | Missing skill for capability |
| AEOS0015 | Warning | Conflicting delegation policy |
| AEOS0016 | Error | Playbook step references missing artifact |
| AEOS0017 | Info | Unused artifact |
| AEOS0018 | Warning | Incompatible model requirements |
| AEOS0019 | Warning | Environment variable mismatch |
| AEOS0020 | Warning | Deprecated field usage |
| AEOS0021 | Error | Invalid version format |
| AEOS0022 | Warning | Naming convention violation |
| AEOS0023 | Warning | Version downgrade |
| AEOS0024 | Error | Step has no action |
| AEOS0025 | Error | Invalid condition expression |
| AEOS0026 | Warning | Parallel step conflicts |
| AEOS0027 | Info | Unused playbook variable |
| AEOS0028 | Warning | Missing rollback |
| AEOS0029 | Warning | Output never set |
| AEOS0030 | Error | Registry source not found |
| AEOS0031 | Warning | Workspace not trusted |
| AEOS0032 | Error | Path outside allowed scope |
| AEOS0033 | Error | Command not in allowlist |
| AEOS0034 | Warning | Secret in plaintext |
| AEOS0035 | Info | Secret redacted |
| AEOS0036 | Error | Insufficient permissions |
| AEOS0037 | Warning | Approval gate triggered |
| AEOS0038 | Error | Required evidence missing |
| AEOS0039 | Error | Evidence hash mismatch |
| AEOS0040 | Error | Policy evaluation failed |
| AEOS0041 | Info | Large file warning |
| AEOS0042 | Info | Many files warning |
| AEOS0043 | Info | Deep nesting warning |
| AEOS0044 | Info | Schema cache miss |
| AEOS0045 | Info | Index rebuild triggered |
| AEOS0046 | Warning | Configuration not found |
| AEOS0047 | Warning | Invalid configuration |
| AEOS0048 | Info | Feature disabled |
| AEOS0049 | Warning | Missing plugin dependency |
| AEOS0050 | Error | Plugin load error |
| AEOS0051 | Info | Validation passed |
| AEOS0052 | Info | Semantic validation passed |
| AEOS0053 | Info | No AEOS artifacts found |
| AEOS0054 | Info | Using cached index |
| AEOS0055 | Info/Warn | Judge evaluation result |

## Known Limitations

### Current Limitations

1. **No multi-root workspace support** — Only a single workspace root is supported. Multi-root workspaces are planned for a future release.
2. **No remote FS support** — Files must be on the local filesystem. WSL, SSHFS, and other remote filesystems are not supported.
3. **Maximum file size: 10 MB** — Files larger than 10 MB are not indexed and trigger a warning.
4. **Maximum file count: 10,000** — Workspaces with more than 10,000 indexed files trigger a performance warning.
5. **No binary file support** — Only text files (.yaml, .yml, .json) are supported.
6. **No notebook support** — Jupyter notebooks and similar cell-based formats are not supported.
7. **No streaming responses** — All LSP methods use request/response pattern. No server push beyond notifications.
8. **Plugin API is experimental** — The plugin API may change in future versions.

### File Type Limitations

| Extension | Support | Notes |
|---|---|---|
| `.yaml` | Full | Primary AEOS artifact format |
| `.yml` | Full | Alias for `.yaml` |
| `.json` | Full | Alternative AEOS artifact format |
| `.jsonc` | Partial | JSON with comments, no schema validation |
| `.json5` | No | Not supported |
| `.toml` | No | Not supported |
| `.hcl` | No | Not supported |

### Schema Validation Limitations

- Remote `$ref` resolution is disabled by default for security
- Dynamic schemas (generated at runtime) are not supported
- Schema composition (`allOf`, `oneOf`, `anyOf`) may produce complex error messages
- Circular `$ref` in schemas is detected and reported

## Getting Help

### Community Resources

| Resource | URL | Description |
|---|---|---|
| **Documentation** | https://aeos.ai/docs/lsp | Full documentation |
| **GitHub Issues** | https://github.com/anomalyco/aeos/issues | Report bugs, request features |
| **Discussions** | https://github.com/anomalyco/aeos/discussions | Q&A and community support |
| **Discord** | https://discord.gg/aeos | Real-time community chat |

### Before Reporting an Issue

1. Check this troubleshooting guide for common solutions
2. Search existing GitHub issues for similar problems
3. Check the log files for error messages
4. Enable debug logging and reproduce the issue
5. Try with a minimal configuration to isolate the problem

### What to Include in a Bug Report

```
**Environment:**
- OS: Windows 11 / macOS 14 / Ubuntu 24.04
- Editor: VS Code 1.95 / Neovim 0.10 / Emacs 29
- AEOS LS version: 1.0.0
- Node.js version: 20.15.0

**Workspace:**
- File count: 150
- Artifact count: 42
- Config: aeos.config.yaml present

**Problem:**
[Describe the problem clearly and concisely]

**Steps to reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected behavior:**
[What should happen]

**Actual behavior:**
[What actually happens]

**Logs:**
[Relevant log output]

**Screenshots/Videos:**
[If applicable]
```

### Contact

For security issues, please report directly to security@aeos.ai. Do not file a public issue for security vulnerabilities.
