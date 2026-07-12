from __future__ import annotations

import logging
from collections.abc import Callable, Coroutine
from typing import Any

from aeos_lsp.commands.validate_document import validate_document
from aeos_lsp.commands.validate_workspace import validate_workspace
from aeos_lsp.commands.refresh_index import refresh_index
from aeos_lsp.commands.explain_diagnostic import explain_diagnostic
from aeos_lsp.commands.show_dependency_graph import show_dependency_graph
from aeos_lsp.commands.show_inheritance_graph import show_inheritance_graph
from aeos_lsp.commands.estimate_tokens import estimate_tokens
from aeos_lsp.commands.judge_artifact import judge_artifact
from aeos_lsp.commands.dry_run_skill import dry_run_skill
from aeos_lsp.commands.dry_run_playbook import dry_run_playbook
from aeos_lsp.commands.preview_resolution import preview_resolution
from aeos_lsp.commands.open_evidence import open_evidence
from aeos_lsp.commands.generate_stub import generate_stub

logger = logging.getLogger(__name__)

CommandHandler = Callable[[Any, dict[str, Any]], Coroutine[Any, Any, Any] | Any]


class CommandValidationError(Exception):
    def __init__(self, command: str, message: str) -> None:
        self.command = command
        self.message = message
        super().__init__(f"Validation error for command '{command}': {message}")


class CommandNotFoundError(Exception):
    def __init__(self, command: str) -> None:
        self.command = command
        super().__init__(f"Command '{command}' not found")


_ARG_SCHEMAS: dict[str, dict[str, Any]] = {
    "aeos.validateDocument": {
        "uri": {"type": str, "required": True},
    },
    "aeos.validateWorkspace": {},
    "aeos.refreshIndex": {},
    "aeos.explainDiagnostic": {
        "code": {"type": str, "required": True},
    },
    "aeos.showDependencyGraph": {
        "uri": {"type": str, "required": False},
        "stable_id": {"type": str, "required": False},
    },
    "aeos.showInheritanceGraph": {
        "uri": {"type": str, "required": False},
        "stable_id": {"type": str, "required": False},
    },
    "aeos.estimateTokens": {
        "uri": {"type": str, "required": True},
        "text": {"type": str, "required": False},
    },
    "aeos.judgeArtifact": {
        "uri": {"type": str, "required": True},
    },
    "aeos.dryRunSkill": {
        "skill_ref": {"type": str, "required": True},
        "inputs": {"type": dict, "required": False},
    },
    "aeos.dryRunPlaybook": {
        "playbook_ref": {"type": str, "required": True},
        "inputs": {"type": dict, "required": False},
    },
    "aeos.previewResolution": {
        "uri": {"type": str, "required": True},
        "position": {"type": dict, "required": True},
    },
    "aeos.openEvidence": {
        "artifact_id": {"type": str, "required": True},
    },
    "aeos.generateMissingStub": {
        "entity_type": {"type": str, "required": True},
        "name": {"type": str, "required": True},
        "uri": {"type": str, "required": False},
    },
}


class CommandRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, CommandHandler] = {}

    def register(self, command: str, handler: CommandHandler) -> None:
        if command in self._handlers:
            logger.warning("Overwriting existing handler for command '%s'", command)
        self._handlers[command] = handler
        logger.debug("Registered command handler: %s", command)

    def unregister(self, command: str) -> None:
        self._handlers.pop(command, None)

    def get_handler(self, command: str) -> CommandHandler | None:
        return self._handlers.get(command)

    def has_command(self, command: str) -> bool:
        return command in self._handlers

    def list_commands(self) -> list[str]:
        return list(self._handlers.keys())

    def validate_args(self, command: str, args: dict[str, Any]) -> None:
        schema = _ARG_SCHEMAS.get(command)
        if schema is None:
            return
        for param_name, param_schema in schema.items():
            value = args.get(param_name)
            if param_schema.get("required", False) and value is None:
                raise CommandValidationError(
                    command,
                    f"Missing required argument '{param_name}'",
                )
            expected_type = param_schema.get("type")
            if expected_type is not None and value is not None and not isinstance(value, expected_type):
                raise CommandValidationError(
                    command,
                    f"Argument '{param_name}' expected type {expected_type.__name__}, got {type(value).__name__}",
                )
        for key in args:
            if key not in schema:
                logger.debug("Unknown argument '%s' for command '%s'", key, command)

    async def dispatch(self, command: str, server: Any, args: dict[str, Any]) -> Any:
        if command not in self._handlers:
            raise CommandNotFoundError(command)
        self.validate_args(command, args)
        handler = self._handlers[command]
        result = handler(server, args)
        if hasattr(result, "__await__"):
            return await result
        return result

    def register_defaults(self) -> None:
        self.register("aeos.validateDocument", validate_document)
        self.register("aeos.validateWorkspace", validate_workspace)
        self.register("aeos.refreshIndex", refresh_index)
        self.register("aeos.explainDiagnostic", explain_diagnostic)
        self.register("aeos.showDependencyGraph", show_dependency_graph)
        self.register("aeos.showInheritanceGraph", show_inheritance_graph)
        self.register("aeos.estimateTokens", estimate_tokens)
        self.register("aeos.judgeArtifact", judge_artifact)
        self.register("aeos.dryRunSkill", dry_run_skill)
        self.register("aeos.dryRunPlaybook", dry_run_playbook)
        self.register("aeos.previewResolution", preview_resolution)
        self.register("aeos.openEvidence", open_evidence)
        self.register("aeos.generateMissingStub", generate_stub)

    def __repr__(self) -> str:
        return f"CommandRegistry(commands={len(self._handlers)})"
