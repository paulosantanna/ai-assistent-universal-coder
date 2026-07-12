from __future__ import annotations

from pathlib import Path

import pytest

from aeos_lsp.security.redaction import RedactionEngine
from aeos_lsp.security.secret_detector import SecretDetector, SecretMatch
from aeos_lsp.security.path_policy import PathPolicy
from aeos_lsp.security.command_policy import CommandPolicy


class TestRedactionEngine:
    @pytest.fixture
    def engine(self) -> RedactionEngine:
        return RedactionEngine()

    def test_redact_api_key(self, engine):
        text = "api_key = sk-1234567890abcdefghijklmnop"
        result = engine.redact_text(text)
        assert "sk-" not in result
        assert "REDACTED" in result

    def test_redact_password(self, engine):
        text = "password = my_secret_password_123"
        result = engine.redact_text(text)
        assert "my_secret_password_123" not in result

    def test_redact_github_token(self, engine):
        text = "token = ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        result = engine.redact_text(text)
        assert "ghp_" not in result

    def test_redact_no_secrets(self, engine):
        text = "name = test-agent\ndescription = a harmless config"
        result = engine.redact_text(text)
        assert result == text

    def test_contains_secret(self, engine):
        assert engine.contains_secret("api_key = sk-1234567890abcdef")
        assert not engine.contains_secret("name = test-agent")

    def test_add_pattern(self, engine):
        import re
        engine.add_pattern("custom", re.compile(r"my_custom_secret_\w+"))
        assert "custom" in engine.list_patterns()


class TestSecretDetector:
    @pytest.fixture
    def detector(self) -> SecretDetector:
        return SecretDetector()

    def test_detect_github_token(self, detector):
        results = detector.detect("token = ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        assert len(results) > 0
        assert any(r.type == "GitHub Token" for r in results)

    def test_detect_aws_key(self, detector):
        results = detector.detect("aws_secret_access_key = wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY")
        assert len(results) > 0

    def test_detect_private_key(self, detector):
        text = "-----BEGIN RSA PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASC\n-----END RSA PRIVATE KEY-----"
        results = detector.detect(text)
        assert len(results) > 0

    def test_detect_no_secrets(self, detector):
        results = detector.detect("This is harmless text.")
        assert len(results) == 0

    def test_detect_by_type(self, detector):
        results = detector.detect_by_type("ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "GitHub Token")
        assert len(results) == 1


class TestSecretMatch:
    def test_match_creation(self):
        match = SecretMatch(
            type="test", value_preview="sk-1234",
            line=0, column=0, end_column=7,
            confidence=0.9,
        )
        assert match.type == "test"
        assert match.confidence == 0.9

    def test_to_dict(self):
        match = SecretMatch(
            type="GitHub Token", value_preview="ghp_xxx...",
            line=1, column=5, end_column=15,
            confidence=0.95, context="line context", entropy=5.2,
        )
        d = match.to_dict()
        assert d["type"] == "GitHub Token"


class TestPathPolicy:
    def test_allow_workspace_path(self, tmp_path):
        test_file = tmp_path / "config.yaml"
        test_file.write_text("test")
        policy = PathPolicy(workspace_roots=[str(tmp_path)], allow_absolute_paths=True)
        assert policy.is_path_allowed(str(test_file))

    def test_block_path_traversal(self, tmp_path):
        policy = PathPolicy(workspace_roots=[str(tmp_path)])
        traversal = str(tmp_path / ".." / ".." / ".." / "etc" / "passwd")
        assert not policy.is_path_allowed(traversal)

    def test_block_absolute_outside_workspace(self, tmp_path):
        policy = PathPolicy(workspace_roots=[str(tmp_path)])
        assert not policy.is_path_allowed(str(Path(tmp_path.anchor) / "etc" / "passwd"))

    def test_allow_subdirectory(self, tmp_path):
        sub = tmp_path / "subdir" / "data.yaml"
        sub.parent.mkdir(parents=True, exist_ok=True)
        sub.write_text("data")
        policy = PathPolicy(workspace_roots=[str(tmp_path)], allow_absolute_paths=True)
        assert policy.is_path_allowed(str(sub))

    def test_allow_relative_path(self, tmp_path):
        policy = PathPolicy(workspace_roots=[str(tmp_path)], allow_absolute_paths=True)
        import os
        old_cwd = os.getcwd()
        os.chdir(str(tmp_path))
        try:
            assert policy.is_path_allowed("relative/path.yaml")
        finally:
            os.chdir(old_cwd)


class TestCommandPolicy:
    @pytest.fixture
    def policy(self) -> CommandPolicy:
        return CommandPolicy()

    def test_allow_safe(self, policy):
        assert policy.is_command_allowed("python script.py")

    def test_block_destructive(self, policy):
        assert not policy.is_command_allowed("rm -rf /")
        assert not policy.is_command_allowed("dd if=/dev/zero of=/dev/sda")
