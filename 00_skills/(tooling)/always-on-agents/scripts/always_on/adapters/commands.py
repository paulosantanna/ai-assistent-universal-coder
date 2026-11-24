"""Argv for the host CLIs. Arguments stay a list. Nothing is passed through a shell."""

from __future__ import annotations

from always_on.domain.billing import is_ollama
from always_on.domain.lifecycle import ResumeForbidden

RESUME_FLAGS = ("--resume", "--continue", "--session", "--fork")


class OllamaRejected(Exception):
    pass


class UnsupportedHost(Exception):
    pass


def _guard(binary: str, model: str, argv: list[str]) -> list[str]:
    if is_ollama(binary) or is_ollama(model):
        raise OllamaRejected(model or binary)
    if any(flag in argv for flag in RESUME_FLAGS):
        raise ResumeForbidden("a worker cannot resume")
    return argv


def cursor_argv(model: str, workspace: str, prompt: str) -> list[str]:
    # Flags verified against Cursor headless CLI docs on 2026-11-24.
    # --force is required so the headless worker can run the test command.
    # --sandbox enabled keeps that force inside the sandbox.
    argv = [
        "agent",
        "-p",
        "--output-format",
        "json",
        "--trust",
        "--force",
        "--sandbox",
        "enabled",
        "--workspace",
        workspace,
        "--model",
        model,
        prompt,
    ]
    return _guard(argv[0], model, argv)


def opencode_argv(model: str, workspace: str, prompt: str) -> list[str]:
    # Flags verified against https://opencode.ai/docs/cli/commands on 2026-11-24.
    # --continue and --session are intentionally absent: a worker cannot be resumed.
    argv = [
        "opencode",
        "run",
        "--model",
        model,
        "--format",
        "json",
        "--dir",
        workspace,
        "--auto",
        "--archived",
        prompt,
    ]
    return _guard(argv[0], model, argv)


def command_for(host: str, model: str, workspace: str, prompt: str) -> list[str]:
    if host == "cursor":
        return cursor_argv(model, workspace, prompt)
    if host == "opencode":
        return opencode_argv(model, workspace, prompt)
    raise UnsupportedHost(host)
