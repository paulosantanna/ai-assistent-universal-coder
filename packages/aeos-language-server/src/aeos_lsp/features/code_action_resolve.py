from __future__ import annotations

import threading
from typing import Any

from lsprotocol.types import (
    CodeAction,
    CodeActionKind,
    Command,
    Position,
    Range,
    TextEdit,
    WorkspaceEdit,
)
from pygls.lsp.server import LanguageServer

from aeos_lsp.semantic.semantic_model import SemanticModel


class CodeActionResolveFeature:
    def __init__(self, server: LanguageServer, semantic_model: SemanticModel) -> None:
        self._server = server
        self._semantic_model = semantic_model
        self._lock = threading.RLock()

    def resolve_code_action(self, action: CodeAction) -> CodeAction:
        with self._lock:
            cmd = action.command
            if cmd is None:
                return action

            resolved = self._resolve_command(cmd)
            if resolved is not None:
                action.edit = resolved

            return action

    def _resolve_command(self, command: Command) -> WorkspaceEdit | None:
        cmd = command.command
        args = command.arguments or []

        if cmd == "aeos.addRegistration":
            return self._edit_add_registration(*args)
        elif cmd == "aeos.fixReference":
            return self._edit_fix_reference(*args)
        elif cmd == "aeos.addTimeout":
            return self._edit_add_timeout(*args)
        elif cmd == "aeos.addRetryLimit":
            return self._edit_add_retry_limit(*args)
        elif cmd == "aeos.addRollback":
            return self._edit_add_rollback(*args)
        elif cmd == "aeos.addApproval":
            return self._edit_add_approval(*args)
        elif cmd == "aeos.addEvidenceRequirement":
            return self._edit_add_evidence(*args)
        elif cmd == "aeos.fixTokenBudget":
            return self._edit_fix_token_budget(*args)
        elif cmd == "aeos.migrateDeprecatedField":
            return self._edit_migrate_deprecated(*args)
        elif cmd == "aeos.normalizeFrontMatter":
            return self._edit_normalize_front_matter(*args)
        elif cmd == "aeos.deduplicateRegistryEntry":
            return self._edit_deduplicate_registry(*args)
        elif cmd == "aeos.fixRelativePath":
            return self._edit_fix_relative_path(*args)
        elif cmd == "aeos.addDefaultExclusions":
            return self._edit_add_default_exclusions(*args)

        return None

    def _edit_add_registration(self, uri: str, message: str, range_: Any) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text=f"\n# TODO: Add registration for: {message}\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _edit_fix_reference(self, uri: str, range_: Any) -> WorkspaceEdit:
        r = Range(
            start=Position(line=range_["start"]["line"], character=range_["start"]["character"]) if isinstance(range_, dict) else Position(line=0, character=0),
            end=Position(line=range_["end"]["line"], character=range_["end"]["character"]) if isinstance(range_, dict) else Position(line=0, character=0),
        )
        return WorkspaceEdit(changes={uri: [TextEdit(range=r, new_text="# FIXME: resolve reference")]})

    def _edit_add_timeout(self, uri: str, range_: Any) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text="  timeout: 30\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _edit_add_retry_limit(self, uri: str, range_: Any) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text="  retry: 3\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _edit_add_rollback(self, uri: str, range_: Any) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text="  rollback:\n    name: rollback_plan\n    steps:\n      - rollback_step_1\n    strategy: sequential\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _edit_add_approval(self, uri: str, range_: Any) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text="  approval:\n    required_approvals: 1\n    scope: step\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _edit_add_evidence(self, uri: str, range_: Any) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text="  evidence_requirements:\n    - type: tool_calls\n      hash_required: true\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _edit_fix_token_budget(self, uri: str, range_: Any) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text="  token_budget:\n    max_input_tokens: 8000\n    max_output_tokens: 4000\n    max_total_tokens: 16000\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _edit_migrate_deprecated(self, uri: str, message: str, range_: Any) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text=f"# DEPRECATED: {message}\n# TODO: migrate to new field\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _edit_normalize_front_matter(self, uri: str) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text="---\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})

    def _edit_deduplicate_registry(self, uri: str) -> WorkspaceEdit:
        return WorkspaceEdit(changes=None)

    def _edit_fix_relative_path(self, uri: str, range_: Any) -> WorkspaceEdit:
        r = Range(
            start=Position(line=range_["start"]["line"], character=range_["start"]["character"]) if isinstance(range_, dict) else Position(line=0, character=0),
            end=Position(line=range_["end"]["line"], character=range_["end"]["character"]) if isinstance(range_, dict) else Position(line=0, character=0),
        )
        return WorkspaceEdit(changes={uri: [TextEdit(range=r, new_text="./")]})

    def _edit_add_default_exclusions(self, uri: str) -> WorkspaceEdit:
        edit = TextEdit(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=0),
            ),
            new_text="  exclusions:\n    - .git\n    - node_modules\n    - .venv\n    - __pycache__\n",
        )
        return WorkspaceEdit(changes={uri: [edit]})
