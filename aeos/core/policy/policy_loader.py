from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from aeos.core.policy.policy_models import PolicyConfig


class PolicyLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()
        self.config: Optional[PolicyConfig] = None
        self.enterprise_configs: dict[str, dict] = {}

    def load(self, policies_path: str = "aeos/config/policies.yaml") -> PolicyConfig:
        full = self.workspace_root / policies_path
        if not full.exists():
            raise FileNotFoundError(f"Policies file not found: {full}")

        with open(full, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        policies = data.get("policies", {})
        self.config = PolicyConfig()

        branches = policies.get("protected_branches", {})
        self.config.protected_branches = branches.get("block_mutation", ["main", "master", "develop"])

        fs = policies.get("filesystem", {})
        self.config.allow_write_paths = fs.get("allow_write_without_approval", self.config.allow_write_paths)
        self.config.block_delete_without_approval = fs.get("block_delete_without_approval", True)

        git = policies.get("git", {})
        self.config.block_merge_always = git.get("block_merge_always", True)
        self.config.block_force_push_always = git.get("block_force_push_always", True)
        self.config.block_commit_without_approval = git.get("block_commit_without_approval", True)
        self.config.block_push_without_approval = git.get("block_push_without_approval", True)

        shell = policies.get("shell", {})
        self.config.shell_allowlist = shell.get("allowlist", [])
        self.config.block_unlisted_shell = shell.get("block_unlisted", True)
        self.config.block_destructive_shell_patterns = shell.get("block_destructive_patterns", [])

        secrets = policies.get("secrets", {})
        self.config.block_secret_output = secrets.get("block_output_values", True)
        self.config.block_secret_package = secrets.get("block_package_values", True)
        self.config.block_secret_logging = secrets.get("block_logging", True)

        packaging = policies.get("packaging", {})
        self.config.require_package_manifest = packaging.get("require_manifest", True)
        self.config.require_package_sha256 = packaging.get("require_sha256", True)
        self.config.block_package_path_traversal = packaging.get("block_path_traversal", True)
        self.config.block_package_absolute_paths = packaging.get("block_absolute_paths", True)
        self.config.block_package_symlinks = packaging.get("block_symlinks", True)
        self.config.block_package_zip_bomb = packaging.get("block_zip_bomb", True)

        return self.config

    def load_enterprise_configs(self) -> dict[str, dict]:
        config_files = [
            ("production_enterprise", "aeos/config/production-enterprise.config.yaml"),
            ("enterprise_security", "aeos/config/enterprise-security.config.yaml"),
            ("security_hardening", "aeos/config/security-hardening.config.yaml"),
        ]

        for key, path in config_files:
            full = self.workspace_root / path
            if full.exists():
                with open(full, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                if data:
                    self.enterprise_configs[key] = data

        return self.enterprise_configs
