from __future__ import annotations

from aeos.core.registries.registry_models import (
    ConsolidatedRegistry,
    FragmentCategory,
    LoadedFragment,
    OrphanRecord,
)


class OverlayRegistryMerger:
    def __init__(self):
        self.registry = ConsolidatedRegistry()
        self.deduplication_log: list[dict] = []
        self.conflict_log: list[dict] = []

    def merge(self, fragments: list[LoadedFragment]) -> ConsolidatedRegistry:
        self.registry = ConsolidatedRegistry()
        self.deduplication_log = []
        self.conflict_log = []

        base_fragments = [f for f in fragments if f.metadata.category == FragmentCategory.BASE and f.metadata.loaded]
        additions_fragments = [f for f in fragments if f.metadata.category == FragmentCategory.ADDITIONS and f.metadata.loaded]
        enterprise_fragments = [f for f in fragments if f.metadata.category == FragmentCategory.ENTERPRISE and f.metadata.loaded]

        for frag in base_fragments:
            self._merge_fragment(frag, priority=0)

        for frag in additions_fragments:
            self._merge_fragment(frag, priority=1)

        for frag in enterprise_fragments:
            self._merge_fragment(frag, priority=2)

        return self.registry

    def _merge_fragment(self, frag: LoadedFragment, priority: int) -> None:
        for entry in frag.agents:
            self._merge_entry("agents", entry, frag.metadata.path, priority)

        for entry in frag.subagents:
            if entry.id not in self.registry.subagents:
                self.registry.subagents[entry.id] = entry

        for entry in frag.skills:
            self._merge_entry("skills", entry, frag.metadata.path, priority)

        for entry in frag.playbooks:
            self._merge_entry("playbooks", entry, frag.metadata.path, priority)

        for entry in frag.mcps:
            self._merge_entry("mcps", entry, frag.metadata.path, priority)

        for entry in frag.lcps:
            self._merge_entry("lcps", entry, frag.metadata.path, priority)

        for entry in frag.blueprints:
            if entry.id not in self.registry.blueprints:
                self.registry.blueprints[entry.id] = entry

        for entry in frag.profiles:
            if entry.id not in self.registry.profiles:
                self.registry.profiles[entry.id] = entry

    def _merge_entry(self, reg_type: str, entry: any, source_path: str, priority: int) -> None:
        target = getattr(self.registry, reg_type, None)
        if target is None:
            return

        if entry.id in target:
            existing = target[entry.id]
            existing_path = getattr(existing, "path", None) or ""
            incoming_path = getattr(entry, "path", None) or ""

            if existing_path == incoming_path:
                self.deduplication_log.append({
                    "entry_id": entry.id,
                    "registry_type": reg_type,
                    "path": existing_path,
                    "kept_from": source_path,
                    "deduplicated": True,
                })
            else:
                self.conflict_log.append({
                    "entry_id": entry.id,
                    "registry_type": reg_type,
                    "existing_path": existing_path,
                    "conflicting_path": incoming_path,
                    "existing_source": getattr(existing, "_source", "unknown"),
                    "conflicting_source": source_path,
                })
            return

        if hasattr(entry, "_source"):
            entry._source = source_path
        target[entry.id] = entry
