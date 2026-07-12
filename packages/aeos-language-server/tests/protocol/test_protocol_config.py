from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from lsprotocol.types import (
    DidChangeConfigurationParams,
    DidChangeWatchedFilesParams,
    DidChangeWorkspaceFoldersParams,
    FileChangeType,
    FileEvent,
    WorkspaceFoldersChangeEvent,
)

from aeos_lsp.protocol.lifecycle import AEOSLifecycleManager


@pytest.fixture
def manager():
    ls = MagicMock()
    return AEOSLifecycleManager(ls)


class TestProtocolConfig:
    def test_did_change_configuration(self, manager):
        params = DidChangeConfigurationParams(
            settings={
                "enableExperimentalFeatures": True,
                "maxDiagnosticsPerFile": 200,
            }
        )
        manager.handle_workspace_did_change_configuration(params)
        assert manager.experimental_enabled is True

    def test_did_change_configuration_empty(self, manager):
        params = DidChangeConfigurationParams(settings={})
        manager.handle_workspace_did_change_configuration(params)
        assert manager.experimental_enabled is False

    def test_did_change_configuration_none(self, manager):
        params = DidChangeConfigurationParams(settings=None)
        manager.handle_workspace_did_change_configuration(params)

    def test_workspace_did_change_watched_files(self, manager):
        params = DidChangeWatchedFilesParams(
            changes=[
                FileEvent(uri="file:///test.yaml", type=FileChangeType.Changed),
                FileEvent(uri="file:///new.yaml", type=FileChangeType.Created),
                FileEvent(uri="file:///del.yaml", type=FileChangeType.Deleted),
            ]
        )
        manager.handle_workspace_did_change_watched_files(params)

    def test_workspace_did_change_workspace_folders_add(self, manager):
        from lsprotocol.types import WorkspaceFolder
        params = DidChangeWorkspaceFoldersParams(
            event=WorkspaceFoldersChangeEvent(
                added=[WorkspaceFolder(uri="file:///new", name="New Folder")],
                removed=[],
            )
        )
        manager.handle_workspace_did_change_workspace_folders(params)
        uris = [wf.uri for wf in manager.workspace_folders]
        assert "file:///new" in uris

    def test_workspace_did_change_workspace_folders_remove(self, manager):
        from lsprotocol.types import WorkspaceFolder
        add_params = DidChangeWorkspaceFoldersParams(
            event=WorkspaceFoldersChangeEvent(
                added=[WorkspaceFolder(uri="file:///remove-me", name="Remove")],
                removed=[],
            )
        )
        manager.handle_workspace_did_change_workspace_folders(add_params)
        assert "file:///remove-me" in [wf.uri for wf in manager.workspace_folders]

        remove_params = DidChangeWorkspaceFoldersParams(
            event=WorkspaceFoldersChangeEvent(
                added=[],
                removed=[WorkspaceFolder(uri="file:///remove-me", name="Remove")],
            )
        )
        manager.handle_workspace_did_change_workspace_folders(remove_params)
        assert "file:///remove-me" not in [wf.uri for wf in manager.workspace_folders]

    def test_workspace_folders_initial(self):
        ls = MagicMock()
        from lsprotocol.types import InitializeParams, ClientCapabilities, WorkspaceFolder
        manager = AEOSLifecycleManager(ls)
        params = InitializeParams(
            process_id=1234,
            capabilities=ClientCapabilities(),
            workspace_folders=[
                WorkspaceFolder(uri="file:///init1", name="Init1"),
                WorkspaceFolder(uri="file:///init2", name="Init2"),
            ],
        )
        manager.handle_initialize(params)
        assert len(manager.workspace_folders) == 2
