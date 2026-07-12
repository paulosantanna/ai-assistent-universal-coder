# AEOS Language Server — Editor Integration Guide

## Overview

The AEOS Language Server works with any editor that supports the Language Server Protocol (LSP). Below are setup instructions for popular editors.

## VS Code

### Installation

1. Install the AEOS extension from the VS Code Marketplace:
   ```
   Extensions: Search for "AEOS Language Support"
   ```

2. Or install via command line:
   ```bash
   code --install-extension aeos.aeos-language-support
   ```

### Configuration

Create or edit `.vscode/settings.json` in your workspace:

```json
{
  "aeos.server.path": "node_modules/.bin/aeos-language-server",
  "aeos.server.args": ["--stdio"],
  "aeos.enable": true,
  "aeos.schemas.autoValidate": true,
  "aeos.diagnostics.verbose": false,
  "aeos.completions.snippets": true,
  "aeos.completions.references": true,
  "aeos.hover.showSchema": true,
  "aeos.hover.showExamples": false,
  "aeos.format.enable": true,
  "aeos.format.style": "default",
  "aeos.security.workspaceTrust.enabled": true,
  "aeos.performance.maxFiles": 10000,
  "aeos.performance.largeFileSizeMB": 1,
  "aeos.experimental.enabled": false
}
```

### Available Commands

| Command | Keybinding | Description |
|---|---|---|
| AEOS: Validate All Schemas | — | Validate all AEOS files in workspace |
| AEOS: Auto-Fix Schema | Ctrl+. (with diagnostic) | Apply auto-fix for selected diagnostic |
| AEOS: Organize Agent Skills | — | Sort and organize agent skill references |
| AEOS: Generate Playbook Docs | — | Generate markdown docs for a playbook |
| AEOS: Export Dependency Graph | — | Export artifact dependency graph as DOT |
| AEOS: Run Judge | — | Run judge evaluation on evidence |

### Troubleshooting VS Code

**Server not starting:**
- Check that `aeos-language-server` is installed (`npm list -g aeos-language-server`)
- Check the Output panel (View → Output, select "AEOS Language Server")
- Verify the `aeos.server.path` setting points to the correct binary

**No diagnostics:**
- Ensure the file is saved with `.yaml`, `.yml`, or `.json` extension
- Check that `aeos.enable` is `true`
- Check that `aeos.schemas.autoValidate` is `true`

---

## Neovim

### Using nvim-lspconfig

```lua
-- Install the language server:
-- npm install -g aeos-language-server

-- Configure with lspconfig:
local lspconfig = require('lspconfig')

lspconfig.aeos_ls.setup({
  cmd = { "aeos-language-server", "--stdio" },
  filetypes = { "yaml", "yml", "json" },
  root_dir = lspconfig.util.root_pattern(
    "aeos.config.yaml",
    "aeos.config.json",
    ".aeos"
  ),
  settings = {
    aeos = {
      enable = true,
      schemas = {
        autoValidate = true,
      },
      diagnostics = {
        verbose = false,
      },
      completions = {
        snippets = true,
        references = true,
      },
      format = {
        enable = true,
      },
    },
  },
  capabilities = {
    -- Ensure 3.17 capabilities
    textDocument = {
      diagnostic = {
        dynamicRegistration = true,
      },
    },
    workspace = {
      diagnostic = {
        dynamicRegistration = true,
      },
    },
  },
})

-- Keybindings
vim.api.nvim_create_autocmd('FileType', {
  pattern = { 'yaml', 'json' },
  callback = function()
    local bufopts = { noremap = true, silent = true, buffer = bufnr }
    vim.keymap.set('n', 'gD', vim.lsp.buf.declaration, bufopts)
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, bufopts)
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, bufopts)
    vim.keymap.set('n', 'gi', vim.lsp.buf.implementation, bufopts)
    vim.keymap.set('n', '<C-k>', vim.lsp.buf.signature_help, bufopts)
    vim.keymap.set('n', '<leader>wa', vim.lsp.buf.add_workspace_folder, bufopts)
    vim.keymap.set('n', '<leader>wr', vim.lsp.buf.remove_workspace_folder, bufopts)
    vim.keymap.set('n', '<leader>wl', function()
      print(vim.inspect(vim.lsp.buf.list_workspace_folders()))
    end, bufopts)
    vim.keymap.set('n', '<leader>D', vim.lsp.buf.type_definition, bufopts)
    vim.keymap.set('n', '<leader>rn', vim.lsp.buf.rename, bufopts)
    vim.keymap.set('n', '<leader>ca', vim.lsp.buf.code_action, bufopts)
    vim.keymap.set('n', 'gr', vim.lsp.buf.references, bufopts)
    vim.keymap.set('n', '<leader>f', function()
      vim.lsp.buf.format({ async = true })
    end, bufopts)
  end,
})
```

### Using mason.nvim (automatic installation)

```lua
require('mason').setup()
require('mason-lspconfig').setup({
  ensure_installed = { 'aeos_ls' },
  automatic_installation = true,
})

local lspconfig = require('lspconfig')
lspconfig.aeos_ls.setup({
  -- See configuration above
})
```

### Troubleshooting Neovim

**Server not found:**
- Run `:LspInfo` to see the server status
- Check that `aeos-language-server` is in your PATH
- Verify `root_dir` pattern matches your workspace

**No completions:**
- Check `:LspLog` for errors
- Ensure `capabilities` includes textDocument.completion

---

## Emacs

### Using eglot

```elisp
;; Install the language server:
;; npm install -g aeos-language-server

(require 'eglot)

(add-to-list 'eglot-server-programs
             '((yaml-mode yaml-ts-mode json-mode json-ts-mode)
               . ("aeos-language-server" "--stdio")))

(setq eglot-workspace-configuration
      '(:aeos (:enable t
               :schemas (:autoValidate t)
               :diagnostics (:verbose :json-false)
               :completions (:snippets t :references t)
               :format (:enable t))))

;; Keybindings
(define-key yaml-mode-map (kbd "C-c C-d") 'eldoc)
(define-key yaml-mode-map (kbd "M-.") 'xref-find-definitions)
(define-key yaml-mode-map (kbd "M-,") 'xref-pop-marker-stack)
(define-key yaml-mode-map (kbd "C-c C-r") 'xref-find-references)
(define-key yaml-mode-map (kbd "C-c C-a") 'eglot-code-actions)
(define-key yaml-mode-map (kbd "C-c C-f") 'eglot-format)
```

### Using lsp-mode

```elisp
(require 'lsp-mode)

(lsp-register-client
  (make-lsp-client
    :new-connection (lsp-stdio-connection '("aeos-language-server" "--stdio"))
    :major-modes '(yaml-mode yaml-ts-mode json-mode json-ts-mode)
    :server-id 'aeos-ls
    :notification-handlers
    (ht ("window/showMessage" #'lsp--window-show-message)
        ("window/logMessage" #'lsp--window-log-message))
    :initialized-fn (lambda (workspace)
                      (with-lsp-workspace workspace
                        (lsp--set-configuration
                          '(:aeos (:enable t
                                   :schemas (:autoValidate t)
                                   :diagnostics (:verbose :json-false)
                                   :completions (:snippets t :references t)
                                   :format (:enable t))))))))

(add-hook 'yaml-mode-hook #'lsp)
(add-hook 'json-mode-hook #'lsp)
```

---

## Helix

```toml
# In ~/.config/helix/languages.toml
[[language]]
name = "yaml"
auto-format = true
language-servers = ["aeos-ls"]

[[language]]
name = "json"
auto-format = true
language-servers = ["aeos-ls"]

[language-server.aeos-ls]
command = "aeos-language-server"
args = ["--stdio"]
config = { aeos = { enable = true, schemas = { autoValidate = true } } }
```

---

## Sublime Text

1. Install the LSP package via Package Control.
2. Add to LSP settings:

```json
{
  "clients": {
    "aeos-language-server": {
      "command": ["aeos-language-server", "--stdio"],
      "selector": "source.yaml | source.json",
      "syntaxes": ["YAML", "JSON"],
      "settings": {
        "aeos": {
          "enable": true,
          "schemas": { "autoValidate": true }
        }
      }
    }
  }
}
```

---

## Any LSP-Compatible Editor

All LSP-compatible editors follow the same pattern:

1. **Install the server**: `npm install -g aeos-language-server`
2. **Configure the editor**: Point it to the `aeos-language-server --stdio` command
3. **Set file types**: Associate with `.yaml`, `.yml`, `.json` files
4. **Set root markers**: Use `aeos.config.yaml`, `aeos.config.json`, or `.aeos` directory
5. **Configure settings**: Pass AEOS-specific settings via the `settings` or `initializationOptions` field

### Generic LSP Configuration

```json
{
  "command": ["aeos-language-server", "--stdio"],
  "languageId": "yaml",
  "filetypes": ["yaml", "yml", "json"],
  "rootPatterns": ["aeos.config.yaml", "aeos.config.json", ".aeos"],
  "settings": {
    "aeos": {
      "enable": true,
      "schemas": { "autoValidate": true },
      "diagnostics": { "verbose": false },
      "completions": { "snippets": true, "references": true },
      "hover": { "showSchema": true, "showExamples": false },
      "format": { "enable": true },
      "security": { "workspaceTrust": { "enabled": true } },
      "performance": {
        "maxFiles": 10000,
        "largeFileSizeMB": 1
      }
    }
  }
}
```

---

## Settings Reference

| Setting | Type | Default | Description |
|---|---|---|---|
| `aeos.enable` | boolean | `true` | Enable/disable the language server |
| `aeos.server.path` | string | `aeos-language-server` | Path to the server executable |
| `aeos.server.args` | string[] | `["--stdio"]` | Server command-line arguments |
| `aeos.schemas.autoValidate` | boolean | `true` | Automatically validate on file change |
| `aeos.diagnostics.verbose` | boolean | `false` | Include informational diagnostics |
| `aeos.diagnostics.delayMs` | number | `500` | Debounce delay for diagnostics |
| `aeos.completions.snippets` | boolean | `true` | Enable snippet completions |
| `aeos.completions.references` | boolean | `true` | Enable reference completions |
| `aeos.completions.triggerChars` | string[] | `[".", "/", "\"", "'", "$", "@"]` | Completion trigger characters |
| `aeos.hover.showSchema` | boolean | `true` | Show schema documentation on hover |
| `aeos.hover.showExamples` | boolean | `false` | Show examples on hover |
| `aeos.definition.enable` | boolean | `true` | Enable go-to-definition |
| `aeos.references.enable` | boolean | `true` | Enable find references |
| `aeos.format.enable` | boolean | `true` | Enable document formatting |
| `aeos.format.style` | string | `"default"` | Formatting style (`default`, `compact`, `expanded`) |
| `aeos.security.workspaceTrust.enabled` | boolean | `true` | Enable workspace trust checks |
| `aeos.security.pathPolicy.enabled` | boolean | `true` | Enable path policy enforcement |
| `aeos.performance.maxFiles` | number | `10000` | Maximum indexed files |
| `aeos.performance.largeFileSizeMB` | number | `1` | Threshold for large file warning |
| `aeos.experimental.enabled` | boolean | `false` | Enable experimental features |
| `aeos.trace.server` | string | `"off"` | Server trace verbosity (`off`, `messages`, `verbose`) |
