from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from lsprotocol.types import WorkspaceFolder

from aeos_lsp.configuration import LSPClientConfig, merge_config
from aeos_lsp.workspace.cache import DocumentCache
from aeos_lsp.workspace.document_store import DocumentStore
from aeos_lsp.workspace.exclusions import Exclusions
from aeos_lsp.workspace.file_watcher import FileWatcher
from aeos_lsp.workspace.folders import WorkspaceFolderInfo, detect_aeos_root, validate_folder


class WorkspaceManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._folders: dict[str, WorkspaceFolderInfo] = {}
        self._trusted: bool = False
        self._config: LSPClientConfig = LSPClientConfig()
        self._document_store = DocumentStore()
        self._file_watcher = FileWatcher()
        self._cache = DocumentCache()
        self._exclusions = Exclusions()

    @property
    def document_store(self) -> DocumentStore:
        return self._document_store

    @property
    def file_watcher(self) -> FileWatcher:
        return self._file_watcher

    @property
    def cache(self) -> DocumentCache:
        return self._cache

    @property
    def exclusions(self) -> Exclusions:
        return self._exclusions

    @property
    def root_uri(self) -> str | None:
        with self._lock:
            if not self._folders:
                return None
            return next(iter(self._folders.values())).uri

    @property
    def workspace_folders(self) -> list[WorkspaceFolderInfo]:
        with self._lock:
            return list(self._folders.values())

    def get_folder(self, uri: str) -> WorkspaceFolderInfo | None:
        with self._lock:
            return self._folders.get(uri)

    def add_folder(self, folder: WorkspaceFolderInfo) -> None:
        with self._lock:
            self._folders[folder.uri] = folder

    def remove_folder(self, uri: str) -> bool:
        with self._lock:
            return self._folders.pop(uri, None) is not None

    def update_folders(self, added: list[WorkspaceFolderInfo], removed: list[str]) -> None:
        with self._lock:
            for folder in added:
                self._folders[folder.uri] = folder
            for uri in removed:
                self._folders.pop(uri, None)

    def get_config(self, uri: str | None = None) -> LSPClientConfig:
        if uri is not None:
            folder = self.get_folder(uri)
            if folder is not None:
                return folder.config
        return self._config

    def update_config(self, config: LSPClientConfig) -> None:
        self._config = config

    def is_trusted(self, uri: str | None = None) -> bool:
        if uri is not None:
            folder = self.get_folder(uri)
            if folder is not None:
                return folder.trusted
        return self._trusted

    def set_trusted(self, trusted: bool, uri: str | None = None) -> None:
        if uri is not None:
            folder = self.get_folder(uri)
            if folder is not None:
                from dataclasses import replace
                updated = replace(folder, trusted=trusted)
                self._folders[uri] = updated
        else:
            self._trusted = trusted
