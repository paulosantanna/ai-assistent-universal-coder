SERVER_NAME = "aeos-lsp"
SERVER_VERSION = "1.0.0"
SERVER_PROTOCOL_VERSION = "3.17"

AEOS_DOCUMENT_PATTERNS = [
    "AGENT.md",
    "AGENTS.md",
    "SKILL.md",
    "PLAYBOOK.md",
    "*.agent.md",
    "*.skill.md",
    "*.playbook.md",
    "*.aeos",
    "*.aeos.yaml",
    "*.aeos.yml",
    "*.aeos.json",
    "*.aeos.jsonc",
    "*.aeos.toml",
    "aeos.config.yaml",
    "permissions.yaml",
    "policies.yaml",
    "overlay.index",
    "overlay.registry.index.yaml",
]

AEOS_REGISTRY_FILES = [
    "agents.registry.yaml",
    "skills.registry.yaml",
    "playbooks.registry.yaml",
    "mcps.registry.yaml",
    "lcps.registry.yaml",
    "blueprints.registry.yaml",
    "enterprise-skills.registry.yaml",
    "enterprise-playbooks.registry.yaml",
    "workbench-profiles.registry.yaml",
    "overlay.registry.index.yaml",
]

AEOS_DIRECTIVES = {"@agent", "@skill", "@playbook", "@tool", "@policy", "@permission", "@evidence", "@gate", "@model", "@step", "@variable", "@input", "@output", "@dependency", "@rollback"}

DEFAULT_EXCLUSIONS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
    "coverage",
    "htmlcov",
    "logs",
    "tmp",
    "temp",
    ".aeos/sandbox",
    "checkpoints",
    "*.safetensors",
    "*.pt",
    "*.pth",
    "*.bin",
    "*.db-wal",
    "*.db-shm",
    "*.db-journal",
}

MAX_DIAGNOSTICS_PER_FILE_DEFAULT = 100
MAX_WORKSPACE_DIAGNOSTICS_DEFAULT = 500
MAX_COMPLETION_ITEMS_DEFAULT = 100
MAX_REFERENCES_DEFAULT = 100
MAX_OUTPUT_CHARS_DEFAULT = 1048576
DEBOUNCE_MILLISECONDS_DEFAULT = 300
INDEXING_CONCURRENCY_DEFAULT = 4
BACKGROUND_INDEXING_DEFAULT = True
DIAGNOSTIC_PROFILE_DEFAULT = "editor"
ENABLE_EXPERIMENTAL_FEATURES_DEFAULT = False

EXIT_SUCCESS = 0
EXIT_DIAGNOSTICS_ERROR = 1
EXIT_INVALID_CONFIG = 2
EXIT_INTERNAL_ERROR = 3
EXIT_OPERATION_BLOCKED = 4
EXIT_TIMEOUT = 5

LSP_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
DEFAULT_LOG_LEVEL = "WARNING"

SEMANTIC_TOKEN_TYPES = [
    "agent", "skill", "playbook", "tool", "policy", "permission",
    "gate", "evidence", "model", "variable", "input", "output",
    "step", "registry", "deprecated", "unsafe", "unresolved",
    "readOnly", "mutating", "keyword", "string", "number", "comment",
    "property", "directive",
]
SEMANTIC_TOKEN_MODIFIERS = [
    "declaration", "definition", "readonly", "static", "deprecated",
    "abstract", "async", "modification", "documentation", "defaultLibrary",
]

MAX_CACHE_SIZE_MB = 256
CACHE_DIR_NAME = "lsp"
INDEX_DB_NAME = "index.sqlite"
INDEX_DB_VERSION = 1
