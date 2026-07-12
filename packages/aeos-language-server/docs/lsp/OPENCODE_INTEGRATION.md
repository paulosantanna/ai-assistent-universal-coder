# AEOS Language Server — OpenCode Integration

## Overview

The AEOS Language Server integrates with OpenCode to provide intelligent editing support for AEOS workspace configurations. When editing AEOS artifacts in an OpenCode session, the language server provides real-time validation, completions, and navigation.

## Configuration Example

### `.opencode/aeos.jsonc`

```jsonc
{
  "aeos": {
    "enable": true,
    "server": {
      "path": "packages/aeos-language-server",
      "args": ["--stdio"],
      "autoStart": true
    },
    "schemas": {
      "autoValidate": true,
      "strictMode": true,
      "customSchemas": []
    },
    "diagnostics": {
      "verbose": false,
      "includeInfo": true,
      "delayMs": 300
    },
    "completions": {
      "enabled": true,
      "snippets": true,
      "references": true,
      "triggerCharacters": [".", "/", "\"", "'", "$", "@"]
    },
    "hover": {
      "showSchema": true,
      "showDocumentation": true,
      "showExamples": false
    },
    "definition": {
      "enabled": true,
      "navigateToSource": true
    },
    "format": {
      "enabled": true,
      "style": "default",
      "onSave": true
    },
    "security": {
      "workspaceTrust": {
        "enabled": true,
        "required": true
      },
      "pathPolicy": {
        "enabled": true
      },
      "secretRedaction": {
        "enabled": true
      }
    },
    "performance": {
      "indexing": {
        "maxFiles": 10000,
        "excludePatterns": ["node_modules", ".git", "dist", "build"],
        "debounceMs": 1000
      },
      "cache": {
        "enabled": true,
        "maxSize": 50,
        "ttlSeconds": 300
      }
    },
    "profiles": {
      "default": "balanced",
      "available": {
        "fast": {
          "validation": "minimal",
          "completions": false,
          "indexing": "shallow"
        },
        "balanced": {
          "validation": "standard",
          "completions": true,
          "indexing": "full"
        },
        "thorough": {
          "validation": "full",
          "completions": true,
          "indexing": "full",
          "semanticRules": "all"
        }
      }
    },
    "experimental": {
      "enabled": false,
      "features": []
    },
    "logging": {
      "level": "info",
      "file": ".aeos/logs/lsp.log",
      "maxSizeMB": 10
    }
  }
}
```

### Minimal Configuration

```jsonc
{
  "aeos": {
    "enable": true
  }
}
```

## Profile Selection

The AEOS Language Server supports three performance profiles that balance features and resource usage:

### Fast Profile

Best for quick editing sessions where full validation is not required.

```jsonc
{
  "aeos": {
    "profiles": {
      "default": "fast"
    }
  }
}
```

Characteristics:
- **Validation**: Minimal — schema validation only, no semantic rules
- **Completions**: Disabled
- **Indexing**: Shallow — file-level only, no cross-reference resolution
- **Diagnostics**: Errors only
- **Hover**: Disabled
- **Memory usage**: ~50 MB

### Balanced Profile (Default)

Suitable for most editing sessions. Provides full editing support with reasonable performance.

```jsonc
{
  "aeos": {
    "profiles": {
      "default": "balanced"
    }
  }
}
```

Characteristics:
- **Validation**: Standard — schema + common semantic rules
- **Completions**: Enabled (snippets and references)
- **Indexing**: Full — file-level + cross-reference resolution
- **Diagnostics**: Errors and warnings
- **Hover**: Enabled (schema only)
- **Memory usage**: ~150 MB

### Thorough Profile

Best for review, audit, and compliance workflows. Enables all validation and analysis.

```jsonc
{
  "aeos": {
    "profiles": {
      "default": "thorough"
    }
  }
}
```

Characteristics:
- **Validation**: Full — schema + all semantic rules + security checks
- **Completions**: Enabled (all types)
- **Indexing**: Full with deep reference resolution
- **Diagnostics**: Errors, warnings, and informational
- **Hover**: Enabled (schema + documentation + examples)
- **Memory usage**: ~300 MB

## Performance Tuning

### Reduce Startup Time

```jsonc
{
  "aeos": {
    "performance": {
      "indexing": {
        "debounceMs": 2000,          // Wait longer before indexing
        "excludePatterns": [          // Exclude non-AEOS files
          "node_modules", ".git", "dist", "build",
          "*.log", "*.tmp"
        ]
      },
      "cache": {
        "enabled": true,
        "maxSize": 100,               // Larger cache for repeat edits
        "ttlSeconds": 600             // Keep cache for 10 minutes
      }
    }
  }
}
```

### Reduce Memory Usage

```jsonc
{
  "aeos": {
    "performance": {
      "maxFiles": 5000,               // Index fewer files
      "cache": {
        "maxSize": 20                 // Smaller cache
      }
    },
    "completions": {
      "references": false             // Disable reference completions
    },
    "hover": {
      "showExamples": false
    }
  }
}
```

### Improve Responsiveness

```jsonc
{
  "aeos": {
    "diagnostics": {
      "delayMs": 1000                 // Longer debounce for fewer re-validations
    },
    "completions": {
      "triggerCharacters": ["."]      // Fewer trigger characters
    },
    "format": {
      "onSave": false                 // Format only on explicit command
    }
  }
}
```

## Troubleshooting

### Server won't start

**Symptoms**: No diagnostics, completions, or hover. OpenCode shows "AEOS Language Server not connected."

**Checks**:
1. Verify the server binary exists:
   ```bash
   ls packages/aeos-language-server/dist/server.js
   ```
2. Check the server path in configuration:
   ```jsonc
   {
     "aeos": {
       "server": {
         "path": "packages/aeos-language-server",
         "args": ["--stdio"]
       }
     }
   }
   ```
3. Start the server manually to check for errors:
   ```bash
   node packages/aeos-language-server/dist/server.js --stdio
   ```
4. Check the log file:
   ```bash
   cat .aeos/logs/lsp.log
   ```

### No diagnostics

**Symptoms**: Files open without error markers.

**Checks**:
1. Ensure `aeos.enable` is `true`
2. Check that the file has a `.yaml`, `.yml`, or `.json` extension
3. Verify `diagnostics.delayMs` is not set too high
4. Run the validate command manually: `AEOS: Validate All Schemas`
5. Check the log file for validation errors

### Slow performance

**Symptoms**: Editing feels sluggish, especially in large workspaces.

**Solutions**:
1. Switch to the "fast" profile:
   ```jsonc
   { "aeos": { "profiles": { "default": "fast" } } }
   ```
2. Increase the diagnostic debounce delay:
   ```jsonc
   { "aeos": { "diagnostics": { "delayMs": 2000 } } }
   ```
3. Exclude more files from indexing:
   ```jsonc
   { "aeos": { "performance": { "indexing": { "excludePatterns": ["**"] } } } }
   ```
4. Disable features you don't need:
   ```jsonc
   {
     "aeos": {
       "completions": { "enabled": false },
       "hover": { "showSchema": false },
       "format": { "enabled": false }
     }
   }
   ```

### Memory usage too high

**Symptoms**: System becomes slow after extended editing.

**Solutions**:
1. Reduce `maxFiles` to limit indexing scope
2. Disable the cache or reduce its size
3. Switch to the "fast" profile
4. Periodically restart the language server

### Secret redaction warnings

**Symptoms**: Warnings about plaintext secrets in configuration files.

**Solutions**:
1. Move secrets to environment variables or a secure credential store
2. Use the `$ref` pattern to reference secrets from a secure source
3. If the warning is a false positive, adjust the secret detection patterns:
   ```jsonc
   {
     "aeos": {
       "security": {
         "secretRedaction": {
           "customPatterns": []
         }
       }
     }
   }
   ```

### Workspace trust issues

**Symptoms**: "Workspace is not trusted" warning.

**Solutions**:
1. Ensure a `.aeos/` directory exists at the workspace root:
   ```bash
   mkdir -p .aeos
   ```
2. Or create a `aeos.config.yaml` file at the workspace root
3. Or disable workspace trust checks (not recommended):
   ```jsonc
   {
     "aeos": {
       "security": {
         "workspaceTrust": { "enabled": false }
       }
     }
   }
   ```

---

## Logging

The AEOS Language Server logs to both stdout/stderr (captured by OpenCode) and a log file. To view logs:

### OpenCode Console

Logs appear in the OpenCode console output. Set logging level:

```jsonc
{
  "aeos": {
    "logging": {
      "level": "debug"  // error, warn, info, debug, trace
    }
  }
}
```

### Log File

Logs are written to the configured log file (default: `.aeos/logs/lsp.log`):

```bash
tail -f .aeos/logs/lsp.log
```

### Diagnostic Log Example

```
[2025-07-11T14:30:00.123Z] [INFO] [server] AEOS Language Server v1.0.0 starting
[2025-07-11T14:30:00.456Z] [INFO] [indexer] Loading workspace index from E:\Projects\aeos-demo
[2025-07-11T14:30:01.234Z] [INFO] [indexer] Found 42 AEOS files
[2025-07-11T14:30:01.567Z] [INFO] [validator] Validating agent 'data-processor'...
[2025-07-11T14:30:01.890Z] [WARN] [validator] AEOS0012: Reference 'skill/text-analyzer' in 'agents/data-processor.yaml' does not resolve
[2025-07-11T14:30:02.000Z] [INFO] [server] Server initialized in 1.877s
```

---

## Commands

The language server registers the following commands that can be triggered from OpenCode:

| Command | Description |
|---|---|
| `aeos.applySchemaFix` | Apply auto-fix for a schema validation error |
| `aeos.validateAll` | Validate all AEOS files in the workspace |
| `aeos.exportGraph` | Export the dependency graph as DOT format |
| `aeos.toggleProfile` | Switch between performance profiles |
| `aeos.clearCache` | Clear the validation and index caches |
| `aeos.showStatus` | Show server status and statistics |
