from __future__ import annotations

import fnmatch
from aeos.core.policy.policy_loader import PolicyLoader
from aeos.core.policy.policy_models import (
    PolicyConfig,
    PolicyDecision,
    PolicyRequest,
    PolicySeverity,
    generate_policy_decision_id,
    now_iso,
)


class PolicyEngine:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root
        self.loader = PolicyLoader(workspace_root)
        self.config: PolicyConfig | None = None
        self.decisions: list[PolicyDecision] = []

    def initialize(self) -> None:
        self.config = self.loader.load()
        self.loader.load_enterprise_configs()

    def evaluate(self, request: PolicyRequest) -> PolicyDecision:
        decision_id = generate_policy_decision_id()
        now = now_iso()

        if not self.config:
            return PolicyDecision(
                decision_id=decision_id, execution_id=request.execution_id,
                action=request.action, resource=request.resource,
                allowed=False, severity=PolicySeverity.CRITICAL,
                reason="Policy engine not initialized",
                matched_policy="engine.initialized", timestamp=now,
            )

        checker_map = {
            "git.merge": self._check_git_merge,
            "git.force_push": self._check_git_force_push,
            "git.commit": self._check_git_commit,
            "git.push": self._check_git_push,
            "filesystem.write": self._check_filesystem_write,
            "filesystem.delete": self._check_filesystem_delete,
            "shell.run": self._check_shell_run,
            "secrets.read": self._check_secrets_read,
            "secrets.output": self._check_secrets_output,
            "package.extract": self._check_package_extract,
            "package.verify": self._check_package_verify,
            "approval.wildcard": self._check_approval_wildcard,
            "auto_merge": self._check_auto_merge,
            "auto_deploy": self._check_auto_deploy,
            "branch.protected": self._check_branch_protected,
            "secret.persist": self._check_secret_persist,
            "pack.import_direct": self._check_pack_import_direct,
        }

        checker = checker_map.get(request.action)
        if checker:
            decision = checker(request, decision_id, now)
        else:
            decision = PolicyDecision(
                decision_id=decision_id, execution_id=request.execution_id,
                action=request.action, resource=request.resource,
                allowed=True, severity=PolicySeverity.LOW,
                reason=f"No specific policy for action '{request.action}', default allow",
                matched_policy="default.allow", timestamp=now,
            )

        self.decisions.append(decision)
        return decision

    def _check_branch_protected(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        branch = req.branch or req.resource
        if branch in self.config.protected_branches:
            return PolicyDecision(
                decision_id=did, execution_id=req.execution_id,
                action=req.action, resource=req.resource,
                allowed=False, severity=PolicySeverity.CRITICAL,
                reason=f"Protected branch '{branch}' mutation blocked",
                matched_policy="protected_branches.block_mutation", timestamp=ts,
            )
        return PolicyDecision(
            decision_id=did, execution_id=req.execution_id,
            action=req.action, resource=req.resource,
            allowed=True, severity=PolicySeverity.LOW,
            reason=f"Branch '{branch}' is not protected",
            matched_policy="protected_branches.block_mutation", timestamp=ts,
        )

    def _check_git_merge(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_merge_always:
            return self._block(req, did, ts, "git.merge", "Git merge is always blocked", "git.block_merge_always", PolicySeverity.CRITICAL)
        return self._allow(req, did, ts, "git.merge", "Git merge allowed", "git.block_merge_always")

    def _check_git_force_push(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_force_push_always:
            return self._block(req, did, ts, "git.force_push", "Force push is always blocked", "git.block_force_push_always", PolicySeverity.CRITICAL)
        return self._allow(req, did, ts, "git.force_push", "Force push allowed", "git.block_force_push_always")

    def _check_git_commit(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_commit_without_approval:
            return self._block(req, did, ts, "git.commit", "Commit blocked, approval required", "git.block_commit_without_approval", PolicySeverity.HIGH)
        return self._allow(req, did, ts, "git.commit", "Commit allowed", "git.block_commit_without_approval")

    def _check_git_push(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        branch = req.branch or req.resource
        if branch in self.config.protected_branches:
            return self._block(req, did, ts, "git.push", f"Push to protected branch '{branch}' blocked", "git.block_push_without_approval", PolicySeverity.CRITICAL)
        if self.config.block_push_without_approval:
            return self._block(req, did, ts, "git.push", "Push blocked, approval required", "git.block_push_without_approval", PolicySeverity.HIGH)
        return self._allow(req, did, ts, "git.push", "Push allowed", "git.block_push_without_approval")

    def _check_filesystem_write(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        resource = req.resource or ""
        for pattern in self.config.allow_write_paths:
            if fnmatch.fnmatch(resource.replace("\\", "/"), pattern.replace("\\", "/")):
                return self._allow(req, did, ts, "filesystem.write", f"Write to '{resource}' is in allowed path", "filesystem.allow_write_without_approval")
            if fnmatch.fnmatch(resource, pattern):
                return self._allow(req, did, ts, "filesystem.write", f"Write to '{resource}' is in allowed path", "filesystem.allow_write_without_approval")
        return self._block(req, did, ts, "filesystem.write", f"Write to '{resource}' is outside allowed paths", "filesystem.allow_write_without_approval", PolicySeverity.HIGH)

    def _check_filesystem_delete(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_delete_without_approval:
            return self._block(req, did, ts, "filesystem.delete", "Delete blocked, approval required", "filesystem.block_delete_without_approval", PolicySeverity.HIGH)
        return self._allow(req, did, ts, "filesystem.delete", "Delete allowed", "filesystem.block_delete_without_approval")

    def _check_shell_run(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        command = (req.command or req.resource or "").strip()
        if not command:
            return self._block(req, did, ts, "shell.run", "Empty shell command blocked", "shell.block_unlisted", PolicySeverity.HIGH)

        for pattern in self.config.block_destructive_shell_patterns:
            if pattern in command:
                return self._block(req, did, ts, "shell.run", f"Destructive pattern '{pattern}' found in command", "shell.block_destructive_patterns", PolicySeverity.CRITICAL)

        if self.config.block_unlisted_shell and command not in self.config.shell_allowlist:
            return self._block(req, did, ts, "shell.run", f"Command '{command}' not in shell allowlist", "shell.block_unlisted", PolicySeverity.HIGH)

        return self._allow(req, did, ts, "shell.run", f"Command '{command}' is allowlisted", "shell.allowlist")

    def _check_secrets_read(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        return PolicyDecision(
            decision_id=did, execution_id=req.execution_id,
            action=req.action, resource=req.resource,
            allowed=True, severity=PolicySeverity.HIGH,
            reason="Secret read requires approval (handled by permission engine)",
            matched_policy="secrets.read", timestamp=ts,
        )

    def _check_secrets_output(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_secret_output:
            return self._block(req, did, ts, "secrets.output", "Secret value output blocked", "secrets.block_output_values", PolicySeverity.CRITICAL)
        return self._allow(req, did, ts, "secrets.output", "Secret output allowed", "secrets.block_output_values")

    def _check_package_extract(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_unverified_package_extract:
            verified = req.details.get("verified", False)
            if not verified:
                return self._block(req, did, ts, "package.extract", "Package extract blocked, verification required", "packaging.require_manifest", PolicySeverity.HIGH)
        return self._allow(req, did, ts, "package.extract", "Package extract allowed (verified)", "packaging.require_manifest")

    def _check_package_verify(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        return self._allow(req, did, ts, "package.verify", "Package verify allowed", "packaging.require_sha256")

    def _check_approval_wildcard(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_wildcard_approval:
            return self._block(req, did, ts, "approval.wildcard", "Wildcard approval blocked", "approval.wildcard", PolicySeverity.CRITICAL)
        return self._allow(req, did, ts, "approval.wildcard", "Wildcard approval allowed", "approval.wildcard")

    def _check_auto_merge(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_auto_merge:
            return self._block(req, did, ts, "auto_merge", "Auto-merge is always blocked", "auto_merge", PolicySeverity.CRITICAL)
        return self._allow(req, did, ts, "auto_merge", "Auto-merge allowed", "auto_merge")

    def _check_auto_deploy(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_auto_deploy:
            return self._block(req, did, ts, "auto_deploy", "Auto-deploy is always blocked", "auto_deploy", PolicySeverity.CRITICAL)
        return self._allow(req, did, ts, "auto_deploy", "Auto-deploy allowed", "auto_deploy")

    def _check_secret_persist(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_raw_secret_persistence:
            return self._block(req, did, ts, "secret.persist", "Raw secret persistence blocked", "secret.persist", PolicySeverity.CRITICAL)
        return self._allow(req, did, ts, "secret.persist", "Secret persistence allowed", "secret.persist")

    def _check_pack_import_direct(self, req: PolicyRequest, did: str, ts: str) -> PolicyDecision:
        if self.config.block_direct_active_pack_import:
            return self._block(req, did, ts, "pack.import_direct", "Direct active pack import blocked", "pack.import_direct", PolicySeverity.CRITICAL)
        return self._allow(req, did, ts, "pack.import_direct", "Direct pack import allowed", "pack.import_direct")

    def _block(self, req: PolicyRequest, did: str, ts: str, action: str, reason: str, policy: str, severity: str) -> PolicyDecision:
        return PolicyDecision(
            decision_id=did, execution_id=req.execution_id,
            action=action, resource=req.resource,
            allowed=False, severity=severity,
            reason=reason, matched_policy=policy, timestamp=ts,
        )

    def _allow(self, req: PolicyRequest, did: str, ts: str, action: str, reason: str, policy: str) -> PolicyDecision:
        return PolicyDecision(
            decision_id=did, execution_id=req.execution_id,
            action=action, resource=req.resource,
            allowed=True, severity=PolicySeverity.LOW,
            reason=reason, matched_policy=policy, timestamp=ts,
        )
