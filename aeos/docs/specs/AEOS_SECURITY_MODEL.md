# AEOS Security Model

## Secret Handling

Allowed:
- logical secret references;
- runtime-only secret resolution;
- OS credential stores;
- Vault-like systems;
- redacted logs.

Forbidden:
- plaintext secrets in files;
- secrets in prompts;
- secrets in traces;
- secrets in evidence;
- secrets in packages;
- cookies/tokens/API keys in ZIPs;
- browser profiles in packages.

## ZIP Security

Every ZIP must be verified before extraction.

Block:
- path traversal;
- absolute paths;
- zip bombs;
- symlinks;
- secrets;
- `.env` real files;
- browser profiles;
- credential stores;
- `.git` unless explicitly allowed.
